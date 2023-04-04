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
        self.assertLessEqual(len(result.split()), 50)


    def test_get_context_no_keywords(self):
        result = get_context("Tag1", 50, "tests/test_context_data.txt", "text-davinci-003", context_keywords_only=False, question="Who is its mayor?")
        expected = "what is the capital of australia? The capital of Australia is Canberra. when was it founded? Canberra was founded in 1913 as the site for Australia's capital city. Who is its mayor?"
        self.assertEqual(result.strip(), expected.strip())
        self.assertLessEqual(len(result.split()), 50)

    def test_get_context_v1_chat_completions(self):
        test_data_file = 'tests/test_context_data.txt'
        tag = 'Tag1'
        question = 'What is the population of Australia?'
        model_name = 'gpt-3'
        max_context_length = 50
        model_type = 'v1/chat/completions'

        expected_context = [
            {'role': 'user', 'content': 'what is the capital of australia?'},
            {'role': 'assistant', 'content': 'The capital of Australia is Canberra.'},
            {'role': 'user', 'content': 'when was it founded?'},
            {'role': 'assistant', 'content': "Canberra was founded in 1913 as the site for Australia's capital city."},
            {'role': 'user', 'content': question},
        ]

        result = get_context(tag, max_context_length, test_data_file, model_name, model_type=model_type, question=question)
        self.assertEqual(result, expected_context)
        self.assertLessEqual(sum(len(item["content"].split()) for item in result), 50)


    def test_get_context_no_tag(self):
        max_context_length = 50
        question = 'What is the population of Australia?'
        model_name = 'gpt-3'
        additional_context = 'Australia is a country in the Southern Hemisphere.'

        # Test for 'v1/chat/completions' model type
        model_type = 'v1/chat/completions'
        expected_context = [
            {'role': 'system', 'content': additional_context},
            {'role': 'user', 'content': question},
        ]

        result = get_context('', max_context_length, None, model_name, additional_context=additional_context, model_type=model_type, question=question)
        self.assertEqual(result, expected_context)
        self.assertLessEqual(sum(len(item["content"].split()) for item in result), 50)


    def test_get_context_no_tag_v1_chat_completions(self):
        max_context_length = 50
        question = 'What is the capital of Australia?'
        model_name = 'gpt-3'
        additional_context = ("I am doing an important research project on the capitals cities of Oceania, "
                              "and need help identifying the important aspects of each. This project is being "
                              "completed for Mr. Anderson's sixth grade history course, and so I also need help "
                              "writing each response as if it is part of a longer essay that we need to write "
                              "called Capitals of the World.")
        model_type = 'v1/chat/completions'

        result = get_context('', max_context_length, None, model_name, additional_context=additional_context, model_type=model_type, question=question)
        self.assertTrue(isinstance(result, list))
        self.assertTrue({'role': 'user', 'content': question} in result)
        self.assertLessEqual(len(question.split()), 50)


    def test_get_context_no_tag_other_model_types(self):
        max_context_length = 50
        question = 'What is the capital of Australia?'
        model_name = 'gpt-3'
        additional_context = ("I am doing an important research project on the capitals cities of Oceania, "
                              "and need help identifying the important aspects of each. This project is being "
                              "completed for Mr. Anderson's sixth grade history course, and so I also need help "
                              "writing each response as if it is part of a longer essay that we need to write "
                              "called Capitals of the World.")
        model_type = None

        result = get_context('', max_context_length, None, model_name, additional_context=additional_context, model_type=model_type, question=question)
        self.assertTrue(isinstance(result, str))
        self.assertTrue(question in result)
        self.assertLessEqual(len(result.split()), 50)


if __name__ == '__main__':
    unittest.main()
