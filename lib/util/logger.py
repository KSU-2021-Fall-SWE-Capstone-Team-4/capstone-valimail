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
    Simply changes the logging's level + format and puts out a debug log.
    """
    # Set the logging level.
    logging.getLogger().setLevel(logging.DEBUG)
    # Set the logging format to include thread id.
    for handler in logging.getLogger().handlers:
        handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s (Thread %(thread)d): %(message)s'))
    # Log that debug mode is enabled.
    logging.debug('Debug mode enabled.')

def log_setup_start_header():
    """
    A simple method that logs a line defining where setup begins.
    """
    logging.info('==========================================================SETUP BEGIN==========================================================')

def log_setup_end_header():
    """
    A simple method that logs a line defining where setup ends.
    """
    logging.info('===========================================================SETUP END===========================================================')