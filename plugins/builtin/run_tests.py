import unittest

# Discover and run all test scripts in the "tests" directory
if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')

    runner = unittest.TextTestRunner(verbosity=1)
    result = runner.run(test_suite)
