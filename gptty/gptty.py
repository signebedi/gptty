__name__ = "gptty.gptty"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.2.2"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

import openai
import time
from datetime import datetime
import click
import pandas as pd
import os
import sys
import asyncio
from aioconsole import ainput

# app specific requirements
from gptty.tagging import get_tag_from_text
from gptty.context import get_context
from gptty.config import get_config_data

# Define color codes
CYAN = "\033[1;36m"
RED = "\033[1;31m"
RESET = "\033[0m"

HELP = """
                        [Commands]
:h[elp]                                     -   see help
:q[uit]                                     -   quit app
:l[og]                                      -   show history log
:c[onfigs]                                  -   show configs

                        [Questions]
`why is the sky blue`                       -   send a question to ChatGPT
`[shakespeare] who is william shakespeare`  -   share context across conversations
`[a:b] what is the meaning of life`         -   pass context positionally
"""

## VALIDATE MODELS - these functions are use to validate the model passed by the user and raises an exception if 
## the model does not exist.
def get_available_models():
    response = openai.Model.list()
    return [model.id for model in response['data']]

def is_valid_model(model_name):
    available_models = get_available_models()
    return model_name in available_models

def validate_model_type(model_name):
    if ('davinci' in model_name or 'curie' in model_name) and is_valid_model(model_name):
        return 'v1/completions'
    elif 'gpt' in model_name and is_valid_model(model_name):
        return 'v1/chat/completions'
    raise Exception()

# here we define the async call to the openai API that is used when running queries
async def fetch_response(prompt, model_engine, max_tokens, temperature, model_type):
    if model_type == 'v1/completions':

        return await openai.Completion.acreate(
            engine=model_engine,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            n=1,
            stop=None,
            timeout=15,
        )

    if model_type == 'v1/chat/completions':
        click.echo(f"\n{CYAN}SUCCESS validating model type 'v1/chat/completions'. Feature still under development. See <https://github.com/signebedi/gptty/issues/31> for more info.{RESET}\n")
        return None

        return await openai.ChatCompletion.acreate( 
            model = model_engine,
            messages = prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            n=1,
            stop=None,
            timeout=15,
        )

    click.echo(f"\n{RED}FAILED to validate the model type '{model_type}'. Are you sure this is a valid OpenAI model endpoint? Check the available model endpoints at <https://platform.openai.com/docs/models/model-endpoint-compatibility>. If you believe this is a bug, submit a bug request at <https://github.com/signebedi/gptty/issues>.{RESET}\n")
    return None


# here we design the wait graphic that is called while awaiting responses
async def wait_graphic():
    while True:
        # for i in range(1, 11):
        #     print("." * i + " " * (9 - i), end="", flush=True)
        #     await asyncio.sleep(0.1)
        #     print("\b" * 10, end="", flush=True)

        # Show the waiting graphic
        for i in range(10):
            print("." * i + " " * (9 - i), end="", flush=True)
            await asyncio.sleep(0.1)
            print("\b" * 10, end="", flush=True)

# this is used when we run the `chat` command
async def create_chat_room(configs=get_config_data(), log_responses=True, config_path=None):

    # Authenticate with OpenAI using your API key
    # click.echo (configs['api_key'])
    if configs['api_key'].rstrip('\n') == "":
        click.echo(f"{RED}FAILED to initialize connection to OpenAI. Have you added an API token? See gptty docs <https://github.com/signebedi/gptty#configuration> or <https://platform.openai.com/account/api-keys> for more information.")
        return

    # here we add a pandas df reference object, see 
    # https://github.com/signebedi/gptty/issues/15
    try:
        df = pd.read_csv(configs['output_file'], header=None,sep='|').fillna('')
        df.columns = ['timestamp','tag','question','response']
    except:
        df = pd.DataFrame(columns=['timestamp','tag','question','response'])

    try:
        openai.api_key = configs['api_key'].rstrip('\n')
    except:
        click.echo(f"{RED}FAILED to initialize connection to OpenAI. Have you added an API token? See gptty docs <https://github.com/signebedi/gptty#configuration> or <https://platform.openai.com/account/api-keys> for more information.")
        return

    # Set the parameters for the OpenAI completion API
    model_engine = configs['model'].rstrip('\n')
    temperature = configs['temperature'] # controls the creativity of the response
    max_tokens = configs['max_tokens']  # the maximum length of the generated response


    try:
        model_type = validate_model_type(model_engine)
    except:
        click.echo(f"{RED}FAILED to validate the model name '{model_engine}'. Are you sure this is a valid OpenAI model? Check the available models at <https://platform.openai.com/docs/models/overview> and try again.{RESET}")
        return

    # Continuously send and receive messages
    while True:
        # Get user input
        i = await ainput(f"{CYAN}> ")
        tag,question = get_tag_from_text(i)
        prompt_length = len(question)

        if prompt_length < 1:
            click.echo('\nPlease provide an actual prompt.\n')
            continue
        elif i.strip() in [':help',':h']:
            click.echo(HELP)
            continue
        elif i.strip() in [':quit',':q']:
            click.echo ('\nGoodbye ... \n')
            break
        elif i.strip() in [':configs',':c']:
            c = f'config_path: {config_path}|model_type: {model_type}|{"|".join(f"{key}: {value}" for key, value in configs.items())}'.replace('|','\n')
            click.echo (f'\n{c}\n')
            continue
        elif i.strip() in [':log',':l']:
            # c = f'{"|".join(f"{row[]}" for index,row in df.iterrows())}'.replace('|','\n')
            click.echo (f'\n{df}\n')
            continue
        elif i.strip().startswith(':'):
            click.echo('\nPlease provide a valid command.\n')
            continue


        # click.echo the question in color
        print(f"{CYAN}[{configs['your_name']}] {question}{RESET} \n", end="", flush=True)

        # we create the callable wait_graphic task
        wait_task = asyncio.create_task(wait_graphic())

        fully_contextualized_question = get_context(tag, configs['max_context_length'],configs['output_file'],context_keywords_only=configs['context_keywords_only']) + ' ' + question

        response_task = asyncio.create_task(fetch_response(fully_contextualized_question, model_engine, max_tokens, temperature, model_type))

        # Wait for the response to be completed
        response = await response_task

        # Cancel the wait graphic task
        wait_task.cancel()
        print("\b" * 10 , end="", flush=True)

        if not response:
            continue

        response_text = response.choices[0].text.strip() if model_type == 'v1/completions' else response.choices[0].text['content'].strip()
        deformatted_response_text = response.choices[0].text.strip().replace("\n", " ") if model_type == 'v1/completions' else response.choices[0].text['content'].strip().replace("\n", " ")

        if configs['preserve_new_lines']:
            click.echo(f"\b{RED}[{configs['gpt_name']}] {response_text}{RESET}\n")
        else:
            # click.echo the response in color
            click.echo(f"\b{RED}[{configs['gpt_name']}] {deformatted_response_text}{RESET}\n")

        if log_responses:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open (configs['output_file'], 'a') as f:
                f.write(f"{timestamp}|{tag}|{question.replace('|','')}|{deformatted_response_text.replace('|','')}\n")

            # here we update the pandas reference object, see 
            # https://github.com/signebedi/gptty/issues/15
            df = pd.concat([df, pd.DataFrame({"timestamp":[timestamp],"tag":[tag],"question":[question],"response":[deformatted_response_text],})], ignore_index=True)




# this is used when we run the `query` command
async def run_query(questions:list, tag:str, configs=get_config_data(), log_responses=True, config_path=None):

    if not os.path.exists(config_path):
        click.echo(f"{RED}FAILED to access app config file at {config_path}. Are you sure this is a valid config file? Run `gptty chat --help` for more information.")
        return

    # Authenticate with OpenAI using your API key
    # click.echo (configs['api_key'])
    if configs['api_key'].rstrip('\n') == "":
        click.echo(f"{RED}FAILED to initialize connection to OpenAI. Have you added an API token? See gptty docs <https://github.com/signebedi/gptty#configuration> or <https://platform.openai.com/account/api-keys> for more information.")
        return

    if len(questions) < 1 or not isinstance(questions, tuple):
        click.echo(f"{RED}FAILED to query ChatGPT. Did you forget to ask a question? Run `gptty chat --help` for more information.")
        return

    # here we add a pandas df reference object, see 
    # https://github.com/signebedi/gptty/issues/15
    try:
        df = pd.read_csv(configs['output_file'], header=None,sep='|').fillna('')
        df.columns = ['timestamp','tag','question','response']
    except:
        df = pd.DataFrame(columns=['timestamp','tag','question','response'])

    try:
        openai.api_key = configs['api_key'].rstrip('\n')
    except:
        click.echo(f"{RED}FAILED to initialize connection to OpenAI. Have you added an API token? See gptty docs <https://github.com/signebedi/gptty#configuration> or <https://platform.openai.com/account/api-keys> for more information.")
        return

    # Set the parameters for the OpenAI completion API
    model_engine = configs['model'].rstrip('\n')
    temperature = configs['temperature'] # controls the creativity of the response
    max_tokens = configs['max_tokens']  # the maximum length of the generated response

    try:
        model_type = validate_model_type(model_engine)
    except:
        click.echo(f"{RED}FAILED to validate the model name '{model_engine}'. Are you sure this is a valid OpenAI model? Check the available models at <https://platform.openai.com/docs/models/overview> and try again.{RESET}")
        return

    # Continuously send and receive messages
    for question in questions:
        if len(question) < 1:
            continue


        # click.echo the question in color
        print(f"{CYAN}[{configs['your_name']}] {question}{RESET} \n", end="", flush=True)


        # we create the callable wait_graphic task
        wait_task = asyncio.create_task(wait_graphic())

        fully_contextualized_question = get_context(tag, configs['max_context_length'],configs['output_file'],context_keywords_only=configs['context_keywords_only']) + ' ' + question

        response_task = asyncio.create_task(fetch_response(fully_contextualized_question, model_engine, max_tokens, temperature, model_type))

        # Wait for the response to be completed
        response = await response_task

        # Cancel the wait graphic task
        wait_task.cancel()
        print("\b" * 10 , end="", flush=True)

        response_text = response.choices[0].text.strip() if model_type == 'v1/completions' else response.choices[0].text['content'].strip()
        deformatted_response_text = response.choices[0].text.strip().replace("\n", " ") if model_type == 'v1/completions' else response.choices[0].text['content'].strip().replace("\n", " ")

        if configs['preserve_new_lines']:
            click.echo(f"\b{RED}[{configs['gpt_name']}] {response_text}{RESET}\n")
        else:
            # click.echo the response in color
            click.echo(f"\b{RED}[{configs['gpt_name']}] {deformatted_response_text}{RESET}\n")

        if log_responses:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open (configs['output_file'], 'a') as f:
                f.write(f"{timestamp}|{tag}|{question.replace('|','')}|{deformatted_response_text.replace('|','')}\n")
