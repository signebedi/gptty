__name__ = "gptty.config"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.1.0"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

import configparser

# parse config data
def get_config_data(config_file='gptty.ini'):
    # create a configuration object
    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        'api_key': "",
        'gpt_version': '3',
        'your_name': 'question',
        'gpt_name': 'response',
        'output_file': 'output.txt',
        'model': 'text-davinci-003',
        'temperature': 0.0,
        'max_tokens': 250,
        'max_context_length': 5000,
    }

    # read the configuration file (if it exists)
    config.read(config_file)

    parsed_data = {
        'api_key': config.get('main', 'api_key', fallback="",),
        'gpt_version': config.get('main', 'gpt_version', fallback='3'),
        'your_name': config.get('main', 'your_name', fallback='question'),
        'gpt_name': config.get('main', 'gpt_name', fallback='response'),
        'output_file': config.get('main', 'output_file', fallback='output.txt'),
        'model': config.get('main', 'model', fallback='text-davinci-003'),
        'temperature': config.getfloat('main', 'temperature', fallback=0.0),
        'max_tokens': config.getint('main', 'max_tokens', fallback=25),
        'max_context_length': config.getint('main', 'max_context_length', fallback=5000),
    }

    return parsed_data