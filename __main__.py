"""
gptty: chat GPT CLI wrapper

"""

__name__ = "gptty"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.1.0"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

import openai
import time
import asyncio
import aiohttp
import json
from typing import Optional
import configparser

# parse config data
def parse_config_data(config_file='gptty.ini'):
    # create a configuration object
    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        'api_key': "",
        'gpt_version': '3',
        'your_name': 'question',
        'gpt_name': 'response',
        'output_file': 'output.txt'
    }


    # read the configuration file (if it exists)
    config.read(config_file)

    parsed_data = {
        'api_key': config.get('main', 'api_key', fallback="",),
        'gpt_version': config.get('main', 'gpt_version', fallback='3'),
        'your_name': config.get('main', 'your_name', fallback='question'),
        'gpt_name': config.get('main', 'gpt_name', fallback='response'),
        'output_file': config.get('main', 'output_file', fallback='output.txt'),
    }

    option1 = config.get('section1', 'option1', fallback='value1')
    option2 = config.get('section1', 'option2', fallback='value2')

    return parsed_data


# Define async API call function
async def make_request(session, url, message):
    async with session.post(url, data=message) as response:
        return await response.text()


# Define a more robust function to query the API
async def query_api(session, url, message: str) -> Optional[str]:
    # Make the HTTP request
    async with session.post(url, data={"message": message}) as response:
        # Check the status code
        if response.status == 200:
            # Return the response text
            return await response.text()
        else:
            # Return None if there was an error
            return None



async def create_chat_room(dev=False, url="http://0.0.0.0:8080", configs=parse_config_data(), log_responses=True):

    # Authenticate with OpenAI using your API key
    # print (configs['api_key'])
    openai.api_key = configs['api_key'].rstrip('\n')

    # Set the parameters for the OpenAI completion API
    model_engine = "davinci" # the most capable GPT-3 model
    temperature = 0.5 # controls the creativity of the response
    max_tokens = 1024 # the maximum length of the generated response

    # Create a session object
    async with aiohttp.ClientSession() as session:
        # Continuously send and receive messages
        while True:
            # Get user input
            question = input(f"{CYAN}> ")
            prompt_length = len(question)

            if prompt_length < 1:
                print('Please provide an actual prompt.\n')
                continue

            # Query the API asynchronously
            response = None
            while not response:

                # Show the waiting graphic
                for i in range(10):
                    print("." * i + " " * (9 - i), end="", flush=True)
                    time.sleep(0.1)
                    print("\b" * 10, end="", flush=True)


                response = openai.Completion.create(
                    engine=model_engine,
                    prompt=question,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    n=1,
                    stop=None,
                    timeout=15,
                )


            #     # Query the API
            #     response = await query_api(session, url, question)

            # # We expect a json object, which we unpack here
            # response = json.loads(response)

            # print the question in color
            print(f"{CYAN}[{configs['your_name']}] {question}{RESET} \n", end="", flush=True)

            # Print the response in color
            # print(f"\b{RED}[{configs['gpt_name']}] {response['response']}{RESET}\n")
            print(f"\b{RED}[{configs['gpt_name']}] {response.choices[0].text.strip()}{RESET}\n")

            if log_responses:
                with open (configs['output_file'], 'a') as f:
                    f.write(f"{question},{response.choices[0].text.strip()}")

# Define color codes
CYAN = "\033[1;36m"
RED = "\033[1;31m"
RESET = "\033[0m"


title = r"""  
   _____ _____ _______ _________     __
  / ____|  __ \__   __|__   __\ \   / /
 | |  __| |__) | | |     | |   \ \_/ / 
 | | |_ |  ___/  | |     | |    \   /  
 | |__| | |      | |     | |     | |   
  \_____|_|      |_|     |_|     |_|   
                                     
"""

# Print the text in cyan
print(f"{CYAN}{title}\nWelcome to GPTTY (v.{__version__}), a ChatGPT wrapper for your CLI.\nWritten by Sig Janoska-Bedi <signe@atreeus.com> under the {__license__} license.{RESET}")


# Run the main coroutine
asyncio.run(create_chat_room())


