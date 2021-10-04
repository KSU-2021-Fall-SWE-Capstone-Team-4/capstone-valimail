from lib.mqtt_sender import MQTTSender

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
        #x5u in payload contains device id
        # dane-jwe-jws
        AuthorizationClient.sender.publish('my/test/topic', message.payload)