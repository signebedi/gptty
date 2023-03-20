user_input = input("Enter some text: ")

assert(len(user_input)>0)

# Initialize the tag and remaining text variables
tag = None
replacement_string='-'
remaining_text = user_input.strip()

# Loop until we find a tag or run out of text
while tag is None and remaining_text != "":
    # Remove leading whitespace and get the first word
    first_word = remaining_text.lstrip().split()[0]

    # Check if the first word starts with '['
    if first_word.startswith('['):
        # Check if the first word ends with ']'
        if first_word.endswith(']'):
            # Get the tag by removing the '[' and ']' characters
            tag = first_word[1:-1].replace(" ", replacement_string)

            # Strip the tag from the remaining text and remove any extra whitespace
            remaining_text = remaining_text[len(first_word):].strip()
        else:
            # The first word doesn't end with ']', so keep appending words to the tag until we find one that does
            tag = first_word[1:].replace(" ", replacement_string)
            remaining_text = remaining_text[len(first_word):].lstrip()

            while "]" not in tag and remaining_text != "":
                # Append the next word to the tag
                next_word = remaining_text.lstrip().split()[0]
                tag += replacement_string+next_word.replace(" ", replacement_string)
                remaining_text = remaining_text[len(next_word):].lstrip()

            # If we found the end of the tag, remove it from the remaining text
            if "]" in tag:
                # Remove the ']' character from the tag and strip any extra whitespace
                tag = tag[:-1].strip()

                # Remove the tag from the remaining text and remove any extra whitespace
                remaining_text = remaining_text[len(tag) + 2:].strip()
            else:
                # We ran out of text before finding the end of the tag
                tag = None
    else:
        # The text doesn't start with a tag
        tag = None
        break

# Output the tag and remaining text, if we found a tag
if tag is not None:
    print("Tag:", tag)
    print("Remaining text:", remaining_text)
else:
    print("Input does not start with a tag.")