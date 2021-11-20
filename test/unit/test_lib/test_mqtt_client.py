from unittest import mock, TestCase
from unittest.mock import MagicMock
from lib.mqtt_client import MQTTClient
from lib import mqtt_client

class TestMQTTClient(TestCase):


    @mock.patch("paho.mqtt.client")
    def test_connect(self, m_mqtt):
        """lib.mqtt_client.MQTTClient._connect"""
        # Mocking the client part
        client_tls_set_mock = MagicMock()
        client_username_pw_set_mock = MagicMock()
        client_connect_mock = MagicMock()
        client_mock = MagicMock(tls_set=client_tls_set_mock, username_pw_set=client_username_pw_set_mock, connect=client_connect_mock)
        m_mqtt = MockPahoMQTT(client_mock)
        mqtt_client.mqtt = m_mqtt

        # Run the method.
        client = MQTTClient()
        client._connect('user', 'pass', '192.168.0.256', '400')

        # Run assertions
        self.assertEqual(client_mock.on_connect, MQTTClient.on_connect)
        client_tls_set_mock.assert_called_with(tls_version='protocol_tls')
        client_username_pw_set_mock.assert_called_with('user', 'pass')
        client_connect_mock.assert_called_with('192.168.0.256', '400')
        self.assertEqual(client.client, client_mock)


    def test_on_connect_resultcode_zero(self):
        """lib.mqtt_client.MQTTClient.on_connect.resultcode_zero"""
        # Just run to make sure that there's no error.
        MQTTClient.on_connect(MagicMock(), {}, {}, 0)


    def test_on_connect_resultcode_nonzero(self):
        """lib.mqtt_client.MQTTClient.on_connect.resultcode_zero"""
        # Run in a for loop to test a lot of values that are decidedly not 0, and see if it causes an exit.
        for i in range(1, 100):
            with self.assertRaises(SystemExit):
                MQTTClient.on_connect(MagicMock(), {}, {}, i)


class MockPahoMQTT:

    def __init__(self, client):
        """Sets variables used to keep track of method call counts."""
        self.mock_client = client
        self.ssl = MagicMock(PROTOCOL_TLS='protocol_tls')

    def Client(self):
        return self.mock_client


# Running part.
if __name__ == '__main__':
    unittest.main()