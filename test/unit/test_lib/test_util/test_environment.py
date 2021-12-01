from lib.util.exceptions import UndefinedVariableError, InvalidDotenvFileError
from unittest import mock, TestCase
from lib.util import environment
import os


class TestEnvironment(TestCase):

    OS_ENVIRON_MOCK =  {
        'MOCK1': 'oh yeah!',
        'MOCK2': 'option1,option2,option3',
        'MOCK3': '123',
        'MOCK4': '1',
        'MOCK5': '0',
    }
    OS_ENVIRON_MOCK_MISSINGONE = {
        'MOCK1': 'oh yeah!',
        'MOCK2': 'option1,option2,option3',
        'MOCK4': '1',
        'MOCK5': '0',
    }
    OS_ENVIRON_MOCK_TYPECHECK_INT = {
        'MOCK1': 'oh yeah!',
        'MOCK2': 'option1,option2,option3',
        'MOCK3': 'oh yeah AGAIN?! thats not right',
        'MOCK4': '1',
        'MOCK5': '0',
    }
    OS_ENVIRON_MOCK_TYPECHECK_BOOL = {
        'MOCK1': 'oh yeah!',
        'MOCK2': 'option1,option2,option3',
        'MOCK3': '123',
        'MOCK4': 'wait no no no STOP THAT',
        'MOCK5': '0',
    }


    @classmethod
    def setUpClass(self):
        """
        Set up class method.
        Creates mock version of the environment's (normally static) dotenv vars and dotenv types.
        """
        environment.EXPECTED_DOTENV_VARS = ['MOCK1', 'MOCK2', 'MOCK3', 'MOCK4', 'MOCK5']
        environment.EXPECTED_DOTENV_TYPES = {
            'MOCK2': list,
            'MOCK3': int,
            'MOCK4': bool,
            'MOCK5': bool
        }


    @mock.patch('os.path.exists')
    @mock.patch('dotenv.load_dotenv')
    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK)
    def test_load_dotenv_nofile(self, m_ld, m_ope):
        """lib.util.environment.load_dotenv.nofile"""
        # Make the os.path.exists method return False
        m_ope.return_value = False

        # Run the load_dotenv method
        with self.assertRaises(InvalidDotenvFileError):
            environment.load_dotenv()

        # Run assertions
        m_ld.assert_not_called()


    @mock.patch('os.path.exists')
    @mock.patch('dotenv.load_dotenv')
    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK_MISSINGONE)
    def test_load_dotenv_missingvar(self, m_ld, m_ope):
        """lib.util.environment.load_dotenv.missingvar"""
        # Make the os.path.exists method return True
        m_ope.return_value = True

        # Run the load_dotenv method
        with self.assertRaises(InvalidDotenvFileError):
            environment.load_dotenv()

        # Run assertions
        m_ld.assert_called()


    @mock.patch('os.path.exists')
    @mock.patch('dotenv.load_dotenv')
    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK)
    def test_load_dotenv_typecheck_pass(self, m_ld, m_ope):
        """lib.util.environment.load_dotenv.typecheck.pass"""
        # Make the os.path.exists method return True
        m_ope.return_value = True

        # Run the load_dotenv method (no assertRaises this time)
        environment.load_dotenv()

        # Run assertions
        m_ld.assert_called()


    @mock.patch('os.path.exists')
    @mock.patch('dotenv.load_dotenv')
    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK_TYPECHECK_INT)
    def test_load_dotenv_typecheck_fail_int(self, m_ld, m_ope):
        """lib.util.environment.load_dotenv.typecheck.fail.int"""
        # Make the os.path.exists method return True
        m_ope.return_value = True

        # Run the load_dotenv method (no assertRaises this time)
        with self.assertRaises(InvalidDotenvFileError):
            environment.load_dotenv()

        # Run assertions
        m_ld.assert_called()


    @mock.patch('os.path.exists')
    @mock.patch('dotenv.load_dotenv')
    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK_TYPECHECK_BOOL)
    def test_load_dotenv_typecheck_fail_bool(self, m_ld, m_ope):
        """lib.util.environment.load_dotenv.typecheck.fail.bool"""
        # Make the os.path.exists method return True
        m_ope.return_value = True

        # Run the load_dotenv method (no assertRaises this time)
        with self.assertRaises(InvalidDotenvFileError):
            environment.load_dotenv()

        # Run assertions
        m_ld.assert_called()


    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK)
    def test_get_str_type(self):
        """lib.util.environment.get.str_type"""
        # Run the get method
        get_val = environment.get('MOCK1')

        # Run assertions
        self.assertEqual(get_val, 'oh yeah!')


    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK)
    def test_get_list_type(self):
        """lib.util.environment.get.list_type"""
        # Run the get method
        get_val = environment.get('MOCK2')

        # Run assertions
        self.assertEqual(get_val, ['option1', 'option2', 'option3'])


    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK)
    def test_get_int_type(self):
        """lib.util.environment.get.int_type"""
        # Run the get method
        get_val = environment.get('MOCK3')

        # Run assertions
        self.assertEqual(get_val, 123)


    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK)
    def test_get_bool_type_true(self):
        """lib.util.environment.get.bool_type.true"""
        # Run the get method
        get_val = environment.get('MOCK4')

        # Run assertions
        self.assertEqual(get_val, True)


    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK)
    def test_get_bool_type_false(self):
        """lib.util.environment.get.bool_type.false"""
        # Run the get method
        get_val = environment.get('MOCK5')

        # Run assertions
        self.assertEqual(get_val, False)


    @mock.patch.object(os, 'environ', OS_ENVIRON_MOCK)
    def test_get_invalid(self):
        """lib.util.environment.get.invalid"""
        # Run the get method
        with self.assertRaises(UndefinedVariableError):
            environment.get('FAKE_MOCK')
