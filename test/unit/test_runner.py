from unittest import TestLoader, TextTestRunner


def initialize_testing_suite():
    """
    Initializes (and runs) the testing suite.
    Runs every test in the test/unit directory at the same time.
    """
    # Get the test loader
    test_loader = TestLoader()

    # Discover unit tests in the test/unit directory
    loaded_tests = test_loader.discover('test/unit')

    # Create the TextTestRunner
    runner = TextTestRunner(verbosity=2)

    # Run the suite
    runner.run(loaded_tests)


# Running part.
if __name__ == '__main__':
    initialize_testing_suite()
