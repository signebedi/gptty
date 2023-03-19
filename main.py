import time

# Define color codes
CYAN = "\033[1;36m"
RED = "\033[1;31m"
RESET = "\033[0m"

# Continuously send and receive messages
while True:
    # Get user input
    message = input(f"{CYAN}> {RESET}")

    # Send a message to the server
    #client_socket.sendall(message.encode())

    # Receive a message from the server
    #data = client_socket.recv(1024).decode()

    for i in range(10):
        print("." * i + " " * (9 - i), end="", flush=True)
        time.sleep(0.1)
        print("\b" * 10, end="", flush=True)


    data = 'Reponse'

    # Print the question and response in color
    print(f"{CYAN}[question] {message}{RESET}")
    print(f"{RED}[response] {data}{RESET}")

