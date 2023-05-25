Module gptty.tagging
====================

Functions
---------

    
`get_tag_from_text(user_input, replacement_string='-')`
:   This function takes a user input and returns the first tag found within square brackets along with the remaining text after the tag. The square brackets are removed from the tag and any spaces within the tag are replaced with the provided replacement string. If no tag is found, an empty string is returned as the tag.
    
    Parameters:
    
        user_input (str): The input string to search for a tag.
        replacement_string (str): The string to replace any spaces within the tag. Defaults to '-' if no replacement string is provided.
    
    Returns:
    
        Tuple: A tuple containing the tag (str) and the remaining text after the tag (str). If no tag is found, the tag will be an empty string.