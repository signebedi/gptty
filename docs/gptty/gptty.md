Module gptty.gptty
==================

Functions
---------

    
`create_chat_room(configs={'api_key': '', 'org_id': '', 'your_name': 'question', 'gpt_name': 'response', 'output_file': 'output.txt', 'model': 'gpt-4-0314', 'temperature': 0.0, 'max_tokens': 1500, 'max_context_length': 1000, 'context_keywords_only': True, 'preserve_new_lines': True, 'verify_internet_endpoint': 'google.com'}, log_responses: bool = True, config_path=None, verbose: bool = False)`
:   This function creates a chat room using the OpenAI API to generate responses to user inputs. 
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

    
`fetch_response(prompt, model_engine, max_tokens, temperature, model_type)`
:   This module provides a function to fetch a response from the OpenAI API based on the given prompt and model specifications.
    
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

    
`get_available_models()`
:   Returns:
        - List: list of available OpenAI model IDs.

    
`is_valid_model(model_name)`
:   Validates whether a given model name is available in the OpenAI platform.
    
    Parameters:
    - model_name (str): The name of the model to validate.
    
    Returns:
    - bool: True if the model name is available, False otherwise.

    
`run_query(questions: list, tag: str, configs={'api_key': '', 'org_id': '', 'your_name': 'question', 'gpt_name': 'response', 'output_file': 'output.txt', 'model': 'gpt-4-0314', 'temperature': 0.0, 'max_tokens': 1500, 'max_context_length': 1000, 'context_keywords_only': True, 'preserve_new_lines': True, 'verify_internet_endpoint': 'google.com'}, additional_context: str = '', log_responses: bool = True, config_path=None, verbose: bool = False, return_json: bool = False, quiet: bool = False)`
:   This function is used to run a query command using OpenAI. 
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

    
`usage_stats_today()`
:   

    
`validate_model_type(model_name)`
:   Validates whether a given model name is a supported model type for OpenAI API completion requests.
    
    Parameters:
    - model_name (str): The name of the model to validate.
    
    Returns:
    - str: The API endpoint to use for completion requests if the model name is valid and supported.
    
    Raises:
    - Exception: If the model name is not valid or not supported.

    
`wait_graphic()`
:   This module provides a function to display a wait graphic while awaiting responses.
    
    Returns:
    - None