import logging

# Logging format is kept here.
LOGGING_FORMAT = '[%(asctime)s] %(levelname)s: %(message)s'


def basic_setup():
    """
    Performs basic setup for the logging module.
    Sets the logging format and level.
    """
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', level=logging.INFO)


def enable_debug_mode():
    """
    A method to be called when debug mode is enabled.
    Simply changes the logging's level and puts out a debug log.
    """
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug('Debug mode enabled.')