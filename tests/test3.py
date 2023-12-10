import unittest
from main3 import func3

class TestDashboard3(unittest.TestCase):
    def test_no_exceptions_thrown(self):
        try:
            # Call the method that should not raise exceptions
            func3()  # Replace 'your_method' with the actual method you want to test

            # Add additional assertions based on the behavior of your method, if needed
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")

if __name__ == '__main__':
    unittest.main()
