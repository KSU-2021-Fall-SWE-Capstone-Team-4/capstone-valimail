def load_dotenv():
    """
    Loads the .env file. Also checks to make sure that the file exists, and that all required
    variables are accounted for.

    Raises:
        InvalidDotenvFileError : .env file is either missing or is lacking a required variable.
    """
    # Required imports
    from lib.util.exceptions import InvalidDotenvFileError
    import os

    # List of variables we should expect to see in every .env file.
    expected_dotenv_vars = [
        'DEBUG', 'DISABLE_SENDER', 'MQTT_LISTENER_USERNAME', 'MQTT_LISTENER_PASSWORD',
        'MQTT_LISTENER_HOSTNAME', 'MQTT_LISTENER_PORT', 'MQTT_LISTENER_TOPICS',
        'MQTT_SENDER_USERNAME', 'MQTT_SENDER_PASSWORD', 'MQTT_SENDER_HOSTNAME',
        'MQTT_SENDER_PORT', 'MQTT_SENDER_TOPICS', 'DNS_WHITELIST', 'DNS_TIMEOUT_SECONDS'
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

    # Check non-string data types.
    expected_dotenv_types = {
        'DEBUG': bool,
        'DISABLE_SENDER': bool,
        'MQTT_LISTENER_PORT': int,
        'MQTT_SENDER_PORT': int,
        'DNS_TIMEOUT_SECONDS': int
    }

    # Detect any non-compliant data types.
    for var_name in expected_dotenv_types:
        # Bool detection (written as 0 or 1 in .env file, for simplicity) and integer protection are packaged together.
        if expected_dotenv_types[var_name] is bool or expected_dotenv_types[var_name] is int:
            try:
                int(os.environ[var_name])
            except ValueError:
                raise InvalidDotenvFileError(f'Variable {var_name} is not of type {expected_dotenv_types[var_name]}')