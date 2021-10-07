from dane_jwe_jws.authentication import Authentication
from lib.mqtt_sender import MQTTSender
from dane_jwe_jws.util import Util
import base64
import json
import os


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
    def authorize(message):
        """
        Usually this would be where the authorization goes.
        However, this is sprint 1, and we don't need to worry ourselves with that just yet.
        As such, it just passes along the message to the MQTT Sender.
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
        if x5u not in os.environ['DNS_WHITELIST'].split(','):
            return

        # Now that we know the message is from a whitelisted source, we verify its integrity.
        Authentication.verify(message.payload)

        # If no exception has been raised / we have not returned yet, then message passed all the checks.
        # Forward the message.
        AuthorizationClient.sender.publish('my/test/topic', message.payload)