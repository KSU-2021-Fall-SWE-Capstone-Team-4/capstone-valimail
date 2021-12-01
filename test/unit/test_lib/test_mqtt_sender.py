from unittest import mock, TestCase
from unittest.mock import MagicMock
from lib.mqtt_sender import MQTTSender


class TestMQTTSender(TestCase):


    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.mqtt_client.MQTTClient._connect")
    @mock.patch("lib.mqtt_sender.MQTTSender.test_connection")
    def test_init(self, m_tc, m_c, m_eg):
        """lib.mqtt_sender.MQTTSender.__init__"""
        # Side effect method for environment.get
        environ_vars = ['HELLO', 'WHERE', 'IS', 'CARMEN SANDIEGO', ['IM IN', 'A MEETING', 'RIGHT NOW LOL']]
        def environment_get_side_effect(*args, **kwargs):
            var = environ_vars[0]
            environ_vars.remove(var)
            return var
        m_eg.side_effect = environment_get_side_effect

        # Create a MagicMock object to act as MQTTSender.client
        client = MagicMock()
        MQTTSender.client = client

        # Run the method
        sender = MQTTSender()

        # Run assertions
        self.assertEqual(sender.client_type, 'MQTTSender')
        m_c.assert_called_with('HELLO', 'WHERE', 'IS', 'CARMEN SANDIEGO')
        m_tc.assert_called_once()
        self.assertEqual(sender.topics, ['IM IN', 'A MEETING', 'RIGHT NOW LOL'])


    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.mqtt_sender.MQTTSender.__init__")
    @mock.patch("time.sleep")
    def test_test_connection_pass(self, m_ts, m_i, m_eg):
        """lib.mqtt_sender.MQTTSender.test_connection.pass"""
        # Set return value for environment.get
        sleep_count = 100
        m_eg.return_value = sleep_count

        # Create thing
        m_i.return_value = None
        sender = MQTTSender()

        # Create mock paho client
        paho_client_mock = MockPahoClient(True)
        sender.client = paho_client_mock

        # Run the method
        sender.test_connection()

        # Run assertions
        self.assertEqual(paho_client_mock.loop_start_call_count, 1)
        self.assertTrue(paho_client_mock.is_connected_call_count < sleep_count)
        self.assertEqual(paho_client_mock.loop_stop_call_count, 1)


    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.mqtt_sender.MQTTSender.__init__")
    @mock.patch("time.sleep")
    @mock.patch("logging.critical")
    def test_test_connection_timeout(self, m_lc, m_ts, m_i, m_eg):
        """lib.mqtt_sender.MQTTSender.test_connection.timeout"""
        # Set return value for environment.get
        sleep_count = 100
        m_eg.return_value = sleep_count

        # Create thing
        m_i.return_value = None
        sender = MQTTSender()

        # Create mock paho client
        paho_client_mock = MockPahoClient(False)
        sender.client = paho_client_mock

        # Run the method
        with self.assertRaises(SystemExit):
            sender.test_connection()

        # Run assertions
        self.assertEqual(paho_client_mock.loop_start_call_count, 1)
        self.assertTrue(paho_client_mock.is_connected_call_count > sleep_count)
        self.assertEqual(paho_client_mock.loop_stop_call_count, 0)


    @mock.patch("lib.mqtt_sender.MQTTSender.__init__")
    @mock.patch("lib.mqtt_sender.MQTTSender._publish")
    def test_publish(self, m_p, m_i):
        """lib.mqtt_sender.MQTTSender.publish"""
        # Side effect method for MQTTClient._publish
        publish_called_with = []
        def publish_side_effect(*args, **kwargs):
            publish_called_with.append(kwargs)
        m_p.side_effect = publish_side_effect

        # Create thing
        m_i.return_value = None
        sender = MQTTSender()

        # Set the thing's topics
        sender.topics = ['watch', 'and', 'learn']

        # Run the method
        sender.publish('message', 10, True, {'property': 'smooth'})

        # Run assertions
        self.assertEqual(publish_called_with[0], {'topic': 'watch', 'payload': 'message', 'qos': 10, 'retain': True, 'properties': {'property': 'smooth'}})
        self.assertEqual(publish_called_with[1], {'topic': 'and', 'payload': 'message', 'qos': 10, 'retain': True, 'properties': {'property': 'smooth'}})
        self.assertEqual(publish_called_with[2], {'topic': 'learn', 'payload': 'message', 'qos': 10, 'retain': True, 'properties': {'property': 'smooth'}})


class MockPahoClient:

    def __init__(self, connected_val):
        """Sets variables used to keep track of method call counts."""
        self.loop_start_call_count = 0
        self.is_connected_call_count = 0
        self.loop_stop_call_count = 0
        self.connected_val = connected_val

    def loop_start(self, *args, **kwargs):
        self.loop_start_call_count += 1

    def is_connected(self, *args, **kwargs):
        self.is_connected_call_count += 1
        return self.connected_val

    def loop_stop(self, *args, **kwargs):
        self.loop_stop_call_count += 1
