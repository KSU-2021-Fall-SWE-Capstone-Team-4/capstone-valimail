# Only run in main.
if __name__ == '__main__':

    # Load up the .env variables.
    # TODO: Detect when user has not set up .env
    from dotenv import load_dotenv
    load_dotenv(verbose=True)

    # Import the MQTTListener.
    # MQTTListener will import AuthorizationClient, which will create its own MQTTSender.
    from lib.mqtt_listener import MQTTListener

    # Instantiate listener.
    listener = MQTTListener()

    # Force listener to loop forever.
    listener.loop_forever()

