from lib.util import environment
from lib.mqtt_client import MQTTClient
from lib.authorization_client import AuthorizationClient
import logging

class MQTTListener(MQTTClient):

    def __init__(self):
        """
        Initializes the MQTTListener class.
        All variables needed are pulled from .env.
        Sets up the necessary connection, but does not test.
        Subscribes to the necessary topics.
        """
        # Sets the client_type for MQTTClient inherited methods.
        self.client_type = 'MQTTListener'

        # Copy connection environment variables to variables to be used twice.
        mqtt_listener_username = environment.get('MQTT_LISTENER_USERNAME')
        mqtt_listener_password = environment.get('MQTT_LISTENER_PASSWORD')
        mqtt_listener_hostname = environment.get('MQTT_LISTENER_HOSTNAME')
        mqtt_listener_port = environment.get('MQTT_LISTENER_PORT')

        # Use the inherited _connect method to setup the connection.
        logging.info(f'MQTTListener setting connection to {mqtt_listener_hostname}:{mqtt_listener_port} with username {mqtt_listener_username} and password {mqtt_listener_password}')
        self._connect(mqtt_listener_username,
                      mqtt_listener_password,
                      mqtt_listener_hostname,
                      mqtt_listener_port)

        # Set the subscribe and on_message protocols.
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

        # Subscribe to relevant topics.
        for topic in environment.get('MQTT_LISTENER_TOPICS'):
            self.subscribe(topic)

    def begin_listening(self):
        """
        Loops forever (starts the listening loop).
        Required call for actually listening to stuff.
        Acts as a wrapper for paho.mqtt.client.Client.loop_forever.
        This is where the __main__ process ends, since loop_forever should never break UNLESS the timeout was achieved.
        """
        # Log the connection's start.
        logging.info('MQTTListener now connecting...')

        # Start the client loop.
        self.client.loop_forever(timeout=environment.get('MQTT_CLIENT_CONNECTION_TIMEOUT_SECONDS'))

        # If we EVER make it here, it means that the connection timed out, which is a critical error.
        # Exit the program accordingly.
        logging.critical('MQTTListener timed out while connecting')
        exit(-1)

    def subscribe(self, topic, qos=0, options=None, properties=None):
        """
        Subscribes to a topic.
        Acts as a wrapper for paho.mqtt.client.Client.subscribe.

        Arguments:
            topic (str): The topic name.
            qos (int): Desired quality of service level. Defaults to 0.
            options : Currently unknown.
            properties : Currently unknown.
        """
        logging.info(f'MQTTListener subscribing to topic {topic} with QOS {qos}')
        self.client.subscribe(topic, qos, options, properties)

    @staticmethod
    def on_subscribe(client, user_data, mid, granted_qos):
        """
        Callback method for subscription through self.client.
        Used as a static method here so that self.client can use it.

        Arguments:
            client (paho.mqtt.client.Client) : The client calling this method.
            user_data : The user data for the established connection.
            mid : Currently unknown.
            granted_qos (bool) : Whether or not the desired quality of service level has been granted.
        """
        logging.debug(f'Subscribed to mid {mid} with desired QOS {granted_qos}')

    @staticmethod
    def on_message(client, user_data, msg):
        """
        Callback method for receiving a message through self.client.
        Used as a static method here so that self.client can use it.

        Arguments:
            client (paho.mqtt.client.Client) : The client calling this method.
            user_data : The user data for the established connection.
            msg (paho.mqtt.client.MQTTMessage) : The message object.
        """
        AuthorizationClient.handle_message(message=msg)