import os
from lib.mqtt_client import MQTTClient

class MQTTSender(MQTTClient):

    def __init__(self):
        """
        Initializes the MQTTListener class.
        All variables needed are pulled from config.py.
        """
        # Perform the initial connection.
        self._connect(os.environ['MQTT_SENDER_USERNAME'],
                      os.environ['MQTT_SENDER_PASSWORD'],
                      os.environ['MQTT_SENDER_HOSTNAME'],
                      int(os.environ['MQTT_SENDER_PORT']))
        self.client.on_publish = self.on_publish

        # Instantiate the topics list, which will keep track of all the topics this sender sends to.
        self.topics = []
        for topic in os.environ['MQTT_SENDER_TOPICS'].split(','):
            self.topics.append(topic)

    def publish(self, payload, qos=0, retain=False, properties=None):
        """
        Publishes a message to a predetermined list of topics.
        Acts as a wrapper for the _publish method.

        Arguments:
            payload (bytes): The payload.
            qos (int): Desired quality of service level. Defaults to 0.
            retain (bool): Whether or not this message should be retained.
            properties : Currently unknown.
        """
        for topic in self.topics:
            self._publish(topic=topic, payload=payload, qos=qos, retain=retain, properties=properties)

    def _publish(self, topic, payload, qos=0, retain=False, properties=None):
        """
        Publishes a message to a topic.
        Acts as a wrapper for paho.mqtt.client.Client.publish.

        Arguments:
            topic (str): The topic name.
            payload (bytes): The payload.
            qos (int): Desired quality of service level. Defaults to 0.
            retain (bool): Whether or not this message should be retained.
            properties : Currently unknown.
        """
        self.client.publish(topic, payload, qos, retain, properties)

    @staticmethod
    def on_publish(client, user_data, mid):
        """
        Callback method for receiving a message through self.client.
        Used as a static method here so that self.client can use it.

        Arguments:
            client (paho.mqtt.client.Client) : The client calling this method.
            user_data : The user data for the established connection.
            mid : Currently unknown.
        """
        print("mid: " + str(mid))