__name__ = "gptty.context"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.1.3"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

def get_context(tag, max_context_length, output_file):

    if len(tag) < 1:
        return ""

    context = ""
    with open (output_file,'r') as f:
        text = f.readlines()
    
    for row in text:
        data = row.replace('\n','').split('|')

        if data[1] == tag:
            context += data[3]
    
    return context