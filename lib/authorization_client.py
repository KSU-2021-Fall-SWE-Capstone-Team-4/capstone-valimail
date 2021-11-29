from dane_jwe_jws.authentication import Authentication
from dane_discovery.exceptions import TLSAError
from binascii import Error as ASCIIError
from lib.util import environment, logger
from lib.mqtt_sender import MQTTSender
from dane_jwe_jws.util import Util
import multiprocessing
import threading
import logging
import base64
import json


class AuthorizationClient(threading.Thread):

    def __init__(self, message=None):
        """
        Initializer for AuthorizationClient thread.
        Used locally in the static handle_message method.

        Arguments:
            message (paho.mqtt.client.MQTTMessage) : The message object.
        """
        self.message = message
        threading.Thread.__init__(self)

    def run(self):
        """
        The run method is, of course, run when a new thread is started.
        It logs the message on the debug channel, authorizes, then logs it on the info level.
        """
        # If logger not yet in post-setup mode, put it in post-setup mode.
        if not logger.SETUP_OVER:
            logger.log_setup_end_header()

        # Log the message.
        logging.debug(f'Message recieved on {self.message.topic}: {self.message.payload}')

        # Run the static authorization method.
        if AuthorizationClient.authorized(self.message)[0]:

            # Authorized, log message
            logging.debug('Message authorized, forwarding to sender')
            logging.info(f'Authorized message recieved on {self.message.topic}: {self.message.payload}')

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

        Returns:
            bool, Exception : Whether or not the message is authorized to proceed, combined with the reason it failed, if any.
                              Reason failed is used pretty much exclusively for testing purposes.
        """
        # First, convert the message into a json file.
        try:
            message_payload_json = json.loads(message.payload)
        except json.JSONDecodeError as e:
            logging.debug('Message not formatted as JSON dict, auth cancelled')
            return False, e

        # Grab the protected attribute.
        try:
            protected = message_payload_json['protected']
        except KeyError as e:
            logging.debug('Message missing "protected" attribute, auth cancelled')
            return False, e

        # Next, convert the protected attribute out of base64.
        try:
            protected = base64.b64decode(protected)
        except ASCIIError as e:
            logging.debug('"protected" attribute does not convert out of base64, auth cancelled')
            return False, e

        # Then, we make the protected attribute into a dict as well.
        try:
            protected_json = json.loads(protected)
        except json.JSONDecodeError as e:
            logging.debug('"protected" attribute is not formatted as JSON dict, auth cancelled')
            return False, e

        # Grab the x5u attribute.
        try:
            x5u = protected_json['x5u']
        except KeyError as e:
            logging.debug('Message\'s "protected" attribute missing "x5u" attribute, auth cancelled')
            return False, e

        # Finally, we trim the excess fat off x5u and compare it against the whitelist.
        try:
            x5u = Util.get_name_from_dns_uri(x5u)
        except ValueError as e:
            logging.debug('Message\'s DNS URI is formatted incorrectly, auth cancelled')
            return False, e
        if x5u not in environment.get('DNS_WHITELIST'):
            logging.debug('Message\'s DNS name is not included in the whitelist, auth cancelled')
            return False, None

        # Now that we know the message is from a whitelisted source, we verify its integrity using the
        # authorize_with_timeout method.
        passed_authentication = AuthorizationClient.verify_authentication_with_timeout(message.payload, x5u)

        # If no exception has been raised / we have not returned yet, then message passed all the checks.
        return passed_authentication, None

    @staticmethod
    def verify_authentication_with_timeout(message_payload, dns_name):
        """
        Authorizes a message with timeout, implemented using the multiprocessing module.

        Arguments:
            message_payload (dict) : The message payload. Used to get the DNS name and verify.
            dns_name (str) : The DNS name. Used for logging purposes.
        """
        # Log that we made it this far.
        logging.debug('Authorizing message with timeout...')

        # First, get the context and a queue; this will allow us to return a boolean value from the _authorize method.
        context = multiprocessing.get_context('spawn')
        queue = context.Queue()

        # Instantiate the process, with the target at _authorize and the queue and message_payload as arguments.
        process = context.Process(target=AuthorizationClient._authorize, args=(queue, message_payload, threading.get_ident()))
        process.start()

        # Wait for the process to join with a timeout variable (changed in .env).
        process.join(environment.get('DNS_TIMEOUT_SECONDS'))

        # Check if the process is still alive (timed out). If so, kill it and return False.
        if process.is_alive():
            process.terminate()
            logging.debug(f'Timed out when accessing TSLA records at {dns_name}')
            return False

        # Process concluded normally, gather the output from the queue.
        result = queue.get()

        # Log the result and return.
        logging.debug(f'Message was{" " if result else " not "}authenticated')
        return result

    @staticmethod
    def _authorize(queue, message_payload, parent_thread_id):
        """
        Protected authorize method used in a second process to implement timeout.

        Arguments:
            queue (context.Queue) : The context queue. Used to return boolean values.
            message_payload (dict) : The message payload. Used to get the DNS name and verify.
            parent_thread_id (int) : The id of the parent thread. Used for logging purposes.
        """
        # Run the verification
        try:
            Authentication.verify(message_payload)

        # Failed, log the error.
        except TLSAError as e:
            logger.log_outside_main_process(logging.DEBUG, repr(e), parent_thread_id)
            queue.put(False)
            return

        # Unexpected exception, log and return..
        except Exception as e:
            logger.log_outside_main_process(logging.DEBUG, f'Unexpected exception: {repr(e)}', parent_thread_id)
            queue.put(False)
            return

        # Passed, set the queue value to true
        queue.put(True)
