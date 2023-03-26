# gptty

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/signebedi/gptty/blob/master/LICENSE)

Chat GPT wrapper in your TTY

## Installation

You can install `gptty` on pip

```
pip install gptty
```

Now, you can run the chat with `gptty`.


You can also install from git:

```
cd ~/Code # replace this with whatever directory you want to use
git clone https://github.com/signebedi/gptty.git
cd gptty/

# now install the requirements
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# now run it (make sure your virtualenv is running)
python gptty
```

If you experience an error, try [configuring](#configuration) the app.

## Configuration

`gptty` reads configuration settings from a file named `gptty.ini`, which should be located in the same directory that you are running `gptty` from. The file uses the INI file format, which consists of sections, each with its own key-value pairs.

| Key    | Type | Default Value    | Description |
| -------- | ------- | -------- | ------- |
| api_key  | String    | ""  |   The API key for OpenAI's GPT service  |
| gpt_version | String     | "3" |    The version of GPT to use  |
| your_name    | String    | "question"    |   The name of the input prompt  |
| gpt_name  | String    | "response"  |   The name of the generated response  |
| output_file | String     | "output.txt" |    The name of the file where the output will be saved  |
| model    | String    | "text-davinci-003"    |   The name of the GPT model to use  |
| temperature  | Float    | 0.0  |   The temperature to use for sampling  |
| max_tokens | Integer     | 250 |    The maximum number of tokens to generate for the response  |
| max_context_length    | Integer    | 5000    |   The maximum length of the input context  |


You can modify the settings in the configuration file to suit your needs. If a key is not present in the configuration file, the default value will be used. The [main] section is used to specify the program's settings. 

```ini
[main]
api_key=my_api_key
```

The application provides a sample configuration file `gptty.ini.example` that you can use as a starting point. 

## Usage

#### Chat

The chat feature provides an interactive chat interface to communicate with ChatGPT. You can ask questions and receive responses in real-time, while maintaining context.

To start the chat interface, run `gptty chat`. You can also specify a custom configuration file path by running `gptty chat --config_path /path/to/your/gptty.ini`.Inside the chat interface, you can type your questions or commands directly. To view the list of available commands, type `:help`, which will show the following options.

| Metacommand    | Description    | 
| -------- | ------- | 
| :help | Display a list of available commands and their descriptions.   |
| :quit | Exit ChatGPT.   |
| :logs | Display the current configuration settings.   |
| :context[a:b] | Display the context history, optionally specifying a range a and b. *Under development*   |

To use a command, simply type it into the command prompt and press Enter. For example, use the following command to display the current configuration settings in the terminal:

```
> :configs

api_key: SOME_CONFIG_HERE
gpt_version: 3
your_name: question
gpt_name: response
output_file: output.txt
model: text-davinci-003
temperature: 0.0
max_tokens: 250
max_context_length: 5000
```

You can type a question into the prompt anytime, and it will generate a response for you. If you'd like to share context across queries, see the [context](#context) section below.

#### Query

The query feature allows you to submit a single or multiple questions to ChatGPT and receive the answers directly in the command line.

To use the query feature, run something like `gptty query --question "What is the capital of France?" --question "What is the largest mammal?"`. You can also provide an optional tag to categorize your query: `gptty query --question "What is the capital of France?" --tag "geography"`. You can specify a custom configuration file path if needed: `gptty query --config_path /path/to/your/gptty.ini --question "What is the capital of France?"`.

Remember that gptty uses a configuration file (by default gptty.ini) to store settings like API keys, model configurations, and output file paths. Make sure you have a valid configuration file before running gptty commands.

## Context

Tagging text for context when writing a query on this app can help improve the accuracy of the generated response. Here are the steps to follow:

1. Identify the context of your question or statement. 
2. Assign a tag to that context. The tag can be a word or short phrase that describes the context like `bananas` or `shakespeare`.
3. Include the tag in your input message by prefixing it with `[tag]`. For example, if the context of your question is "cooking," you can tag it as `[cooking]`.
Make sure to use the same tag consistently for all related queries.
4. The application will save your tagged question and response in the output file specified in the code output file.
5. When asking subsequent questions on the same topic, provide the tag in your input message in order to retrieve the relevant context for the generated response.

Here is an example of what this might look like, using questions tagged as `[shakespeare]`. Notice how, in the second question, the name 'William Shakespeare' is not mentioned at all.

![context example](assets/context_example.png)
