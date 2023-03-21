__name__ = "gptty.gptty"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.1.0"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

import openai
import time
from datetime import datetime
import click
import pandas as pd

# app specific requirements
from tagging import get_tag_from_text
from context import get_context
from config import get_config_data

# Define color codes
CYAN = "\033[1;36m"
RED = "\033[1;31m"
RESET = "\033[0m"

def create_chat_room(configs=get_config_data(), log_responses=True):

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

    openai.api_key = configs['api_key'].rstrip('\n')

    # Set the parameters for the OpenAI completion API
    model_engine = configs['model'].rstrip('\n')
    temperature = configs['temperature'] # controls the creativity of the response
    max_tokens = configs['max_tokens']  # the maximum length of the generated response

    # Continuously send and receive messages
    while True:
        # Get user input
        i = input(f"{CYAN}> ")
        tag,question = get_tag_from_text(i)
        prompt_length = len(question)

        if prompt_length < 1:
            click.echo('\nPlease provide an actual prompt.\n')
            continue
        elif i.strip() == ':help':
            click.echo('\nCommands:\n:help - see help\n:quit - quit app\n:context[a:b] - show context history with optional index ranges a and b *under development*\n:configs - show configs\nTo send a question to ChatGPT, just type it into the chat interface like `why is the sky blue`.\nTo share context across conversations, prepend questions with tags like `[shakespeare] who is william shakespeare`.\nTo pass context positionally, prepend questions with tags like `[a:b] what is the meaning of life`.\n')
            continue
        elif i.strip() == ':quit':
            click.echo ('\nGoodbye ... \n')
            break
        elif i.strip() == ':configs':
            c = f'{"|".join(f"{key}: {value}" for key, value in configs.items())}'.replace('|','\n')
            click.echo (f'\n{c}\n')
            continue
        elif i.strip() == ':context':
            # c = f'{"|".join(f"{row[]}" for index,row in df.iterrows())}'.replace('|','\n')
            click.echo (f'\n{df}\n')
            continue
        elif i.strip().startswith(':'):
            click.echo('\nPlease provide a valid command.\n')
            continue



        # Show the waiting graphic
        for i in range(10):
            print("." * i + " " * (9 - i), end="", flush=True)
            time.sleep(0.1)
            print("\b" * 10, end="", flush=True)


        fully_contextualized_question = get_context(tag, configs['max_context_length'],configs['output_file']) + ' ' + question

        response = openai.Completion.create(
            engine=model_engine,
            prompt=fully_contextualized_question,
            max_tokens=max_tokens,
            temperature=temperature,
            n=1,
            stop=None,
            timeout=15,
        )

        response_text = response.choices[0].text.strip().replace("\n", "")

        # click.echo the question in color
        print(f"{CYAN}[{configs['your_name']}] {question}{RESET} \n", end="", flush=True)

        # click.echo the response in color
        click.echo(f"\b{RED}[{configs['gpt_name']}] {response_text}{RESET}\n")

        if log_responses:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open (configs['output_file'], 'a') as f:
                f.write(f"{timestamp}|{tag}|{question.replace('|','')}|{response_text.replace('|','')}\n")

            # here we update the pandas reference object, see 
            # https://github.com/signebedi/gptty/issues/15
            df = pd.concat([df, pd.DataFrame({"timestamp":[timestamp],"tag":[tag],"question":[question],"response":[response_text],})])
