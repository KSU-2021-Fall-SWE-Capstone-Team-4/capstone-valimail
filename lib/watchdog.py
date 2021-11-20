from time import sleep
import threading
from threading import Thread

class Watchdog(Thread):

    def __init__(self):
        """
        Initializer for Watchdog thread.
        Sets the stopping_event to False so that it can be set to True later in unit testing.
        """
        Thread.__init__(self)
        self.stopping_event = False

    def run(self):
        """
        Runs the main watchdog loop.
        Does not depend on any class variables or anything, just uses the threading library to keep track
        of which threads are running at what time.
        """
        # The outer loop.
        while True:
            # Sets the value of main_thread_running, which keeps track of whether or not the main thread is, well, running.
            main_thread_running = False
            # Iterate through each thread and make sure that the main thread (MQTTListener) is still going.
            # Iterate through each thread and make sure that the main thread (MQTTListener) is still going.
            for thread in threading.enumerate():
                if type(thread) is threading._MainThread:
                    main_thread_running = True
            # If the main thread ISN'T running, produce a critical error and exit.
            if not main_thread_running:
                logging.critical('Main thread stopped running for some reason, exiting')
                exit(-1)
            # If the stopping event has been set, then stop.
            if self.stopping_event:
                return
            # Sleep for 1 second.
            sleep(1)

    def emergency_stop(self):
        """
        Sets the stopping trigger, which should ideally terminate the loop.
        Used exclusively in unit testing, just in case the test for run() fails.
        """
        self.stopping_event = True