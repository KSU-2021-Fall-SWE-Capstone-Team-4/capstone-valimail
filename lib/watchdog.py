from time import sleep
import threading
from threading import Thread

class Watchdog(Thread):

    def __init__(self):
        """
        Initializer for Watchdog thread.
        """
        Thread.__init__(self)

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
            for thread in threading.enumerate():
                if type(thread) is threading._MainThread:
                    main_thread_running = True
            # If the main thread ISN'T running, produce a critical error and exit.
            if not main_thread_running:
                logging.critical('Main thread stopped running for some reason, exiting')
                exit(-1)
            # Sleep for 1 second.
            sleep(1)