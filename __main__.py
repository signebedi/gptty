import time
import asyncio
import aiohttp
import json
from typing import Optional



__name__ = "gptty"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.1.0"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

# Define color codes
CYAN = "\033[1;36m"
RED = "\033[1;31m"
RESET = "\033[0m"


title = f"""  
   _____ _____ _______ _________     __
  / ____|  __ \__   __|__   __\ \   / /
 | |  __| |__) | | |     | |   \ \_/ / 
 | | |_ |  ___/  | |     | |    \   /  
 | |__| | |      | |     | |     | |   
  \_____|_|      |_|     |_|     |_|   
                                     
Welcome to GPTTY (v.{__version__}), a ChatGPT wrapper for your CLI.
Written by Sig Janoska-Bedi <signe@atreeus.com> under the {__license__} license.
"""

# Print the text in cyan
print(f"{CYAN}{title}{RESET}")


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



async def create_chat_room(url="http://0.0.0.0:8080"):

    # Create a session object
    async with aiohttp.ClientSession() as session:
        # Continuously send and receive messages
        while True:
            # Get user input
            question = input(f"{CYAN}> ")

            # Query the API asynchronously
            response = None
            while not response:

                # Show the waiting graphic
                for i in range(10):
                    print("." * i + " " * (9 - i), end="", flush=True)
                    time.sleep(0.1)
                    print("\b" * 10, end="", flush=True)

                # Query the API
                response = await query_api(session, url, question)

            # We expect a json object, which we unpack here
            response = json.loads(response)

            # print the question in color
            print(f"{CYAN}[question] {question}{RESET} \n", end="", flush=True)

            # Print the response in color
            print(f"\b{RED}[response] {response['response']}{RESET}\n")

# Run the main coroutine
asyncio.run(create_chat_room())


