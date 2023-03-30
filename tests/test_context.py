import unittest
from gptty.context import return_most_common_phrases, get_context


class TestContext(unittest.TestCase):
    def test_return_most_common_phrases(self):
        text = "The quick brown fox jumps over the lazy dog."
        result = return_most_common_phrases(text)
        self.assertEqual(result, ['lazy dog', 'quick brown fox jumps'])

    def test_get_context_keywords_only(self):
        result = get_context("Tag1", 50, "tests/test_context_data.txt", "text-davinci-003", context_keywords_only=True, question="Who is its mayor?")
        expected = "australia canberra 's capital city Who is its mayor?"
        self.assertEqual(result.strip(), expected.strip())

    def test_get_context_no_keywords(self):
        result = get_context("Tag1", 50, "tests/test_context_data.txt", "text-davinci-003", context_keywords_only=False, question="Who is its mayor?")
        expected = "what is the capital of australia? The capital of Australia is Canberra. when was it founded? Canberra was founded in 1913 as the site for Australia's capital city. Who is its mayor?"
        self.assertEqual(result.strip(), expected.strip())

    # Placeholder - tests when model_type == 'v1/chat/completions'

if __name__ == '__main__':
    unittest.main()
