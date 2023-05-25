Module gptty
============

Sub-modules
-----------
* gptty.config
* gptty.context
* gptty.gptty
* gptty.tagging

Classes
-------

`UniversalCompletion(api_key: str = '', org_id: str = '', output_file: str = 'output.txt', your_name: str = 'question', gpt_name: str = 'response', model: str = 'text-davinci-003', temperature: float = 0.0, max_tokens: int = 250, max_context_length: int = 150, context_keywords_only: bool = True, preserve_new_lines: bool = False)`
:   Initializes a new instance of the UniversalCompletion class.
    
Parameters:
    api_key (str): The OpenAI API key.
    org_id (str): The OpenAI organization ID.
    output_file (str): The name of the file where the output should be stored.
    your_name (str): The name that will be used to identify user inputs in the chat history.
    gpt_name (str): The name that will be used to identify GPT outputs in the chat history.
    model (str): The name of the model to use for generating text.
    temperature (float): The temperature to use for the text generation process. Higher values make output more random.
    max_tokens (int): The maximum number of tokens in the output text.
    max_context_length (int): The maximum number of tokens in the input text.
    context_keywords_only (bool): If True, only keywords from the input text are taken into account in the generation process.
    preserve_new_lines (bool): If True, new lines in the output text are preserved.

Returns:
    None

### Methods

`a_fetch_response(self, prompt: Union[str, List[Dict[str, str]]], max_tokens: Optional[int] = None, temperature: Optional[float] = None, model_type: Optional[str] = None) ‑> Union[openai.api_resources.completion.Completion, openai.api_resources.chat_completion.ChatCompletion, None]`
:   Asynchronously fetches a response from the model based on the provided prompt.

    Parameters:
        prompt (Union[str, List[Dict[str, str]]]): The input prompt for the model. This can either be a string or a list of message dictionaries for chat models.
        max_tokens (Optional[int]): The maximum number of tokens for the model to generate. Defaults to None, in which case it uses the instance's default.
        temperature (Optional[float]): The randomness factor for the model's output. Defaults to None, in which case it uses the instance's default.
        model_type (Optional[str]): The type of the model. Defaults to None, in which case it uses the instance's default.

    Returns:
        Optional[Union[openai.Completion, openai.ChatCompletion]]: The model's response as a Completion or ChatCompletion object, or None if the model type is not recognized.

    Example usage:
        >>> g = UniversalCompletion(api_key="your-api-key", org_id="your-org-id")
        >>> g.connect()
        >>> g.set_model('gpt-3.5-turbo')
        >>> prompt = [{"role": "user", "content": "What is an abstraction?"}]
        >>> response = asyncio.run(g.a_fetch_response(prompt=prompt))
        >>> print(response.choices[0].message['content'])

`build_context(self, prompt: str, context: List[Dict[str, str]], max_context_length: int, model_type: Optional[str] = None, context_keywords_only: bool = True, additional_context: str = '') ‑> Union[str, List[Dict[str, str]]]`
:   Builds a full query context for a given prompt and context.

    Parameters:
        prompt (str): The main prompt to build the context around.
        context (List[Dict[str, str]]): List of past prompts and responses.
        max_context_length (int): Maximum length of the context to return.
        model_type (Optional[str]): Type of the language model. If 'v1/chat/completions', return a list of dicts 
                                    with 'role' and 'content' keys. If not, return a string. Default is None.
        context_keywords_only (bool, optional): If True, use only the most common phrases and words from the context 
                                                and additional context. Default is True.
        additional_context (str, optional): Additional context to add to the context. Default is an empty string.

    Returns:
        Union[str, List[Dict[str, str]]]: If `model_type` is 'v1/chat/completions', returns a list of dicts with 
                                          'role' and 'content' keys. If not, returns a string.

`connect(self, api_key=None, org_id=None) ‑> None`
:   Connects to the OpenAI API using the provided organization ID and API key.

    Parameters:
        api_key (str): The OpenAI API key, defaults to the corresponding class element.
        org_id (str): The OpenAI organization ID, defaults to the corresponding class element.

    Returns:
        None

`fetch_response(self, prompt: Union[str, List[Dict[str, str]]], max_tokens: Optional[int] = None, temperature: Optional[float] = None, model_type: Optional[str] = None) ‑> Union[openai.api_resources.completion.Completion, openai.api_resources.chat_completion.ChatCompletion, None]`
:   Fetches a response from the model based on the provided prompt.

    Parameters:
        prompt (Union[str, List[Dict[str, str]]]): The input prompt for the model. This can either be a string or a list of message dictionaries for chat models.
        max_tokens (Optional[int]): The maximum number of tokens for the model to generate. Defaults to None, in which case it uses the instance's default.
        temperature (Optional[float]): The randomness factor for the model's output. Defaults to None, in which case it uses the instance's default.
        model_type (Optional[str]): The type of the model. Defaults to None, in which case it uses the instance's default.

    Returns:
        Optional[Union[openai.Completion, openai.ChatCompletion]]: The model's response as a Completion or ChatCompletion object, or None if the model type is not recognized.

    Example usage:
        >>> g = UniversalCompletion(api_key="your-api-key", org_id="your-org-id")
        >>> g.connect()
        >>> g.set_model('gpt-3.5-turbo')
        >>> prompt = [{"role": "user", "content": "What is an abstraction?"}]
        >>> response = g.fetch_response(prompt=prompt)
        >>> print(response.choices[0].message['content'])

`get_available_models(self) ‑> List[str]`
:   Retrieves a list of available models from the OpenAI API.

    Parameters:
        None

    Returns:
        List[str]: A list of model IDs available for use.

`is_valid_model(self, model_name: str) ‑> bool`
:   Checks whether the given model name is valid and available.

    Parameters:
        model_name (str): The name of the model to validate.

    Returns:
        bool: True if the model name is valid and available, False otherwise.

`set_model(self, model_name: str) ‑> None`
:   Sets the model to be used for the class instance. The model name provided must be a valid and available model.

    Parameters:
        model_name (str): The name of the model to set.

    Returns:
        None

    Raises:
        AssertionError: If the model name is not valid or available.

`usage_stats_today(self) ‑> Optional[Tuple[int, int, int]]`
:   Retrieves usage statistics for the current day from the OpenAI API.

    Parameters:
        None

    Returns:
        requests_today (int): The total number of requests made today.
        query_tokens_today (int): The total number of context tokens used in queries today.
        response_tokens_today (int): The total number of generated tokens in responses today.

    If any error occurs during the process, this method will return None.

`validate_model_type(self, model_name: str) ‑> str`
:   Validates the model type based on the model name provided.

    Parameters:
        model_name (str): The name of the model to validate.

    Returns:
        str: The corresponding API endpoint ('v1/completions' or 'v1/chat/completions') based on the model type.

    Raises:
        Exception: If the model name does not match any of the known model types or is not a valid or available model.
