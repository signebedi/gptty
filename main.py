import time
import asyncio
import aiohttp
import json

# Define color codes
CYAN = "\033[1;36m"
RED = "\033[1;31m"
RESET = "\033[0m"

# Define async API call function
async def make_request(session, url, message):
    async with session.post(url, data=message) as response:
        return await response.text()


title = """  
   _____ _____ _______ _________     __
  / ____|  __ \__   __|__   __\ \   / /
 | |  __| |__) | | |     | |   \ \_/ / 
 | | |_ |  ___/  | |     | |    \   /  
 | |__| | |      | |     | |     | |   
  \_____|_|      |_|     |_|     |_|   
                                     
Welcome to GPTTY, a ChatGPT wrapper for your CLI
Written by Sig Janoska-Bedi <https://github.com/signebedi/gptty>

"""

# Print the text in cyan
print(f"{CYAN}{title}{RESET}")


async def main(url="http://0.0.0.0:8080"):

    # Create a session object
    async with aiohttp.ClientSession() as session:
        # Continuously send and receive messages
        while True:
            # Get user input
            message = input(f"{CYAN}> {RESET}")

            # Show a graphic while waiting for a response
            print(f"{CYAN}[question] {message}{RESET} \n", end="", flush=True)
            for i in range(3):
                print("." * i + " " * (9 - i), end="", flush=True)
                time.sleep(0.1)
                print("\b" * 10, end="", flush=True)

            # Send a message to the API
            response = await make_request(session, url, message)

            # We expect a json object, which we unpack here
            response = json.loads(response)

            # Print the response in color
            print(f"\b{RED}[response] {response['response']}{RESET}\n")

# Run the main coroutine
asyncio.run(main())






# # Continuously send and receive messages
# while True:
#     # Get user input
#     message = input(f"{CYAN}> {RESET}")

#     # Send a message to the server
#     #client_socket.sendall(message.encode())

#     # Receive a message from the server
#     #data = client_socket.recv(1024).decode()

#     for i in range(10):
#         print("." * i + " " * (9 - i), end="", flush=True)
#         time.sleep(0.1)
#         print("\b" * 10, end="", flush=True)


#     data = 'Reponse'

#     # Print the question and response in color
#     print(f"{CYAN}[question] {message}{RESET}")
#     print(f"{RED}[response] {data}{RESET}")

