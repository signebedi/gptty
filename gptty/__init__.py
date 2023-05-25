__name__ = "gptty"
__author__ = "Sig Janoska-Bedi"
__credits__ = ["Sig Janoska-Bedi"]
__version__ = "0.2.6"
__license__ = "MIT"
__maintainer__ = "Sig Janoska-Bedi"
__email__ = "signe@atreeus.com"

from gptty import (
    config, 
    context, 
    gptty, 
    tagging
)

import openai
from datetime import datetime
import pandas as pd
import json
import asyncio
import click

class UniversalCompletion:
    def __init__(   self, 
                    api_key="", 
                    org_id="",
                    output_file="output.txt",
                    your_name="question",
                    gpt_name="response",
                    model="text-davinci-003",
                    temperature=0.0,
                    max_tokens=250,
                    max_context_length=150,
                    context_keywords_only=True,
                    preserve_new_lines=False,
                ):

        self.api_key = api_key
        self.org_id = org_id
        self.output_file = output_file
        self.your_name = your_name
        self.gpt_name = gpt_name
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_context_length = max_context_length
        self.context_keywords_only = context_keywords_only
        self.preserve_new_lines = preserve_new_lines
        
    def connect(self):
        openai.organization = self.org_id.rstrip('\n')
        openai.api_key = self.api_key.rstrip('\n')


    def usage_stats_today(self):
        try:
            r = openai.api_requestor.APIRequestor(self.api_key)
            resp = r.request("GET", f'/usage?date={datetime.now().strftime("%Y-%m-%d")}')
            resp_object = resp[0].data
        except:
            return None

        requests_today = sum(item["n_requests"] for item in resp_object['data'])
        query_tokens_today = sum(item["n_context_tokens_total"] for item in resp_object['data'])
        response_tokens_today = sum(item["n_generated_tokens_total"] for item in resp_object['data'])

        return requests_today, query_tokens_today, response_tokens_today

    def get_available_models(self):
        response = openai.Model.list()
        return [model.id for model in response['data']]

    def is_valid_model(self, model_name):
        available_models = self.get_available_models()
        return model_name in available_models

    def set_model(self, model_name):
        assert self.is_valid_model(model_name)
        self.model = model_name

    def validate_model_type(self, model_name):
        if ('davinci' in model_name or 'curie' in model_name) and self.is_valid_model(model_name):
            return 'v1/completions'
        elif 'gpt' in model_name and self.is_valid_model(model_name):
            return 'v1/chat/completions'
        raise Exception()

    async def a_fetch_response(self, prompt, max_tokens=None, temperature=None, model_type=None):
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        temperature = temperature if temperature is not None else self.temperature
        model_type = model_type if model_type is not None else self.validate_model_type(self.model)

        if model_type == 'v1/completions':
            return await openai.Completion.acreate(
                engine=self.model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                n=1,
                stop=None,
                timeout=15,
            )
        if model_type == 'v1/chat/completions':
            return await openai.ChatCompletion.acreate( 
                model = self.model,
                messages = prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                n=1,
                stop=None,
                timeout=15,
            )

        return None

    def fetch_response(self, prompt, max_tokens=None, temperature=None, model_type=None):
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        temperature = temperature if temperature is not None else self.temperature
        model_type = model_type if model_type is not None else self.validate_model_type(self.model)

        if model_type == 'v1/completions':
            return openai.Completion.create(
                engine=self.model,
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                n=1,
                stop=None,
                timeout=15,
            )
        if model_type == 'v1/chat/completions':
            return openai.ChatCompletion.create( 
                model = self.model,
                messages = prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                n=1,
                stop=None,
                timeout=15,
            )

        return None

