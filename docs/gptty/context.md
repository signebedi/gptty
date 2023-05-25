Module gptty.context
====================

Functions
---------

    
`get_context(tag: str, max_context_length: int, output_file: str, model_name: str, context_keywords_only: bool = True, additional_context: str = '', model_type: str = None, question: str = None, debug: bool = False)`
:   Returns a full query context for a given tag, question and additional context.
    
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

    
`get_token_count(s, model_name)`
:   Returns the number of tokens in a text string encoded using a specified model.
    
    Args:
    
        s (str): The input text string.
        model_name (str): The name of the model used for encoding.
    
    Returns:
    
        num_tokens (int): The number of tokens in the encoded text string.

    
`return_most_common_phrases(text: str, weight_recent=True) ‑> list`
:   Returns a list of the most common noun phrases in the input text, with an option to weight more recent phrases more heavily.
    
    Args:
    - text (str): The input text.
    - weight_recent (bool): If True, more recent phrases are weighted more heavily.
    
    Returns:
    - list: A list of the most common noun phrases in the input text. Each item in the list is a string representing a noun phrase.