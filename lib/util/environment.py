from lib.util.exceptions import UndefinedVariableError
import os

# List of variables we should expect to see in every .env file.
EXPECTED_DOTENV_VARS = [
    'DEBUG', 'DISABLE_SENDER', 'MQTT_LISTENER_USERNAME', 'MQTT_LISTENER_PASSWORD',
    'MQTT_LISTENER_HOSTNAME', 'MQTT_LISTENER_PORT', 'MQTT_LISTENER_TOPICS',
    'MQTT_SENDER_USERNAME', 'MQTT_SENDER_PASSWORD', 'MQTT_SENDER_HOSTNAME',
    'MQTT_SENDER_PORT', 'MQTT_SENDER_TOPICS', 'DNS_WHITELIST', 'DNS_TIMEOUT_SECONDS'
]
# List of expected .env types. Used in both load_dotenv and get.
EXPECTED_DOTENV_TYPES = {
    'DEBUG': bool,
    'DISABLE_SENDER': bool,
    'MQTT_LISTENER_PORT': int,
    'MQTT_LISTENER_TOPICS': list,
    'MQTT_SENDER_PORT': int,
    'MQTT_SENDER_TOPICS': list,
    'DNS_WHITELIST': list,
    'DNS_TIMEOUT_SECONDS': int
}


def load_dotenv():
    """
    Loads the .env file. Also checks to make sure that the file exists, and that all required
    variables are accounted for.

    Raises:
        InvalidDotenvFileError : .env file is either missing or is lacking a required variable.
    """
    # Required imports
    from lib.util.exceptions import InvalidDotenvFileError

    # First, check that the .env file does exist.
    if not os.path.exists('.env'):
        raise InvalidDotenvFileError('.env file missing from working directory')

    # Then, load .env.
    from dotenv import load_dotenv as dotenv_load
    dotenv_load()

    # Detect if any dotenv_vars are missing.
    for dotenv_var in EXPECTED_DOTENV_VARS:
        if dotenv_var not in os.environ.keys():
            raise InvalidDotenvFileError(f'Missing variable {dotenv_var}')

    # Detect any non-str data types.
    # List is excluded from this check, as the only way to derive lists in .env is to split them by comma.
    for var_name in EXPECTED_DOTENV_TYPES:
        # Bool detection (written as 0 or 1 in .env file, for simplicity) and integer protection are packaged together.
        if EXPECTED_DOTENV_TYPES[var_name] is bool or EXPECTED_DOTENV_TYPES[var_name] is int:
            try:
                int(os.environ[var_name])
            except ValueError:
                raise InvalidDotenvFileError(f'Variable {var_name} is not of type {EXPECTED_DOTENV_TYPES[var_name]}')


def get(variable_name):
    """
    Returns a variable declared in the .env file.
    Acts as a semi-wrapper for os.environ, with minor differences.
    Will only return values declared in the .env file.

    Arguments:
        variable_name (str) : The name of the desired variable.

    Returns:
        bool | int | str | list : Either a boolean, integer, string, or list value, depending on the variable.

    Raises:
        UndefinedVariableError: The variable name provided is not one that is provided in the .env file.
    """
    # Check to make sure the variable name is a valid one.
    if variable_name not in EXPECTED_DOTENV_VARS:
        raise UndefinedVariableError(f'{variable_name} is not a valid .env variable')

    # If variable type is str, simply return it.
    if variable_name not in EXPECTED_DOTENV_TYPES:
        return os.environ[variable_name]

    # If variable type is list, return the string value split by ','.
    if EXPECTED_DOTENV_TYPES[variable_name] is list:
        return os.environ[variable_name].split(',')

    # If variable type is other (integer or boolean), first get the integer value.
    var_int = int(os.environ[variable_name])
    # Return it straight if int, otherwise typecast it to bool.
    return var_int if EXPECTED_DOTENV_TYPES[variable_name] is int else bool(var_int)