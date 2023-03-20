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

import asyncio

# app specific requirements
from config import get_config_data
from gptty import create_chat_room

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
title = r"""
               _   _         
   ____ _____ | | | |        
  / __ `/ __ \| |_| |_ _   _ 
 / /_/ / /_/ /| __| __| | | |
 \__, / .___/ | |_| |_| |_| |
/____/_/       \__|\__|\__, |
                        __/ |
                       |___/ 
"""

# Print the text in cyan
print(f"{CYAN}{title}\nWelcome to gptty (v.{__version__}), a ChatGPT wrapper for your CLI.\nWritten by Sig Janoska-Bedi <signe@atreeus.com> under the {__license__} license.{RESET}\n")

# load the app configs
configs = get_config_data()

# create the output file if it doesn't exist
with open (configs['output_file'], 'a'): pass

# Run the main coroutine
asyncio.run(create_chat_room(configs=configs))


