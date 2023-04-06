__name__ = "gptty.gptty"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.2.5"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

import click
import openai
import pandas as pd
from aioconsole import ainput
from datetime import datetime
import os, time, sys, asyncio, json

# prompt toolkit requirements
from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.styles import Style
from prompt_toolkit.patch_stdout import patch_stdout

# app specific requirements
from gptty.tagging import get_tag_from_text
from gptty.context import get_context
from gptty.config import get_config_data

# Define color codes
CYAN = "\033[1;36m"
RED = "\033[1;31m"
RESET = "\033[0m"
YELLOW = "\033[1;33m"
GREY = "\033[90m"
ERASE_LINE = "\033[K"
MOVE_CURSOR_UP = "\033[F"

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


def usage_stats_today():

    r = openai.api_requestor.APIRequestor()
    resp = r.request("GET", f'/usage?date={datetime.now().strftime("%Y-%m-%d")}')
    resp_object = resp[0].data

    requests_today = resp_object['data'][0]['n_requests'] # num requests
    query_tokens_today = resp_object['data'][0]['n_context_tokens_total'] # query tokens
    response_tokens_today = resp_object['data'][0]['n_generated_tokens_total'] # response tokens

    return requests_today, query_tokens_today, response_tokens_today

## VALIDATE MODELS - these functions are use to validate the model passed by the user and raises an exception if 
## the model does not exist.
def get_available_models():

    """    
    Returns:
        - List: list of available OpenAI model IDs.

    """

    response = openai.Model.list()
    return [model.id for model in response['data']]

def is_valid_model(model_name):
    """
    Validates whether a given model name is available in the OpenAI platform.

    Parameters:
    - model_name (str): The name of the model to validate.

    Returns:
    - bool: True if the model name is available, False otherwise.
    """

    available_models = get_available_models()
    return model_name in available_models

def validate_model_type(model_name):

    """
    Validates whether a given model name is a supported model type for OpenAI API completion requests.

    Parameters:
    - model_name (str): The name of the model to validate.

    Returns:
    - str: The API endpoint to use for completion requests if the model name is valid and supported.

    Raises:
    - Exception: If the model name is not valid or not supported.
    """

    if ('davinci' in model_name or 'curie' in model_name) and is_valid_model(model_name):
        return 'v1/completions'
    elif 'gpt' in model_name and is_valid_model(model_name):
        return 'v1/chat/completions'
    raise Exception()

# here we define the async call to the openai API that is used when running queries
async def fetch_response(prompt, model_engine, max_tokens, temperature, model_type):

    """
    This module provides a function to fetch a response from the OpenAI API based on the given prompt and model specifications.

    Parameters:
    - prompt (str): The prompt to use for the API request.
    - model_engine (str): The engine ID to use for the API request.
    - max_tokens (int): The maximum number of tokens to generate in the response.
    - temperature (float): The temperature to use for the API request.
    - model_type (str): The API endpoint to use for the API request.

    Returns:
    - OpenAICompletion: The completion response object from the OpenAI API.

    Raises:
    - Exception: If the model type is not recognized or supported.
    """

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
        # click.echo(f"\n{CYAN}SUCCESS validating model type 'v1/chat/completions'. Feature still under development. See <https://github.com/signebedi/gptty/issues/31> for more info.{RESET}\n")
        # return None

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

    """
    This module provides a function to display a wait graphic while awaiting responses.

    Returns:
    - None
    """

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
async def create_chat_room(configs=get_config_data(), log_responses:bool=True, config_path=None, verbose:bool=False):

    """
    This function creates a chat room using the OpenAI API to generate responses to user inputs. 
    The user input is prompted and the response is displayed on the console. 
    The chat session is continuously open until the user enters ':quit' or ':q' to terminate the session. 
    The session log is stored in a csv file. 
    
    Parameters:
    - configs: A dictionary containing OpenAI API key, model name, temperature, max_tokens, max_context_length, context_keywords_only, preserve_new_lines, gpt_name and your_name.
    - log_responses: A boolean indicating whether or not to log the responses in a csv file. Default is True.
    - config_path: The path to the configuration file.
    - verbose: A boolean indicating whether or not to print debugging information. Default is False.

    Returns:
    - None
    """


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

    session = PromptSession()

    # Continuously send and receive messages
    while True:

        # Get user input
        try:

            usage = usage_stats_today() if verbose else ""

            with patch_stdout():
                i = await session.prompt_async(ANSI(f"{CYAN}{usage}> "), style=Style.from_dict({'': 'ansicyan'}))
            print(f"{ERASE_LINE}{MOVE_CURSOR_UP}{GREY}{usage}> {i}\n", end="")

            # i = await ainput(f"{CYAN}> ")
            tag,question = get_tag_from_text(i)
            prompt_length = len(question)

        # handle keyboard interrupt
        except KeyboardInterrupt:
            i = False

        if i == False:
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
        elif i.strip().startswith(':') or prompt_length < 1:
            click.echo('\nPlease provide a valid command or prompt.\n')
            continue

        # click.echo the question in color
        print(f"\n{CYAN}[{configs['your_name']}] {question}{RESET} \n", end="", flush=True)

        # we create the callable wait_graphic task
        wait_task = asyncio.create_task(wait_graphic())

        fully_contextualized_question = get_context(tag, configs['max_context_length'], configs['output_file'], model_engine, context_keywords_only=configs['context_keywords_only'], model_type=model_type, question=question, debug=verbose)

        response_task = asyncio.create_task(fetch_response(fully_contextualized_question, model_engine, max_tokens, temperature, model_type))

        # Wait for the response to be completed
        response = await response_task

        # Cancel the wait graphic task
        wait_task.cancel()
        print("\b" * 10 , end="", flush=True)

        if not response:
            continue

        response_text = response.choices[0].text.strip() if model_type == 'v1/completions' else response.choices[0]['message']['content'].strip()
        deformatted_response_text = response.choices[0].text.strip().replace("\n", " ") if model_type == 'v1/completions' else response.choices[0]['message']['content'].strip().replace("\n", " ")

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
async def run_query(questions:list, tag:str, configs=get_config_data(), additional_context:str="", log_responses:bool=True, config_path=None, verbose:bool=False, return_json:bool=False, quiet:bool=False):

    """
    This function is used to run a query command using OpenAI. 
    It takes in a list of questions, a tag, additional context, and various configuration options. 
    It authenticates with OpenAI using the API key specified in the configuration file, and then continuously sends and receives messages until all the questions 
    have been answered. The responses are either printed to the console in color or returned in a JSON format, depending on the options specified. Additionally, 
    the function logs the questions and responses in a pandas dataframe if specified in the configuration file.

    Parameters:
        questions (list): a list of questions to ask the GPT-3 model
        tag (str): a tag to associate with the questions and responses
        configs (dict): a dictionary containing configuration options (default: get_config_data())
        additional_context (str): additional context to provide to the GPT-3 model (default: "")
        log_responses (bool): whether to log the questions and responses in a pandas dataframe (default: True)
        config_path (str): the path to the configuration file (default: None)
        verbose (bool): whether to enable debug mode (default: False)
        return_json (bool): whether to return the responses in a JSON format (default: False)
        quiet (bool): whether to suppress console output (default: False)

    Returns:
        None if the function fails to authenticate with OpenAI or if there are no questions to ask
        if return_json is True and quiet is False, prints a JSON representation of the question/response data to the console and returns None
        if return_json is True and quiet is True, returns a JSON representation of the question/response data
        if return_json is False and quiet is False, prints the responses to the console in color and returns None
        if return_json is False and quiet is True, returns None
    """


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

    # create a json representation of the question / response data FOR THE CURRENT SESSION
    json_output = []

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

        if not return_json and not quiet:
            # click.echo the question in color
            print(f"{CYAN}[{configs['your_name']}] {question}{RESET} \n", end="", flush=True)

            # we create the callable wait_graphic task
            wait_task = asyncio.create_task(wait_graphic())

        fully_contextualized_question = get_context(tag, configs['max_context_length'], configs['output_file'], model_engine, additional_context=additional_context, context_keywords_only=configs['context_keywords_only'], model_type=model_type, question=question, debug=verbose)

        response_task = asyncio.create_task(fetch_response(fully_contextualized_question, model_engine, max_tokens, temperature, model_type))

        # Wait for the response to be completed
        response = await response_task

        if not return_json and not quiet:
            # Cancel the wait graphic task
            wait_task.cancel()
            print("\b" * 10 , end="", flush=True)

        response_text = response.choices[0].text.strip() if model_type == 'v1/completions' else response.choices[0]['message']['content'].strip()
        deformatted_response_text = response.choices[0].text.strip().replace("\n", " ") if model_type == 'v1/completions' else response.choices[0]['message']['content'].strip().replace("\n", " ")

        if configs['preserve_new_lines']:
            response_text_to_print = f"\b{RED}[{configs['gpt_name']}] {response_text}{RESET}\n"
        else:
            # click.echo the response in color
            response_text_to_print = f"\b{RED}[{configs['gpt_name']}] {deformatted_response_text}{RESET}\n"

        if log_responses:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open (configs['output_file'], 'a') as f:
                f.write(f"{timestamp}|{tag}|{question.replace('|','')}|{deformatted_response_text.replace('|','')}\n")

        if return_json or quiet:
            json_output.append({
                'question': question,
                'response': deformatted_response_text
            })
        else:
            click.echo(response_text_to_print)

    # Add this line before the final return statement
    if return_json and not quiet:
        json_response = json.dumps(json_output)
        click.echo(json_response)
        # return json_response
        return