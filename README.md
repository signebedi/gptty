# gptty
Chat GPT wrapper in your TTY

## Installation

On linux, run:

```
cd ~/Code # replace this with whatever directory you want to use
git clone https://github.com/signebedi/gptty.git

# now install the requirements
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# now run it (make sure your venv is running)
cd ~/Code # replace this with whatever directory you want to use
python gptty
```

If you experience an error, try [configuring](#configuration) the app.

## Configuration

`gptty` reads configuration settings from a file named gptty.ini located in the same directory as the main script. The file uses the INI file format, which consists of sections, each with its own key-value pairs.

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

## Context

Tagging text for context when writing a query on this app can help improve the accuracy of the generated response. Here are the steps to follow:

1. Identify the context of your question or statement. 
2. Assign a tag to that context. The tag can be a word or short phrase that describes the context like `bananas` or `shakespeare`..
3. Include the tag in your input message by prefixing it with `[tag]`. For example, if the context of your question is "cooking," you can tag it as `[cooking]`.
Make sure to use the same tag consistently for all related queries.
4. The application will save your tagged question and response in the output file specified in the code output file.
5. When asking subsequent questions on the same topic, provide the tag in your input message in order to retrieve the relevant context for the generated response.

Here is an example of what this might look like, using questions tagged as `[shakespeare]`. Notice how, in the second question, the name 'William Shakespeare' is not mentioned at all.

![context example](assets/context_example.png)
