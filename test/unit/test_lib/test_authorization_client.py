from unittest import mock, TestCase
from unittest.mock import MagicMock
from lib.authorization_client import AuthorizationClient
from lib.mqtt_sender import MQTTSender
from lib.util import logger
from json import JSONDecodeError
from dane_discovery.exceptions import TLSAError
from binascii import Error as ASCIIError


class TestAuthorizationClient(TestCase):


    @mock.patch("threading.Thread.__init__")
    def test_init(self, m_i):
        """lib.authorization_client.AuthorizationClient.__init__"""
        # Set return value to None so as to not cause errors
        m_i.return_value = None

        # Run the method
        auth_client = AuthorizationClient('my time')

        # Run assertions
        self.assertEqual(auth_client.message, 'my time')
        m_i.assert_called()


    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.util.logger.log_setup_end_header")
    @mock.patch("lib.authorization_client.AuthorizationClient.authorized")
    @mock.patch("lib.authorization_client.AuthorizationClient.__init__")
    def test_run_fail_auth(self, m_i, m_a, m_lseh, m_eg):
        """lib.authorization_client.AuthorizationClient.run.fail_auth"""
        # Set return value for environment.get and AuthorizationClient.authorized
        m_eg.return_value = True
        m_a.return_value = False, None

        # Create thing
        m_i.return_value = None
        auth_client = AuthorizationClient('fake_message')

        # Create mock paho message and attach to auth client
        mock_paho_message = MagicMock(topic='test_topic', payload='unrealistically_readable_payload')
        auth_client.message = mock_paho_message

        # Create mock listener with publish mock and attach to AuthorizationClient
        publish = MagicMock()
        sender = MagicMock(publish=publish)
        AuthorizationClient.sender = sender

        # Run method
        auth_client.run()

        # Run assertions
        m_a.assert_called_with(mock_paho_message)
        m_eg.assert_not_called()
        publish.assert_not_called()

    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.util.logger.log_setup_end_header")
    @mock.patch("lib.authorization_client.AuthorizationClient.authorized")
    @mock.patch("lib.authorization_client.AuthorizationClient.__init__")
    def test_run_pass_auth_no_send(self, m_i, m_a, m_lseh, m_eg):
        """lib.authorization_client.AuthorizationClient.run.pass_auth.no_send"""
        # Set return value for environment.get and AuthorizationClient.authorized
        m_eg.return_value = True
        m_a.return_value = True, None

        # Create thing
        m_i.return_value = None
        auth_client = AuthorizationClient('fake_message')

        # Create MockPahoMessage and attach to auth client
        mock_paho_message = MagicMock(topic='test_topic', payload='unrealistically_readable_payload')
        auth_client.message = mock_paho_message

        # Create mock listener with publish mock and attach to AuthorizationClient
        publish = MagicMock()
        sender = MagicMock(publish=publish)
        AuthorizationClient.sender = sender

        # Run method
        auth_client.run()

        # Run assertions
        m_a.assert_called_with(mock_paho_message)
        m_eg.assert_called_with('DISABLE_SENDER')
        publish.assert_not_called()

    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.util.logger.log_setup_end_header")
    @mock.patch("lib.authorization_client.AuthorizationClient.authorized")
    @mock.patch("lib.authorization_client.AuthorizationClient.__init__")
    def test_run_pass_auth_yes_send(self, m_i, m_a, m_lseh, m_eg):
        """lib.authorization_client.AuthorizationClient.run.pass_auth.yes_send"""
        # Set return value for environment.get and AuthorizationClient.authorized
        m_eg.return_value = False
        m_a.return_value = True, None

        # Create thing
        m_i.return_value = None
        auth_client = AuthorizationClient('fake_message')

        # Create MockPahoMessage and attach to auth client
        mock_paho_message = MagicMock(topic='test_topic', payload='unrealistically_readable_payload')
        auth_client.message = mock_paho_message

        # Create mock listener with publish mock and attach to AuthorizationClient
        publish = MagicMock()
        sender = MagicMock(publish=publish)
        AuthorizationClient.sender = sender

        # Run method
        auth_client.run()

        # Run assertions
        m_a.assert_called_with(mock_paho_message)
        m_eg.assert_called_with('DISABLE_SENDER')
        publish.assert_called_with(mock_paho_message.payload)


    @mock.patch("lib.mqtt_sender.MQTTSender.__init__")
    def test_initialize_no_attr(self, m_i):
        """lib.authorization_client.AuthorizationClient.no_attr"""
        # Set return value to None so as to not cause errors
        m_i.return_value = None

        # Make sure that AuthorizationClient does not have the 'initialized' attribute
        if hasattr(AuthorizationClient, 'initialized'):
            delattr(AuthorizationClient, 'initialized')
        # Make sure that AuthorizationClient does not have a sender
        if hasattr(AuthorizationClient, 'sender'):
            delattr(AuthorizationClient, 'sender')

        # Run the method
        AuthorizationClient.initialize()

        # Run assertions
        m_i.assert_called()
        self.assertIsInstance(AuthorizationClient.sender, MQTTSender)


    @mock.patch("lib.mqtt_sender.MQTTSender.__init__")
    def test_initialize_attr_false(self, m_i):
        """lib.authorization_client.AuthorizationClient.attr_false"""
        # Set return value to None so as to not cause errors
        m_i.return_value = None

        # Make sure that AuthorizationClient's 'initialized' attribute is set to False
        AuthorizationClient.initialized = False
        # Make sure that AuthorizationClient does not have a sender
        if hasattr(AuthorizationClient, 'sender'):
            delattr(AuthorizationClient, 'sender')

        # Run the method
        AuthorizationClient.initialize()

        # Run assertions
        m_i.assert_called()
        self.assertIsInstance(AuthorizationClient.sender, MQTTSender)


    @mock.patch("lib.mqtt_sender.MQTTSender.__init__")
    def test_initialize_attr_true(self, m_i):
        """lib.authorization_client.AuthorizationClient.attr_true"""
        # Set return value to None so as to not cause errors
        m_i.return_value = None

        # Make sure that AuthorizationClient's 'initialized' attribute is set to True
        AuthorizationClient.initialized = True
        # Make sure that AuthorizationClient does not have a sender
        if hasattr(AuthorizationClient, 'sender'):
            delattr(AuthorizationClient, 'sender')

        # Run the method
        AuthorizationClient.initialize()

        # Run assertions
        m_i.assert_not_called()
        self.assertFalse(hasattr(AuthorizationClient, 'sender'))


    @mock.patch("lib.authorization_client.AuthorizationClient.__init__")
    @mock.patch("lib.authorization_client.AuthorizationClient.start")
    def test_handle_message(self, m_s, m_i):
        """lib.authorization_client.AuthorizationClient.handle_message"""
        # Set return value to None so as to not cause errors
        m_i.return_value = None

        # Run the method
        AuthorizationClient.handle_message('DOOR STUCK')

        # Run assertions
        m_i.assert_called_with('DOOR STUCK')
        m_s.assert_called()


    @mock.patch("json.JSONDecodeError.__init__")
    @mock.patch("json.loads")
    @mock.patch("base64.b64decode")
    @mock.patch("dane_jwe_jws.util.Util.get_name_from_dns_uri")
    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout")
    def test_authorized_message_not_json(self, m_vawt, m_eg, m_gnfdi, m_b64d, m_jl, m_i):
        """lib.authorization_client.AuthorizationClient.authorized.message_not_json"""
        # Set return value to None so as to not cause errors
        m_i.return_value = None

        # Set side effect for json.loads
        json_loads_called_with = []
        def json_loads_side_effect(*args, **kwargs):
            json_loads_called_with.append(args)
            raise JSONDecodeError()
        m_jl.side_effect = json_loads_side_effect

        # Set side effect for base64.b64decode
        def base64_b64decode_side_effect(*args, **kwargs):
            raise ASCIIError()
        m_b64d.side_effect = base64_b64decode_side_effect

        # Set side effect for util.get_name_from_dns_uri
        def util_get_name_from_dns_uri_side_effect(*args, **kwargs):
            raise ValueError()
        m_gnfdi.side_effect = util_get_name_from_dns_uri_side_effect

        # Create the starter message
        starter_message = MagicMock(payload='unusually readable payload')

        # Run the method
        authorized, exception = AuthorizationClient.authorized(starter_message)

        # Run assertions (split into parts because there are so many)
        # Return value assertions
        self.assertFalse(authorized)
        self.assertIsInstance(exception, JSONDecodeError)
        # Json loads assertions
        self.assertEqual(len(json_loads_called_with), 1)
        self.assertEqual(json_loads_called_with[0], ('unusually readable payload',))
        # base64.b64decode assertions
        m_b64d.assert_not_called()
        # util.get_name_from_dns_uri assertions
        m_gnfdi.assert_not_called()
        # environment.get assertions
        m_eg.assert_not_called()
        # AuthorizationClient.verify_authentication_with_timeout assertions
        m_vawt.assert_not_called()


    @mock.patch("json.loads")
    @mock.patch("base64.b64decode")
    @mock.patch("dane_jwe_jws.util.Util.get_name_from_dns_uri")
    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout")
    def test_authorized_message_missing_protected(self, m_vawt, m_eg, m_gnfdi, m_b64d, m_jl):
        """lib.authorization_client.AuthorizationClient.authorized.message_missing_protected"""
        # Set side effect for json.loads
        json_loads_called_with = []
        def json_loads_side_effect(*args, **kwargs):
            json_loads_called_with.append(args)
            if len(json_loads_called_with) == 1:
                return {}
            else:
                return 'HOW DID YOU GET THIS FAR SOMETHING WENT WRONG'
        m_jl.side_effect = json_loads_side_effect

        # Set side effect for base64.b64decode
        def base64_b64decode_side_effect(*args, **kwargs):
            raise ASCIIError()
        m_b64d.side_effect = base64_b64decode_side_effect

        # Set side effect for util.get_name_from_dns_uri
        def util_get_name_from_dns_uri_side_effect(*args, **kwargs):
            raise ValueError()
        m_gnfdi.side_effect = util_get_name_from_dns_uri_side_effect

        # Create the starter message
        starter_message = MagicMock(payload='unusually readable payload')

        # Run the method
        authorized, exception = AuthorizationClient.authorized(starter_message)

        # Run assertions (split into parts because there are so many)
        # Return value assertions
        self.assertFalse(authorized)
        self.assertIsInstance(exception, KeyError)
        # Json loads assertions
        self.assertEqual(len(json_loads_called_with), 1)
        self.assertEqual(json_loads_called_with[0], ('unusually readable payload',))
        # base64.b64decode assertions
        m_b64d.assert_not_called()
        # util.get_name_from_dns_uri assertions
        m_gnfdi.assert_not_called()
        # environment.get assertions
        m_eg.assert_not_called()
        # AuthorizationClient.verify_authentication_with_timeout assertions
        m_vawt.assert_not_called()


    @mock.patch("json.loads")
    @mock.patch("base64.b64decode")
    @mock.patch("dane_jwe_jws.util.Util.get_name_from_dns_uri")
    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout")
    def test_authorized_protected_not_b64(self, m_vawt, m_eg, m_gnfdi, m_b64d, m_jl):
        """lib.authorization_client.AuthorizationClient.authorized.protected_not_b64"""
        # Set side effect for json.loads
        json_loads_called_with = []
        def json_loads_side_effect(*args, **kwargs):
            json_loads_called_with.append(args)
            if len(json_loads_called_with) == 1:
                return {'protected': 'asdfghjkl!@#$%^&*()_+-= surely this isnt base64 right oh wait it doesnt matter lol'}
            else:
                return 'HOW DID YOU GET THIS FAR SOMETHING WENT WRONG'
        m_jl.side_effect = json_loads_side_effect

        # Set side effect for base64.b64decode
        def base64_b64decode_side_effect(*args, **kwargs):
            raise ASCIIError()
        m_b64d.side_effect = base64_b64decode_side_effect

        # Set side effect for util.get_name_from_dns_uri
        def util_get_name_from_dns_uri_side_effect(*args, **kwargs):
            raise ValueError()
        m_gnfdi.side_effect = util_get_name_from_dns_uri_side_effect

        # Create the starter message
        starter_message = MagicMock(payload='unusually readable payload')

        # Run the method
        authorized, exception = AuthorizationClient.authorized(starter_message)

        # Run assertions (split into parts because there are so many)
        # Return value assertions
        self.assertFalse(authorized)
        self.assertIsInstance(exception, ASCIIError)
        # Json loads assertions
        self.assertEqual(len(json_loads_called_with), 1)
        self.assertEqual(json_loads_called_with[0], ('unusually readable payload',))
        # base64.b64decode assertions
        m_b64d.assert_called_with('asdfghjkl!@#$%^&*()_+-= surely this isnt base64 right oh wait it doesnt matter lol')
        # util.get_name_from_dns_uri assertions
        m_gnfdi.assert_not_called()
        # environment.get assertions
        m_eg.assert_not_called()
        # AuthorizationClient.verify_authentication_with_timeout assertions
        m_vawt.assert_not_called()


    @mock.patch("json.JSONDecodeError.__init__")
    @mock.patch("json.loads")
    @mock.patch("base64.b64decode")
    @mock.patch("dane_jwe_jws.util.Util.get_name_from_dns_uri")
    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout")
    def test_authorized_protected_not_dict(self, m_vawt, m_eg, m_gnfdi, m_b64d, m_jl, m_i):
        """lib.authorization_client.AuthorizationClient.authorized.protected_not_dict"""
        # Set return value to None so as to not cause errors
        m_i.return_value = None

        # Set side effect for json.loads
        json_loads_called_with = []
        def json_loads_side_effect(*args, **kwargs):
            json_loads_called_with.append(args)
            if len(json_loads_called_with) == 1:
                return {'protected': 'now it is base64 :) <- well not ACTUALLY but you get it'}
            else:
                raise JSONDecodeError()
        m_jl.side_effect = json_loads_side_effect

        # Set return value for base64.b64decode
        m_b64d.return_value = 'NOT A DICT, HAHA'

        # Set side effect for util.get_name_from_dns_uri
        def util_get_name_from_dns_uri_side_effect(*args, **kwargs):
            raise ValueError()
        m_gnfdi.side_effect = util_get_name_from_dns_uri_side_effect

        # Create the starter message
        starter_message = MagicMock(payload='unusually readable payload')

        # Run the method
        authorized, exception = AuthorizationClient.authorized(starter_message)

        # Run assertions (split into parts because there are so many)
        # Return value assertions
        self.assertFalse(authorized)
        self.assertIsInstance(exception, JSONDecodeError)
        # Json loads assertions
        self.assertEqual(len(json_loads_called_with), 2)
        self.assertEqual(json_loads_called_with[0], ('unusually readable payload',))
        self.assertEqual(json_loads_called_with[1], ('NOT A DICT, HAHA',))
        # base64.b64decode assertions
        m_b64d.assert_called_with('now it is base64 :) <- well not ACTUALLY but you get it')
        # util.get_name_from_dns_uri assertions
        m_gnfdi.assert_not_called()
        # environment.get assertions
        m_eg.assert_not_called()
        # AuthorizationClient.verify_authentication_with_timeout assertions
        m_vawt.assert_not_called()


    @mock.patch("json.loads")
    @mock.patch("base64.b64decode")
    @mock.patch("dane_jwe_jws.util.Util.get_name_from_dns_uri")
    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout")
    def test_authorized_protected_missing_x5u(self, m_vawt, m_eg, m_gnfdi, m_b64d, m_jl):
        """lib.authorization_client.AuthorizationClient.authorized.protected_missing_x5u"""
        # Set side effect for json.loads
        json_loads_called_with = []
        def json_loads_side_effect(*args, **kwargs):
            json_loads_called_with.append(args)
            return {'protected': 'now it is base64 :) <- well not ACTUALLY but you get it'} if len(json_loads_called_with) == 1 else {}
        m_jl.side_effect = json_loads_side_effect

        # Set return value for base64.b64decode
        m_b64d.return_value = 'Pretend this is a dict. shhh!'

        # Set side effect for util.get_name_from_dns_uri
        def util_get_name_from_dns_uri_side_effect(*args, **kwargs):
            raise ValueError()
        m_gnfdi.side_effect = util_get_name_from_dns_uri_side_effect

        # Create the starter message
        starter_message = MagicMock(payload='unusually readable payload')

        # Run the method
        authorized, exception = AuthorizationClient.authorized(starter_message)

        # Run assertions (split into parts because there are so many)
        # Return value assertions
        self.assertFalse(authorized)
        self.assertIsInstance(exception, KeyError)
        # Json loads assertions
        self.assertEqual(len(json_loads_called_with), 2)
        self.assertEqual(json_loads_called_with[0], ('unusually readable payload',))
        self.assertEqual(json_loads_called_with[1], ('Pretend this is a dict. shhh!',))
        # base64.b64decode assertions
        m_b64d.assert_called_with('now it is base64 :) <- well not ACTUALLY but you get it')
        # util.get_name_from_dns_uri assertions
        m_gnfdi.assert_not_called()
        # environment.get assertions
        m_eg.assert_not_called()
        # AuthorizationClient.verify_authentication_with_timeout assertions
        m_vawt.assert_not_called()


    @mock.patch("json.loads")
    @mock.patch("base64.b64decode")
    @mock.patch("dane_jwe_jws.util.Util.get_name_from_dns_uri")
    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout")
    def test_authorized_x5u_formatted_wrong(self, m_vawt, m_eg, m_gnfdi, m_b64d, m_jl):
        """lib.authorization_client.AuthorizationClient.authorized.x5u_formatted_wrong"""
        # Set side effect for json.loads
        json_loads_called_with = []
        def json_loads_side_effect(*args, **kwargs):
            json_loads_called_with.append(args)
            return {'protected': 'now it is base64 :) <- well not ACTUALLY but you get it'} if len(json_loads_called_with) == 1 else {'x5u': 'this line is really long'}
        m_jl.side_effect = json_loads_side_effect

        # Set return value for base64.b64decode
        m_b64d.return_value = 'Pretend this is a dict. shhh!'

        # Set side effect for util.get_name_from_dns_uri
        def util_get_name_from_dns_uri_side_effect(*args, **kwargs):
            raise ValueError()
        m_gnfdi.side_effect = util_get_name_from_dns_uri_side_effect

        # Create the starter message
        starter_message = MagicMock(payload='unusually readable payload')

        # Run the method
        authorized, exception = AuthorizationClient.authorized(starter_message)

        # Run assertions (split into parts because there are so many)
        # Return value assertions
        self.assertFalse(authorized)
        self.assertIsInstance(exception, ValueError)
        # Json loads assertions
        self.assertEqual(len(json_loads_called_with), 2)
        self.assertEqual(json_loads_called_with[0], ('unusually readable payload',))
        self.assertEqual(json_loads_called_with[1], ('Pretend this is a dict. shhh!',))
        # base64.b64decode assertions
        m_b64d.assert_called_with('now it is base64 :) <- well not ACTUALLY but you get it')
        # util.get_name_from_dns_uri assertions
        m_gnfdi.assert_called_with('this line is really long')
        # environment.get assertions
        m_eg.assert_not_called()
        # AuthorizationClient.verify_authentication_with_timeout assertions
        m_vawt.assert_not_called()


    @mock.patch("json.loads")
    @mock.patch("base64.b64decode")
    @mock.patch("dane_jwe_jws.util.Util.get_name_from_dns_uri")
    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout")
    def test_authorized_dns_name_not_whitelisted(self, m_vawt, m_eg, m_gnfdi, m_b64d, m_jl):
        """lib.authorization_client.AuthorizationClient.authorized.dns_name_not_whitelisted"""
        # Set side effect for json.loads
        json_loads_called_with = []
        def json_loads_side_effect(*args, **kwargs):
            json_loads_called_with.append(args)
            return {'protected': 'now it is base64 :) <- well not ACTUALLY but you get it'} if len(json_loads_called_with) == 1 else {'x5u': 'this line is really long'}
        m_jl.side_effect = json_loads_side_effect

        # Set return value for base64.b64decode, util.get_name_from_dns_uri, and environment.get
        m_b64d.return_value = 'Pretend this is a dict. shhh!'
        m_gnfdi.return_value = 'WHAT you gotta be kidding me whaddya mean im not on the list'
        m_eg.return_value = ['sorry pal youre not on the list']

        # Create the starter message
        starter_message = MagicMock(payload='unusually readable payload')

        # Run the method
        authorized, exception = AuthorizationClient.authorized(starter_message)

        # Run assertions (split into parts because there are so many)
        # Return value assertions
        self.assertFalse(authorized)
        self.assertIsNone(exception)
        # Json loads assertions
        self.assertEqual(len(json_loads_called_with), 2)
        self.assertEqual(json_loads_called_with[0], ('unusually readable payload',))
        self.assertEqual(json_loads_called_with[1], ('Pretend this is a dict. shhh!',))
        # base64.b64decode assertions
        m_b64d.assert_called_with('now it is base64 :) <- well not ACTUALLY but you get it')
        # util.get_name_from_dns_uri assertions
        m_gnfdi.assert_called_with('this line is really long')
        # environment.get assertions
        m_eg.assert_called_with("DNS_WHITELIST")
        # AuthorizationClient.verify_authentication_with_timeout assertions
        m_vawt.assert_not_called()


    @mock.patch("json.loads")
    @mock.patch("base64.b64decode")
    @mock.patch("dane_jwe_jws.util.Util.get_name_from_dns_uri")
    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout")
    def test_authorized_not_verified(self, m_vawt, m_eg, m_gnfdi, m_b64d, m_jl):
        """lib.authorization_client.AuthorizationClient.authorized.not_verified"""
        # Set side effect for json.loads
        json_loads_called_with = []
        def json_loads_side_effect(*args, **kwargs):
            json_loads_called_with.append(args)
            return {'protected': 'now it is base64 :) <- well not ACTUALLY but you get it'} if len(json_loads_called_with) == 1 else {'x5u': 'this line is really long'}
        m_jl.side_effect = json_loads_side_effect

        # Set return value for base64.b64decode, util.get_name_from_dns_uri, environment.get, and AuthorizationClient.verify_authentication_with_timeout
        m_b64d.return_value = 'Pretend this is a dict. shhh!'
        m_gnfdi.return_value = 'jerry'
        m_eg.return_value = ['OH WAIT YOU ARE ON THE LIST', 'jerry', 'right this way sir have a nice time']
        m_vawt.return_value = False

        # Create the starter message
        starter_message = MagicMock(payload='unusually readable payload')

        # Run the method
        authorized, exception = AuthorizationClient.authorized(starter_message)

        # Run assertions (split into parts because there are so many)
        # Return value assertions
        self.assertFalse(authorized)
        self.assertIsNone(exception)
        # Json loads assertions
        self.assertEqual(len(json_loads_called_with), 2)
        self.assertEqual(json_loads_called_with[0], ('unusually readable payload',))
        self.assertEqual(json_loads_called_with[1], ('Pretend this is a dict. shhh!',))
        # base64.b64decode assertions
        m_b64d.assert_called_with('now it is base64 :) <- well not ACTUALLY but you get it')
        # util.get_name_from_dns_uri assertions
        m_gnfdi.assert_called_with('this line is really long')
        # environment.get assertions
        m_eg.assert_called_with("DNS_WHITELIST")
        # AuthorizationClient.verify_authentication_with_timeout assertions
        m_vawt.assert_called_with('unusually readable payload', 'jerry')


    @mock.patch("json.loads")
    @mock.patch("base64.b64decode")
    @mock.patch("dane_jwe_jws.util.Util.get_name_from_dns_uri")
    @mock.patch("lib.util.environment.get")
    @mock.patch("lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout")
    def test_authorized_passed_everything(self, m_vawt, m_eg, m_gnfdi, m_b64d, m_jl):
        """lib.authorization_client.AuthorizationClient.authorized.passed_everything"""
        # Set side effect for json.loads
        json_loads_called_with = []
        def json_loads_side_effect(*args, **kwargs):
            json_loads_called_with.append(args)
            return {'protected': 'now it is base64 :) <- well not ACTUALLY but you get it'} if len(json_loads_called_with) == 1 else {'x5u': 'this line is really long'}
        m_jl.side_effect = json_loads_side_effect

        # Set return value for base64.b64decode, util.get_name_from_dns_uri, environment.get, and AuthorizationClient.verify_authentication_with_timeout
        m_b64d.return_value = 'Pretend this is a dict. shhh!'
        m_gnfdi.return_value = 'jerry'
        m_eg.return_value = ['OH WAIT YOU ARE ON THE LIST', 'jerry', 'right this way sir have a nice time']
        m_vawt.return_value = True

        # Create the starter message
        starter_message = MagicMock(payload='unusually readable payload')

        # Run the method
        authorized, exception = AuthorizationClient.authorized(starter_message)

        # Run assertions (split into parts because there are so many)
        # Return value assertions
        self.assertTrue(authorized)
        self.assertIsNone(exception)
        # Json loads assertions
        self.assertEqual(len(json_loads_called_with), 2)
        self.assertEqual(json_loads_called_with[0], ('unusually readable payload',))
        self.assertEqual(json_loads_called_with[1], ('Pretend this is a dict. shhh!',))
        # base64.b64decode assertions
        m_b64d.assert_called_with('now it is base64 :) <- well not ACTUALLY but you get it')
        # util.get_name_from_dns_uri assertions
        m_gnfdi.assert_called_with('this line is really long')
        # environment.get assertions
        m_eg.assert_called_with("DNS_WHITELIST")
        # AuthorizationClient.verify_authentication_with_timeout assertions
        m_vawt.assert_called_with('unusually readable payload', 'jerry')


    @mock.patch("lib.util.environment.get")
    @mock.patch("multiprocessing.get_context")
    @mock.patch("threading.get_ident")
    def test_verify_authentication_with_timeout_timeout(self, m_gi, m_gc, m_eg):
        """lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout.timeout"""
        # Set up complicated multiprocessing mocking for each function call
        queue_get_mock = MagicMock(return_value='what')
        queue_mock = MagicMock(get=queue_get_mock)
        process_start_mock = MagicMock()
        process_join_mock = MagicMock()
        process_terminate_mock = MagicMock()
        process_is_alive_mock = MagicMock(return_value=True)
        process_mock = MagicMock(start=process_start_mock, join=process_join_mock, is_alive=process_is_alive_mock, terminate=process_terminate_mock)
        mock_multiprocessing_context = MockMultiprocessingContext(queue_mock, process_mock)
        m_gc.return_value = mock_multiprocessing_context

        # Mock environment.get and threading.get_ident
        m_eg.return_value = 10
        m_gi.return_value = 300

        # Run the method.
        verified = AuthorizationClient.verify_authentication_with_timeout('unusually readable payload', 'dns_name')

        # Run assertions
        m_gc.assert_called_with('spawn')
        self.assertEqual(len(mock_multiprocessing_context.queue_called_with), 1)
        self.assertEqual(len(mock_multiprocessing_context.process_called_with), 1)
        self.assertEqual(mock_multiprocessing_context.process_called_with[0], {'target': AuthorizationClient._authorize, 'args': (queue_mock, 'unusually readable payload', 300)})
        process_start_mock.assert_called()
        process_join_mock.assert_called_with(10)
        process_is_alive_mock.assert_called()
        process_terminate_mock.assert_called()
        queue_get_mock.assert_not_called()
        self.assertFalse(verified)


    @mock.patch("lib.util.environment.get")
    @mock.patch("multiprocessing.get_context")
    @mock.patch("threading.get_ident")
    def test_verify_authentication_with_timeout_success(self, m_gi, m_gc, m_eg):
        """lib.authorization_client.AuthorizationClient.verify_authentication_with_timeout.success"""
        # Set up complicated multiprocessing mocking for each function call
        queue_get_mock = MagicMock(return_value='what')
        queue_mock = MagicMock(get=queue_get_mock)
        process_start_mock = MagicMock()
        process_join_mock = MagicMock()
        process_terminate_mock = MagicMock()
        process_is_alive_mock = MagicMock(return_value=False)
        process_mock = MagicMock(start=process_start_mock, join=process_join_mock, is_alive=process_is_alive_mock, terminate=process_terminate_mock)
        mock_multiprocessing_context = MockMultiprocessingContext(queue_mock, process_mock)
        m_gc.return_value = mock_multiprocessing_context

        # Mock environment.get and threading.get_ident
        m_eg.return_value = 10
        m_gi.return_value = 300

        # Run the method.
        verified = AuthorizationClient.verify_authentication_with_timeout('unusually readable payload', 'dns_name')

        # Run assertions
        m_gc.assert_called_with('spawn')
        self.assertEqual(len(mock_multiprocessing_context.queue_called_with), 1)
        self.assertEqual(len(mock_multiprocessing_context.process_called_with), 1)
        self.assertEqual(mock_multiprocessing_context.process_called_with[0], {'target': AuthorizationClient._authorize, 'args': (queue_mock, 'unusually readable payload', 300)})
        process_start_mock.assert_called()
        process_join_mock.assert_called_with(10)
        process_is_alive_mock.assert_called()
        process_terminate_mock.assert_not_called()
        queue_get_mock.assert_called()
        self.assertEqual(verified, 'what')


    @mock.patch("dane_jwe_jws.authentication.Authentication.verify")
    @mock.patch("lib.util.logger.log_outside_main_process")
    def test_authorize_pass(self, m_lomp, m_v):
        """lib.authorization_client.AuthorizationClient._authorize.pass"""
        # Create mock for queue
        queue_put_mock = MagicMock()
        queue_mock = MagicMock(put=queue_put_mock)

        # Run the method.
        AuthorizationClient._authorize(queue_mock, 'unusually readable payload', 3)

        # Run assertions
        m_v.assert_called_with('unusually readable payload')
        queue_put_mock.assert_called_with(True)


    @mock.patch("dane_discovery.exceptions.TLSAError.__init__")
    @mock.patch("dane_jwe_jws.authentication.Authentication.verify")
    @mock.patch("lib.util.logger.log_outside_main_process")
    def test_authorize_fail_tlsa(self, m_lomp, m_v, m_i):
        """lib.authorization_client.AuthorizationClient._authorize.fail_tlsa"""
        # Set return value to None so as to not cause errors
        m_i.return_value = None

        # Set side effect for Authentication.verify
        def authentication_verify_side_effect(*args, **kwargs):
            raise TLSAError()
        m_v.side_effect = authentication_verify_side_effect

        # Create mock for queue
        queue_put_mock = MagicMock()
        queue_mock = MagicMock(put=queue_put_mock)

        # Run the method.
        AuthorizationClient._authorize(queue_mock, 'unusually readable payload', 3)

        # Run assertions
        m_v.assert_called_with('unusually readable payload')
        queue_put_mock.assert_called_with(False)


    @mock.patch("dane_discovery.exceptions.TLSAError.__init__")
    @mock.patch("dane_jwe_jws.authentication.Authentication.verify")
    @mock.patch("lib.util.logger.log_outside_main_process")
    def test_authorize_fail_unexpected(self, m_lomp, m_v, m_i):
        """lib.authorization_client.AuthorizationClient._authorize.fail_unexpected"""
        # Set return value to None so as to not cause errors
        m_i.return_value = None

        # Set side effect for Authentication.verify
        def authentication_verify_side_effect(*args, **kwargs):
            raise Exception()
        m_v.side_effect = authentication_verify_side_effect

        # Create mock for queue
        queue_put_mock = MagicMock()
        queue_mock = MagicMock(put=queue_put_mock)

        # Run the method.
        AuthorizationClient._authorize(queue_mock, 'unusually readable payload', 3)

        # Run assertions
        m_v.assert_called_with('unusually readable payload')
        queue_put_mock.assert_called_with(False)


class MockMultiprocessingContext:

    def __init__(self, queue_mock, process_mock):
        self.queue_mock = queue_mock
        self.process_mock = process_mock
        self.queue_called_with = []
        self.process_called_with = []

    def Queue(self, **kwargs):
        self.queue_called_with.append(kwargs)
        return self.queue_mock

    def Process(self, **kwargs):
        self.process_called_with.append(kwargs)
        return self.process_mock