class Util:

    @staticmethod
    def load_dotenv():
        """
        Loads the .env file. Also checks to make sure that the file exists, and that all required
        variables are accounted for.

        Raises:
            InvalidDotenvFileError : .env file is either missing or is lacking a required variable.
        """

        expected_dotenv_vars = [
            'DEBUG', 'DISABLE_SENDER', 'MQTT_LISTENER_USERNAME', 'MQTT_LISTENER_PASSWORD',
            'MQTT_LISTENER_HOSTNAME', 'MQTT_LISTENER_HOSTNAME', 'MQTT_LISTENER_PORT',
            'MQTT_LISTENER_TOPICS', 'MQTT_SENDER_USERNAME', 'MQTT_SENDER_PASSWORD',
            'MQTT_SENDER_HOSTNAME', 'MQTT_SENDER_PORT', 'MQTT_SENDER_TOPIC', 'DNS_WHITELIST'
        ]

        from lib.exceptions import InvalidDotenvFileError

        # TODO: Detect when user has not set up .env (possible with os.path.exists i think.)
        from dotenv import load_dotenv as dotenv_load
        dotenv_load(verbose=True)

        # Import os so we can certify that every dotenv variable is in there.
        import os

        # Detect if any dotenv_vars are missing.
        for dotenv_var in expected_dotenv_vars:
            if dotenv_var not in os.environ.keys():
                raise InvalidDotenvFileError(f'Missing variable {dotenv_var}')