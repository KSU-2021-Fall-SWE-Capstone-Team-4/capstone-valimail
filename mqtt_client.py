import paho.mqtt.client as mqtt

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
        # Instantiates the client. Adds an on_connect callback method.
        client = mqtt.Client()
        client.on_connect = self.on_connect

        # Sets the proper protocol, username, password, hostname, and port.
        # client.connect also makes the connection.
        client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        client.username_pw_set(username, password)
        client.connect(hostname, port)

        # Sets the established client to self.client.
        self.client = client

    @staticmethod
    def on_connect(client, user_data, flags, result_code):
        """
        Callback method for initial connection through self.client.
        Used as a static method here so that self.client can use it.

        Arguments:
            client (paho.mqtt.client.Client) : The client calling this method.
            user_data : The user data for the established connection.
            flags (dict) : The flags raised by this connection.
            result_code (int) : The result code returned by this connection. Ideally 0.
        """
        # If the result code is 0, connection was established successfully.
        if result_code == 0:
            print('Connection successful')
        # Otherwise, connection was unsuccessful.
        else:
            print(f'RESULT CODE {str(result_code)}')