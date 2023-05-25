Module gptty.config
===================

Functions
---------

    
`get_config_data(config_file='gptty.ini')`
:   The get_config_data() function reads a configuration file and returns a dictionary containing the parsed data. 
    If the configuration file does not exist or does not contain a particular key, a default value is used. 
    The default configuration values are defined in the function itself. 
    By default, the function reads the gptty.ini configuration file, but you can specify a different file name by passing it as an argument.
    
    The returned dictionary has the following keys:
    
        api_key: An API key used to authenticate with the OpenAI API.
        your_name: The name of the user (you) who is running the program.
        gpt_name: The name of the GPT model to use.
        output_file: The name of the output file to write the generated text to.
        model: The ID of the GPT model to use.
        temperature: The temperature value to use when generating text.
        max_tokens: The maximum number of tokens to generate in the generated text.
        max_context_length: The maximum number of tokens to use as context when generating text.
        context_keywords_only: A boolean value indicating whether to use only the keywords in the context when generating text.
        preserve_new_lines: A boolean value indicating whether to preserve new lines in the generated text.
        verify_internet_endpoint: The internet endpoint to use when verifying the internet connection.
    
    Note: This function uses the configparser module to parse configuration files.