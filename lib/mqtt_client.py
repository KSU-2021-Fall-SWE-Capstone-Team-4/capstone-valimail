import paho.mqtt.client as mqtt
import logging

class MQTTClient:

    def _connect(self, username, password, hostname, port):
        """
        Connects the MQTT Client to a MQTT Server.
        Acts somewhat as a wrapper for paho.mqtt.client.Client.subscribe.
        After calling this method, self.client will have its attribute set to a paho.mqtt.client.Client instance.

        Arguments:
            username (str) : The username of the account making the connection.
            password (str) : The password of the account making the connection.
            hostname (str) : The hostname of the MQTT server.
            port (int) : The port of the MQTT server.
        """
        # Instantiates the client.
        client = mqtt.Client()

        # If the client doesn't already have a client_type attribute, we add one for it and add the connection callback method.
        if not hasattr(client, 'client_type') and hasattr(self, 'client_type'):
            client.client_type = self.client_type
        client.on_connect = MQTTClient.on_connect

        # Sets the proper protocol, username, password, hostname, and port.
        client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        client.username_pw_set(username, password)

        # Attempts the connection.
        # The client.connect method sets the variables in place so that the connection can be instantiated, but doesn't launch.
        # This is due to the fact that no connection is made until the client is put into a loop.
        # This will be done differently based on what type of MQTTClient is being instantiated, so it's not acted upon here.
        client.connect(hostname, port)

        # Sets the established client to self.client.
        self.client = client

    @staticmethod
    def on_connect(client, user_data, flags, result_code):
        """
        Callback method for initial connection through self.client.
        Used as a static method here so that self.client can use it.
        If any result code other than 0 is received, then the program will exit immediately (critical connection error).

        Arguments:
            client (paho.mqtt.client.Client) : The client calling this method.
            user_data : The user data for the established connection.
            flags (dict) : The flags raised by this connection.
            result_code (int) : The result code returned by this connection. Ideally 0.
        """
        # If the result code is 0, connection was established successfully.
        if result_code == 0:
            logging.info(f'{client.client_type if hasattr(client, "client_type") else "MQTTClient"} connected successfully')
            return

        # Otherwise, connection was unsuccessful.
        # Result code values are reported as documented in paho.mqtt.client's docstring.
        elif result_code <= 5:
            fail_reasons = {
                1: 'failed to connect due to mismatching protocol versions',
                2: 'failed to connect due to invalid client identifier',
                3: 'failed to connect, server unavailable',
                4: 'failed to connect due to bad username / password',
                5: 'failed to connect, not authorized',
            }
            # Report with a log.
            logging.critical(f'{client.client_type if hasattr(client, "client_type") else "MQTTClient"} {fail_reasons[result_code]}')

        # Other / unknown, log accordingly:
        else:
            logging.critical(f'{client.client_type if hasattr(client, "client_type") else "MQTTClient"} could not connect for unknown reason')

        # Exit with the result_code.
        exit(result_code)