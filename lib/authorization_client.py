class AuthorizationClient:

    @staticmethod
    def authorize(message):
        """
        Usually this would be where the authorization goes.
        However, this is sprint 1, and we don't need to worry ourselves with that just yet.
        As such, it just passes along the message to the MQTT Sender.
        """