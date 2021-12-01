from unittest import mock, TestCase
from lib.util import logger


class TestLogger(TestCase):


    @mock.patch("logging.debug")
    def test_enable_debug_mode_can_run_after_basic_setup(self, m_d):
        """lib.util.logger.enable_debug_mode.can_run_after_basic_setup"""
        # Run basic_setup.
        logger.basic_setup()
        # Run enable_debug_mode.
        logger.enable_debug_mode()
