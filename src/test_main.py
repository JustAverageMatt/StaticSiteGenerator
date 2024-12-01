import unittest

from main import extract_title


class TestMain(unittest.TestCase):

    def test_extract_title(self):
        result = extract_title("# Header\n123")
        expected_result = "Header"
        self.assertEqual(result, expected_result)
