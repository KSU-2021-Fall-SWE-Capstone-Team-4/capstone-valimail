from dane_jwe_jws.authentication import Authentication
from lib.mqtt_sender import MQTTSender
from dane_jwe_jws.util import Util
from lib.util import environment
from threading import Thread
import multiprocessing
import logging
import base64
import json
import time


class AuthorizationClient(Thread):

    def __init__(self, message=None):
        """
        Initializer for AuthorizationClient thread.
        Used locally in the static handle_message method.

        Arguments:
            message (paho.mqtt.client.MQTTMessage) : The message object.
        """
        self.message = message
        Thread.__init__(self)

    def run(self):
        """
        The run method is, of course, run when a new thread is started.
        """
        # Log the message.
        logging.debug(f'Message recieved on {self.message.topic}: {self.message.payload}')

        # Run the static authorization method.
        if AuthorizationClient.authorized(self.message):
            # Forward the message.
            if not environment.get('DISABLE_SENDER'):
                AuthorizationClient.sender.publish(self.message.payload)

    @staticmethod
    def initialize():
        """
        Initializes the AuthorizationClient's static methods.
        Individual AuthorizationClient threads are not started here.
        """
        # Make sure this hasn't been run twice.
        if hasattr(AuthorizationClient, 'initialized') and AuthorizationClient.initialized:
            return

        # Create the MQTTSender.
        AuthorizationClient.sender = MQTTSender()

    @staticmethod
    def handle_message(message):
        """
        Handles a message receieved from the MQTTListener.
        Starts a new thread that handles the authentication, error handling, and forwarding.

        Arguments:
            message (paho.mqtt.client.MQTTMessage) : The message object.
        """
        # Starts the client.
        client = AuthorizationClient(message)
        client.start()

    @staticmethod
    def authorized(message):
        """
        Determines whether or not a message is authorized.
        First checks if the dns name is on the whitelist defined in .env.
        Then checks whether the message itself has a valid TLSA record with the supplied dns name.
        If it passes all the checks, then True is returned.

        Arguments:
            message (MQTTMessage) : The message received from the MQTTListener.

        Raises:
            json.decoder.JSONDecodeError : The message received is not in a valid JSON format.
            binascii.Error : One or more fields has a non-base64 character in it.
            dane_discovery.exceptions.TLSAError : No TLSA records for supplied dns name.

        Returns:
            bool : Whether or not the message is authorized to proceed.
        """
        # First, convert the message into a json file and grab its 'protected' attribute.
        message_payload_json = json.loads(message.payload)
        protected = message_payload_json['protected']

        # Next, convert the protected attribute out of base64.
        protected = base64.b64decode(protected)

        # Then, we make the protected attribute into a dict as well and grab its 'x5u' attribute.
        protected_json = json.loads(protected)
        x5u = protected_json['x5u']

        # Finally, we trim the excess fat off x5u and compare it against the whitelist.
        x5u = Util.get_name_from_dns_uri(x5u)
        if x5u not in environment.get('DNS_WHITELIST'):
            return False

        # Now that we know the message is from a whitelisted source, we verify its integrity using the authorize_with_timeout method.
        passed_authentication = AuthorizationClient.verify_authentication_with_timeout(message.payload)

        # If no exception has been raised / we have not returned yet, then message passed all the checks.
        return passed_authentication

    @staticmethod
    def verify_authentication_with_timeout(message_payload):
        """
        Authorizes a message with timeout, implemented using the multiprocessing module.
        """
        # First, get the context and a queue; this will allow us to return a boolean value from the _authorize method.
        context = multiprocessing.get_context('spawn')
        queue = context.Queue()

        # Instantiate the process, with the target at _authorize and the queue and message_payload as arguments.
        process = context.Process(target=AuthorizationClient._authorize, args=(queue, message_payload))
        process.start()

        # Wait for the process to join with a timeout variable (changed in .env).
        process.join(environment.get('DNS_TIMEOUT_SECONDS'))

        # Check if the process is still alive (timed out). If so, kill it and return False.
        if process.is_alive():
            process.terminate()
            return False

        # Process concluded normally, gather the output from the queue.
        return queue.get()

    @staticmethod
    def _authorize(queue, message_payload):
        # Set the queue value to false (in case of an exception)
        queue.put(False)
        # Run the verification
        Authentication.verify(message_payload)
        # Passed, set the queue value to true
        queue.put(True)