# Only run in main.
if __name__ == '__main__':

    # First things first, launch the logger.
    from lib.util import logger
    logger.basic_setup()

    # Load up the .env variables.
    from lib.util import environment
    environment.load_dotenv()

    # If debug mode is enabled, change the logging level.
    if environment.get('DEBUG'):
        logger.enable_debug_mode()

    # Log the setup 'begin' line.
    logger.log_setup_start_header()

    # Import the AuthorizationClient.
    from lib.authorization_client import AuthorizationClient
    # Initialize the AuthorizationClient (which will, in turn, instantiate the MQTTSender).
    AuthorizationClient.initialize()

    # Import the MQTTListener.
    from lib.mqtt_listener import MQTTListener
    # Instantiate listener.
    listener = MQTTListener()

    # Force listener to loop forever.
    listener.loop_forever()