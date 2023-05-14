import unittest
from gptty.config import get_config_data

class TestConfig(unittest.TestCase):

    # Test the default configuration values
    def test_default_config(self):
        default_config_data = get_config_data('test/test_default_gptty.ini')
        self.assertEqual(default_config_data['api_key'], "")
        self.assertEqual(default_config_data['org_id'], "")
        self.assertEqual(default_config_data['your_name'], 'question')
        self.assertEqual(default_config_data['gpt_name'], 'response')
        self.assertEqual(default_config_data['output_file'], 'output.txt')
        self.assertEqual(default_config_data['model'], 'text-davinci-003')
        self.assertEqual(default_config_data['temperature'], 0.0)
        self.assertEqual(default_config_data['max_tokens'], 25)
        self.assertEqual(default_config_data['max_context_length'], 150)
        self.assertEqual(default_config_data['context_keywords_only'], True)
        self.assertEqual(default_config_data['preserve_new_lines'], False)

    # Test with a custom configuration file
    def test_custom_config(self):
        custom_config_data = get_config_data(config_file='tests/test_gptty.ini')
        self.assertEqual(custom_config_data['api_key'], "ANOTHER_KEY_HERE")
        self.assertEqual(custom_config_data['org_id'], "org-536JCU1SlmsQZB0i734dCsGC")
        self.assertEqual(custom_config_data['your_name'], 'custom_question')
        self.assertEqual(custom_config_data['gpt_name'], 'custom_response')
        self.assertEqual(custom_config_data['output_file'], 'custom_output.txt')
        self.assertEqual(custom_config_data['model'], 'text-curie-003')
        self.assertEqual(custom_config_data['temperature'], 0.5)
        self.assertEqual(custom_config_data['max_tokens'], 300)
        self.assertEqual(custom_config_data['max_context_length'], 200)
        self.assertEqual(custom_config_data['context_keywords_only'], False)
        self.assertEqual(custom_config_data['preserve_new_lines'], True)


if __name__ == '__main__':
    unittest.main()