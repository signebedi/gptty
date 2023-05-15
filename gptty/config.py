__name__ = "gptty.config"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.2.6"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

import configparser

# parse config data
def get_config_data(config_file='gptty.ini'):

    """
    The get_config_data() function reads a configuration file and returns a dictionary containing the parsed data. 
    If the configuration file does not exist or does not contain a particular key, a default value is used. 
    The default configuration values are defined in the function itself. 
    By default, the function reads the gptty.ini configuration file, but you can specify a different file name by passing it as an argument.

    The returned dictionary has the following keys:

        api_key: An API key used to authenticate with the OpenAI API.
        your_name: The name of the user (you) who is running the program.
        gpt_name: The name of the GPT model to use.
        output_file: The name of the output file to write the generated text to.
        model: The ID of the GPT model to use.
        temperature: The temperature value to use when generating text.
        max_tokens: The maximum number of tokens to generate in the generated text.
        max_context_length: The maximum number of tokens to use as context when generating text.
        context_keywords_only: A boolean value indicating whether to use only the keywords in the context when generating text.
        preserve_new_lines: A boolean value indicating whether to preserve new lines in the generated text.
        verify_internet_endpoint: The internet endpoint to use when verifying the internet connection.

    Note: This function uses the configparser module to parse configuration files.
    """

    # create a configuration object
    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        'api_key': "",
        'org_id': "",
        'your_name': 'question',
        'gpt_name': 'response',
        'output_file': 'output.txt',
        'model': 'text-davinci-003',
        'temperature': 0.0,
        'max_tokens': 250,
        'max_context_length': 150,
        'context_keywords_only': True,
        'preserve_new_lines': False,
        'verify_internet_endpoint': 'google.com',
    }

    # read the configuration file (if it exists)
    config.read(config_file)

    parsed_data = {
        'api_key': config.get('main', 'api_key', fallback="",),
        'org_id': config.get('main', 'org_id', fallback="",),
        'your_name': config.get('main', 'your_name', fallback='question'),
        'gpt_name': config.get('main', 'gpt_name', fallback='response'),
        'output_file': config.get('main', 'output_file', fallback='output.txt'),
        'model': config.get('main', 'model', fallback='text-davinci-003'),
        'temperature': config.getfloat('main', 'temperature', fallback=0.0),
        'max_tokens': config.getint('main', 'max_tokens', fallback=25),
        'max_context_length': config.getint('main', 'max_context_length', fallback=150),
        'context_keywords_only': config.getboolean('main', 'context_keywords_only', fallback=True),
        'preserve_new_lines': config.getboolean('main', 'preserve_new_lines', fallback=False),
        'verify_internet_endpoint': config.get('main', 'verify_internet_endpoint', fallback='google.com'),
	}

   

    return parsed_data
