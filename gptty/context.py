__name__ = "gptty.context"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.2.2"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

from textblob import TextBlob
from collections import Counter, defaultdict
from nltk.corpus import stopwords


def return_most_common_phrases(text:str, weight_recent=True) -> list:

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

def get_context(tag:str, max_context_length:int, output_file:str, context_keywords_only:bool=True, model_type:str=None, question:str=None) -> str:

    if len(tag) < 1:
        return [{"role": "user", "content": question}] if model_type == 'v1/chat/completions' else "" 


    with open (output_file,'r') as f:
        text = f.readlines()
    

    if model_type == 'v1/chat/completions':
        context = []

        for row in text:
            data = row.replace('\n','').split('|')

            # verifying the length of 
            if (sum(len(item["content"].split()) for item in context) + len(data[2].split()) + len(data[3].split())) > max_context_length:
                break

            if data[1] == tag:
                context.append({"role": "user", "content": data[2]})
                context.append({"role": "assistant", "content": data[3]})

        context.append({"role": "user", "content": question})
        # print(f'[debug]\nlength: {sum(len(item["content"].split()) for item in context)}\ntext: {context}') # debug - print the context to see what it looks like

    else:
        context = ""
        for row in text:
            data = row.replace('\n','').split('|')

            if data[1] == tag:
                for item in data[3].split():
                    # if len(context.split()) >= (max_context_length):
                    #     break
                    context += ' ' + item    

                # ugh ... need to find a better way to handle this.   
                if not context_keywords_only:
                    c = ""

                    for item in context.split():
                        if not len(c.split()) >= (max_context_length): 
                            break
                        c += item

                    context = c

        if context_keywords_only:

            # here we overwrite the context string with just a list of keywords ... though this might 
            # result in suboptimal results without the full sentences ..
            phrases = return_most_common_phrases(context)
            context = ""

            for phrase in phrases:
                # somewhat complex logic ... what we are asking, is whether the additional
                # phrase will push our context over the character limit.
                if len (context.split()) > ( max_context_length - len (phrase.split()) ):
                    break
                context += " " + phrase

        # print(f'[debug]\nlength: {len(context.split())}\ntext: {context}') # debug - print the context to see what it looks like
        context = context + ' ' + question
    
    # from pprint import pprint
    # pprint(context)
    return context