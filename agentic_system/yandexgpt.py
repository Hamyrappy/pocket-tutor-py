import os
from typing import Optional

import requests

import warnings

class YandexGPT2LangchainOutput():
    '''class to convert YandexGPT-type output to Langchain-type output. Currently just a dummy with .content attribute'''
    def __init__(self, response) -> None:
        response_data = response.json()
        self.content = response_data["result"]["alternatives"][0]["message"]["text"]

class YandexGPTFinetuned():
    """Class for custom finetuned YandexGPT model. See more on https://yandex.cloud/en-ru/docs/foundation-models/concepts/yandexgpt/models"""

    def __init__(
        self,
        IAM_token: str,
        folder_id: str,
        model_id: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.6,
        max_tokens: int = 2000,
    ) -> None:
        self.system_prompt = system_prompt
        self.messages = []
        self.api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {IAM_token}",
            "x-folder-id": folder_id,
        }
        if model_id == 'lite':
            self.model_url = f'gpt://{folder_id}/yandexgpt-lite/latest'
        else:
            self.model_url = f'ds://{model_id}'
        self.completion_options = {
            "stream": False,
            "temperature": temperature,
            "maxTokens": str(max_tokens),
        }

    def invoke(self, user_message: str, clear_history: bool = True) -> YandexGPT2LangchainOutput:
        if clear_history:
            self.messages = []
            if self.system_prompt:
                self.messages.append({"role": "system", "text": self.system_prompt})

        self.messages.append({"role": "user", "text": user_message})

        json_request = {
            "modelUri": self.model_url,
            "completionOptions": self.completion_options,
            "messages": self.messages,
        }

        response = requests.post(self.api_url, headers=self.headers, json=json_request)
        if response.status_code != 200:
            warnings.warn("Execution aborted due to error. \n Response returned with code {} and text /n{}".format(response.status_code, response.text))
            return None
        assistant_message = YandexGPT2LangchainOutput(response)
        self.messages.append({"role": "assistant", "text": assistant_message.content})
        return assistant_message