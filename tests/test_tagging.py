import unittest
from gptty.tagging import get_tag_from_text

class TestTagging(unittest.TestCase):

    # Test when there's no tag in the input text
    def test_no_tag(self):
        result = get_tag_from_text("This is a test.")
        self.assertEqual(result, ('', "This is a test."))

    # Test when there's a single-word tag in the input text
    def test_single_word_tag(self):
        result = get_tag_from_text("[Tag] This is a test.")
        self.assertEqual(result, ('Tag', "This is a test."))

        # Test when there's a multi-word tag in the input text
    def test_multi_word_tag(self):
        result = get_tag_from_text("[Multi Word Tag] This is a test.")
        self.assertEqual(result, ('Multi-Word-Tag', "This is a test."))

    # Test when there's an incomplete tag in the input text
    def test_incomplete_tag(self):
        result = get_tag_from_text("[Incomplete Tag This is a test.")
        self.assertEqual(result, ('', "[Incomplete Tag This is a test."))

if __name__ == '__main__':
    unittest.main()
