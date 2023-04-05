__name__ = "gptty.context"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.2.5"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"


import click
import tiktoken
from textblob import TextBlob
from collections import Counter, defaultdict
from nltk.corpus import stopwords


YELLOW = "\033[1;33m"
RESET = "\033[0m"

def get_token_count(s, model_name):

    """
    Returns the number of tokens in a text string encoded using a specified model.

    Args:

        s (str): The input text string.
        model_name (str): The name of the model used for encoding.

    Returns:

        num_tokens (int): The number of tokens in the encoded text string.
    """

    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(s))
    return num_tokens

def return_most_common_phrases(text:str, weight_recent=True) -> list:

    """
    Returns a list of the most common noun phrases in the input text, with an option to weight more recent phrases more heavily.

    Args:
    - text (str): The input text.
    - weight_recent (bool): If True, more recent phrases are weighted more heavily.

    Returns:
    - list: A list of the most common noun phrases in the input text. Each item in the list is a string representing a noun phrase.
    """

    # Extract noun phrases using TextBlob
    blob = TextBlob(text)
    noun_phrases = blob.noun_phrases

    # Remove stopwords from noun phrases
    stop_words = set(stopwords.words('english'))
    filtered_noun_phrases = []
    for np in noun_phrases:
        words = np.split()
        filtered_words = [word for word in words if word not in stop_words]
        if filtered_words:
            filtered_noun_phrases.append(' '.join(filtered_words))

    if not weight_recent:

        # Count the frequency of the noun phrases
        noun_phrase_counts = Counter(filtered_noun_phrases)

        # Get the most frequent key phrases
        return [phrase for phrase, count in noun_phrase_counts.most_common()]

    # Count the weighted frequency of the noun phrases
    noun_phrase_weighted_counts = defaultdict(int)
    total_phrases = len(filtered_noun_phrases)

    for i, phrase in enumerate(filtered_noun_phrases):
        weight = (i + 1) / total_phrases  # Assign a higher weight to phrases that appear later in the text
        noun_phrase_weighted_counts[phrase] += weight

    # Get the most frequent key phrases
    return [phrase for phrase, count in sorted(noun_phrase_weighted_counts.items(), key=lambda x: x[1], reverse=True)]

def get_context(tag: str, 
                max_context_length: int, 
                output_file: str, 
                model_name:str, 
                context_keywords_only: bool = True, 
                additional_context: str = "",
                model_type: str = None, 
                question: str = None, 
                debug: bool = False):


    """
    Returns a full query context for a given tag, question and additional context.
    
    Parameters:
        tag: str
            Tag to identify a conversation with a specific topic
        max_context_length: int
            Maximum length of the context to return.
        output_file: str
            Path to the file to read the context from.
        model_name: str
            Name of the language model to use
        context_keywords_only: bool, optional
            If True, use only the most common phrases and words from the context and additional context.
            Default is True.
        additional_context: str, optional
            Additional context to add to the context.
            Default is an empty string.
        model_type: str, optional
            Type of the language model. If 'v1/chat/completions', return a list of dicts with 'role' and 'content' keys
            If not, return a string.
            Default is None.
        question: str, optional
            Question to add to the context. If None, return only the context.
            Default is None.
        debug: bool, optional
            If True, print debug information.
            Default is False.
    
    Returns:
        If `model_type` is 'v1/chat/completions', returns a list of dicts with 'role' and 'content' keys
        If not, returns a string.
    """


    if len(tag) < 1:
        if model_type == 'v1/chat/completions':

            context = [{"role": "user", "content": question}]

            if len(additional_context) > 0:
                # at this point we've added all the elements to context that we believe we should, so let's add any 
                # additional context that we passed.
                remaining_tokens = max_context_length - len(question)
                context = [{"role": "system", "content": ' '.join(additional_context.split()[:remaining_tokens])}] + context


            if debug:
                click.echo(YELLOW + '-' * 25)
                click.echo(f'[debug]\nmodel: {model_name}\ntokens: {get_token_count(question, model_name)}\nwords: {len(question.split()) }\ntext: {question}') # debug - print the context to see what it looks like
                click.echo('-' * 25 + RESET)
                
            return context

        else:

            if len(additional_context) > 0:

                remaining_tokens = max_context_length - (len(question.split()))
                if remaining_tokens > 0:
                    question = ' '.join(additional_context.split()[:remaining_tokens]) + " " + question


            if debug:
                click.echo(YELLOW + '-' * 25)
                click.echo(f'[debug]\nmodel: {model_name}\ntokens: {get_token_count(question, model_name)}\nwords: {len(question.split())}\ntext: {question}') # debug - print the context to see what it looks like
                click.echo('-' * 25 + RESET)

            return question

    with open(output_file, 'r') as f:
        text = f.read().strip().split('\n')

    if model_type == 'v1/chat/completions':
        context = []

        for row in reversed(text):
            data = [item.strip() for item in row.split('|')]

            if (sum(len(item["content"].split()) for item in context) + len(data[2].split()) + len(data[3].split()) + len(question.split())) > max_context_length:
                break

            if data[1] == tag:
                context = [{"role": "assistant", "content": data[3]}] + context
                context = [{"role": "user", "content": data[2]}] + context

        context.append({"role": "user", "content": question})
        
        if len(additional_context) > 0:
            # at this point we've added all the elements to context that we believe we should, so let's add any 
            # additional context that we passed.
            remaining_tokens = max_context_length - (sum(len(item["content"].split()) for item in context))
            context = [{"role": "system", "content": ' '.join(additional_context.split()[:remaining_tokens])}] + context

        if debug:
            token_count = " ".join([x['content'] for x in context])
            click.echo(YELLOW + '-' * 25)
            click.echo(f'[debug]\nmodel: {model_name}\ntokens: {get_token_count(token_count, model_name)}\nwords: {sum(len(item["content"].split()) for item in context)}\ntext: {context}') # debug - print the context to see what it looks like
            click.echo('-' * 25 + RESET)


    else:
        context = ""
        for row in text:
            data = [item.strip() for item in row.split('|')]

            if data[1] == tag:
                context += ' ' + data[2] + ' ' + data[3]

        if context_keywords_only:
            phrases = return_most_common_phrases(additional_context+context) # here we prepend the context with the additional_context string
            context = "" # maybe not the cleanest way to do this, but we are resetting the context here

            for phrase in phrases:
                if (len(context.split()) + len(phrase.split()) + len(question.split())) > max_context_length:
                    break
                context += " " + phrase

        else:
            c = ""
            context_words = context.split()

            for i in range(len(context_words)):
                if (len(c.split()) + len(question.split())) >= max_context_length:
                    break
                c += ' ' + context_words[i]

            context = c.strip()

            # prepend `context` with `additional_context` if we have any tokens remaining.
            # WARNING - this may create unexpected behavior, especially if a question is 
            # contained within the additional context passed, that may provide seemingly 
            # inexplicable responses.
            remaining_tokens = max_context_length - (len(context.split()) + len(question.split()))
            if remaining_tokens > 0:
                context = ' '.join(additional_context.split()[:remaining_tokens]) + " " + context


        context = context.strip() + ' ' + question
        

        if debug:
            click.echo(YELLOW + '-' * 25)
            click.echo(f'[debug]\nmodel: {model_name}\ntokens: {get_token_count(context, model_name)}\nwords: {len(context.split())}\ntext: {context}') # debug - print the context to see what it looks like
            click.echo('-' * 25 + RESET)

    return context