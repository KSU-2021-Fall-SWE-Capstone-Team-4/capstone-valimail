class Util:

    @staticmethod
    def load_dotenv():
        """
        Loads the .env file. Also checks to make sure that the file exists, and that all required
        variables are accounted for.

        Raises:
            InvalidDotenvFileError : .env file is either missing or is lacking a required variable.
        """
        # Required imports
        from lib.exceptions import InvalidDotenvFileError
        import os

        # List of variables we should expect to see in every .env file.
        expected_dotenv_vars = [
            'DEBUG', 'DISABLE_SENDER', 'MQTT_LISTENER_USERNAME', 'MQTT_LISTENER_PASSWORD',
            'MQTT_LISTENER_HOSTNAME', 'MQTT_LISTENER_HOSTNAME', 'MQTT_LISTENER_PORT',
            'MQTT_LISTENER_TOPICS', 'MQTT_SENDER_USERNAME', 'MQTT_SENDER_PASSWORD',
            'MQTT_SENDER_HOSTNAME', 'MQTT_SENDER_PORT', 'MQTT_SENDER_TOPICS', 'DNS_WHITELIST',
            'DNS_TIMEOUT_SECONDS'
        ]

        # First, check that the .env file does exist.
        if not os.path.exists('.env'):
            raise InvalidDotenvFileError('.env file missing from working directory')

        # Then, load .env.
        from dotenv import load_dotenv as dotenv_load
        dotenv_load()

        # Detect if any dotenv_vars are missing.
        for dotenv_var in expected_dotenv_vars:
            if dotenv_var not in os.environ.keys():
                raise InvalidDotenvFileError(f'Missing variable {dotenv_var}')