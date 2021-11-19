from unittest import mock, TestCase
from unittest.mock import MagicMock
from lib.mqtt_listener import MQTTListener

class TestMQTTListener(TestCase):


    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.mqtt_client.MQTTClient._connect")
    @mock.patch("lib.mqtt_listener.MQTTListener.subscribe")
    def test_init(self, m_s, m_c, m_eg):
        """lib.mqtt_listener.MQTTListener.__init__"""
        # Side effect method for environment.get
        environ_vars = ['HELLO', 'WHERE', 'IS', 'CARMEN SANDIEGO', ['IM IN', 'A MEETING', 'RIGHT NOW LOL']]
        def environment_get_side_effect(*args, **kwargs):
            var = environ_vars[0]
            environ_vars.remove(var)
            return var
        m_eg.side_effect = environment_get_side_effect

        # Side effect method for MQTTListener.subscribe
        subscribe_called_with = []
        def subscribe_side_effect(*args, **kwargs):
            subscribe_called_with.append(args)
        m_s.side_effect = subscribe_side_effect

        # Create a MagicMock object to act as MQTTSender.client
        client = MagicMock()
        MQTTListener.client = client

        # Run the method
        sender = MQTTListener()

        # Run assertions
        self.assertEqual(sender.client_type, 'MQTTListener')
        m_c.assert_called_with('HELLO', 'WHERE', 'IS', 'CARMEN SANDIEGO')
        self.assertEqual(subscribe_called_with, [('IM IN',), ('A MEETING',), ('RIGHT NOW LOL',)])


    @mock.patch("lib.mqtt_listener.MQTTListener.__init__")
    def test_subscribe(self, m_i):
        """lib.mqtt_listener.MQTTListener.subscribe"""
        # Create thing
        m_i.return_value = None
        listener = MQTTListener()

        # Create subscribe mock
        subscribe_mock = MagicMock()

        # Create mock paho client with subscribe mock and attach to listener
        paho_client_mock = MagicMock()
        paho_client_mock.subscribe = subscribe_mock
        listener.client = paho_client_mock

        # Run method
        listener.subscribe('topic', 40, {'recovery': None}, {'whatever': 'bro'})

        # Run assertions
        subscribe_mock.assert_called_with('topic', 40, {'recovery': None}, {'whatever': 'bro'})


    @mock.patch("lib.authorization_client.AuthorizationClient.handle_message")
    def test_on_message(self, m_hm):
        """lib.mqtt_listener.MQTTListener.on_message"""
        # Run the method
        MQTTListener.on_message('HAM', 'TURKEY', 'CORN')

        # Run assertions
        m_hm.assert_called_with(message='CORN')


# Running part.
if __name__ == '__main__':
    unittest.main()