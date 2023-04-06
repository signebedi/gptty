
"""
gptty: context-preserving chatGPT CLI wrapper

"""

__name__ = "gptty"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.2.5"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

# general packages
import click
import os
import asyncio
import pandas as pd
import nltk
import socket
from contextlib import closing

# app specific requirements
from gptty.config import get_config_data
from gptty.gptty import create_chat_room, run_query

# Define color codes
CYAN = "\033[1;36m"
RED = "\033[1;31m"
RESET = "\033[0m"

# download nltk corpora if they are not already downloaded
def download_nltk_data_if_needed(data_name):
    try:
        nltk.data.find(data_name)
    except LookupError:
        nltk.download(data_name.split('/')[-1])

# Download 'stopwords', 'punkt', and 'brown' if they haven't been downloaded yet
download_nltk_data_if_needed('corpora/stopwords')
download_nltk_data_if_needed('tokenizers/punkt')
download_nltk_data_if_needed('corpora/brown')

# return a simple pandas df of the logged questions
def return_log_as_df(configs):
    # here we add a pandas df reference object, see 
    # https://github.com/signebedi/gptty/issues/15
    try:
        df = pd.read_csv(configs['output_file'], header=None,sep='|').fillna('')
        df.columns = ['timestamp','tag','question','response']
    except:
        df = pd.DataFrame(columns=['timestamp','tag','question','response'])
    return df

# Check if the system has a valid internet connection

def has_internet_connection(host="google.com", port=443, timeout=3):
    """Check if the system has a valid internet connection.

    Args:
        host (str, optional): A well-known website to test the connection. Default is 'www.google.com'.
        port (int, optional): The port number to use for the connection. Default is 80.
        timeout (int, optional): The time in seconds to wait for a response before giving up. Default is 3.

    Returns:
        bool: True if the system has an internet connection, False otherwise.
    """
    try:
        with closing(socket.create_connection((host, port), timeout=timeout)):
            return True
    except OSError:
        return False

# borrowed version callback from https://click.palletsprojects.com/en/7.x/options/#callbacks-and-eager-options
def print_version(ctx, param, value, version=__version__):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f'gptty version {version}')
    ctx.exit()

@click.group()
@click.option('--version', '-v', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True, help="Show app version.")
def main():
  pass


@click.command()
@click.option('--config_path', '-c', default=os.path.join(os.getcwd(),'gptty.ini'), help="Path to config file.")
@click.option('--verbose', '-v', is_flag=True, help="Show debug data.")
def chat(config_path:str, verbose:bool):
  
  """
  Run the gptty chat client
  """

  asyncio.run(chat_async_wrapper(config_path, verbose))

async def chat_async_wrapper(config_path:str, verbose:bool):
  title = r"""
                 _   _         
     ____  ____ | | | |        
    / __ `/ __ \| |_| |_ _   _ 
   / /_/ / /_/ /| __| __| | | |
   \__, / .___/ | |_| |_| |_| |
  /____/_/       \__|\__|\__, |
                          __/ |
                         |___/ 
  """

  # Print the text in cyan
  click.echo(f"{CYAN}{title}\nWelcome to gptty (v.{__version__}), a ChatGPT wrapper in your TTY. Type :help in the chat interface if you need help getting started.{' Verbose / Debug mode is on. Query prompts will be preceded by your daily API usage in the format (query count, query tokens, response tokens).' if verbose else ''}{RESET}\n")
  
  if not os.path.exists(config_path):
      click.echo(f"{RED}FAILED to access app config file at {config_path}. Are you sure this is a valid config file? Run `gptty chat --help` for more information. You can get a sample config at <https://github.com/signebedi/gptty/blob/master/assets/gptty.ini.example>.")
      return

  # load the app configs
  configs = get_config_data(config_file=config_path)

  # Here, we verify that we have a wifi connection and if not, exit
  if not has_internet_connection(configs['verify_internet_endpoint']):
    click.echo(f"{RED}FAILED to verify connection at {configs['verify_internet_endpoint']}. Are you sure you are connected to the internet?")
    return

  # create the output file if it doesn't exist
  with open (configs['output_file'], 'a'): pass
  
  # Authenticate with OpenAI using your API key
  # click.echo (configs['api_key'])
  if configs['api_key'].rstrip('\n') == "":
      click.echo(f"{RED}FAILED to initialize connection to OpenAI. Have you added an API token? See gptty docs <https://github.com/signebedi/gptty#configuration> or <https://platform.openai.com/account/api-keys> for more information.")
      return

  # Run the main function
  # create_chat_room(configs=configs, config_path=config_path)
  # asyncio.run(create_chat_room(configs=configs, config_path=config_path))
  await create_chat_room(configs=configs, config_path=config_path, verbose=verbose)


@click.command()
# @click.option('--log', '-l', is_flag=True, callback=print_version,
#               expose_value=False, is_eager=True, help="Show question log.")
@click.option('--config_path', '-c', default=os.path.join(os.getcwd(),'gptty.ini'), help="Path to config file.")
@click.option('--additional_context', '-a', default="", help="Pass more context to your questions.")
@click.option('--question', '-q', multiple=True, help='Repeatable list of questions.')
@click.option('--tag', '-t', default="", help='Tag to categorize your query. [optional]')
@click.option('--verbose', '-v', is_flag=True, help="Show debug data.")
@click.option('--json', '-j', is_flag=True, help="Return query as JSON object.")
@click.option('--quiet', is_flag=True, help="Don't write to stdout.")
def query(config_path:str, additional_context:str, question:str, tag:str, verbose:bool, json:bool, quiet:bool):
  """
  Submit a gptty query
  """

  asyncio.run(query_async_wrapper(config_path, question, tag, additional_context, verbose, json, quiet))


async def query_async_wrapper(config_path:str, question:str, tag:str, additional_context:str, verbose:bool, json:bool, quiet:bool):

  if not os.path.exists(config_path):
      click.echo(f"{RED}FAILED to access app config file at {config_path}. Are you sure this is a valid config file? Run `gptty chat --help` for more information.")
      return

  # load the app configs
  configs = get_config_data(config_file=config_path)

  # Here, we verify that we have a wifi connection and if not, exit
  if not has_internet_connection(configs['verify_internet_endpoint']):
    click.echo(f"{RED}FAILED to verify connection at {configs['verify_internet_endpoint']}. Are you sure you are connected to the internet?")
    return

  # create the output file if it doesn't exist
  with open (configs['output_file'], 'a'): pass

  # Authenticate with OpenAI using your API key
  # click.echo (configs['api_key'])
  if configs['api_key'].rstrip('\n') == "":
      click.echo(f"{RED}FAILED to initialize connection to OpenAI. Have you added an API token? See gptty docs <https://github.com/signebedi/gptty#configuration> or <https://platform.openai.com/account/api-keys> for more information.")
      return

  if len(questions) < 1 or not isinstance(questions, tuple):
      click.echo(f"{RED}FAILED to query ChatGPT. Did you forget to ask a question? Run `gptty chat --help` for more information.")
      return

  await run_query(questions=question, tag=tag, configs=configs, additional_context=additional_context, config_path=config_path, verbose=verbose, return_json=json, quiet=quiet)


@click.command()
@click.option('--config_path', '-c', default=os.path.join(os.getcwd(),'gptty.ini'), help="Path to config file.")
def log(config_path):
  """
  Get log of past queries
  """
  # load the app configs
  configs = get_config_data(config_file=config_path)
  
  # create the output file if it doesn't exist
  with open (configs['output_file'], 'a'): pass

  if not os.path.exists(config_path):
      click.echo(f"{RED}FAILED to access app config file at {config_path}. Are you sure this is a valid config file? Run `gptty chat --help` for more information.")
      return


  df = return_log_as_df(configs)

  click.echo(df)



main.add_command(chat)
main.add_command(query)
main.add_command(log)

if __name__ == "__main__":
  main()
