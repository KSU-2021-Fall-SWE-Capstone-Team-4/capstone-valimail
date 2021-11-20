from unittest import mock, TestCase
from unittest.mock import MagicMock
from lib.watchdog import Watchdog
from lib import watchdog
from threading import Thread
from time import sleep

class TestWatchdog(TestCase):


    def test_run_normal_terminate(self):
        """lib.watchdog.Watchdog.run.normal_terminate"""
        # Create method for threading.enumerate.
        TestWatchdog.humor_watchdog_count = 100
        def enumerate_limited():
            TestWatchdog.humor_watchdog_count-= 1
            if TestWatchdog.humor_watchdog_count:
                return ['hello']
            else:
                return []

        # Replace threading in watchdog with our own thing that can be more easily mocked.
        watchdog.threading = MagicMock(enumerate=enumerate_limited, _MainThread=str)

        # Ironically, create a thread to run the test.
        TestWatchdog.watchdog_object = Watchdog()
        def perform_test():
            TestWatchdog.watchdog_object.start()
        # Just in case the test fails, this thread is set to be a daemon thread.
        test_thread = Thread(target=perform_test, daemon=True)
        test_thread.start()

        # Sleep for a short moment
        sleep(0.5)

        # Run asseritions
        self.assertFalse(test_thread.is_alive())


    def test_run_stopping_event(self):
        """lib.watchdog.Watchdog.run.stopping_event"""
        # Create method for threading.enumerate.
        def enumerate_limited():
            return ['hello']

        # Replace threading in watchdog with our own thing that can be more easily mocked.
        watchdog.threading = MagicMock(enumerate=enumerate_limited, _MainThread=str)

        # Ironically, create a thread to run the test.
        TestWatchdog.watchdog_object = Watchdog()
        def perform_test():
            TestWatchdog.watchdog_object.start()
        # Just in case the test fails, this thread is set to be a daemon thread.
        test_thread = Thread(target=perform_test, daemon=True)
        test_thread.start()

        # Sleep for a short moment
        sleep(0.1)

        # Run the emergency_stop method
        TestWatchdog.watchdog_object.emergency_stop()

        # Sleep for a short moment
        sleep(0.1)

        # Run asseritions
        self.assertFalse(test_thread.is_alive())


# Running part.
if __name__ == '__main__':
    unittest.main()