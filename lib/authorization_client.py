from dane_jwe_jws.authentication import Authentication
from lib.mqtt_sender import MQTTSender
from dane_jwe_jws.util import Util
from lib.util import environment
import multiprocessing
import base64
import json
import time


class AuthorizationClient:

    @staticmethod
    def initialize():
        """
        Initializes the AuthorizationClient.
        """
        # Make sure this hasn't been run twice.
        if hasattr(AuthorizationClient, 'initialized') and AuthorizationClient.initialized:
            return

        # Create the MQTTSender.
        AuthorizationClient.sender = MQTTSender()

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
        process.join(9)

        # Check if the process is still alive (timed out). If so, kill it and return False.
        if process.is_alive():
            process.terminate()
            return False

        # Process concluded normally, gather the output from the queue.
        return queue.get()

    @staticmethod
    def _authorize(queue, message_payload):
        queue.put(False)
        Authentication.verify(message_payload)
        queue.put(True)