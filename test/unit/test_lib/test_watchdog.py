from unittest import mock, TestCase
from multiprocessing import Process
from unittest.mock import MagicMock
from lib.watchdog import Watchdog
from lib import watchdog
from time import sleep


class TestWatchdog(TestCase):


    def test_run(self):
        """lib.watchdog.Watchdog.run.normal_terminate"""
        # Initialize the subprocess, which will allow us to test for a timeout and avoid the possibility of
        # getting caught in an infinite loop.
        process = Process(target=TestWatchdog.run_process_submethod)
        process.start()

        # Wait for the process to join with a timeout variable.
        process.join(1)

        # Check if the process is still alive (timed out). If so, then kill it and raise an error.
        if process.is_alive():
            process.terminate()
            raise ValueError('Process was still running after expected termination')


    @staticmethod
    def run_process_submethod():
        """
        A submethod that gets run inside of test_run.
        This is the only way that it would work alongside the multiprocessing module.
        This method involves all the data modification, and the other one handles timeout detection.
        """
        # Create method for threading.enumerate.
        TestWatchdog.humor_watchdog_count = 100

        def enumerate_limited():
            TestWatchdog.humor_watchdog_count -= 1
            if TestWatchdog.humor_watchdog_count:
                return ['hello']
            else:
                return []

        # Replace threading in watchdog with our own thing that can be more easily mocked.
        watchdog.threading = MagicMock(enumerate=enumerate_limited, _MainThread=str)
