""" This module contains the GPTModelManager class for managing the GPT model. """
import instructor
from openai import OpenAI
from typing import Any, Dict, Union
from tools.text_response import TextResponse

class GPTModelManager:
    def __init__(self, use_local: bool = False, system_message: str = "I'm an AI assistant here to help you with any questions you have."):
        """
        Initializes a new instance of the GPTModelManager.
        :param use_local: Determines whether to use a local model or an OpenAI model.
        """
        self.use_local = use_local
        self.client = None
        self.initialize_client()
        self.system_message = system_message

    def initialize_client(self):
        """
        Initializes the GPT client based on the configuration.
        """
        if self.use_local:
            self.client = instructor.patch(
                OpenAI(
                    base_url="http://localhost:11434/v1",
                    api_key="ollama",  # Local API key, required but unused
                ),
                mode=instructor.Mode.JSON,
            )

        else:
            self.client = instructor.patch(OpenAI(), mode=instructor.Mode.TOOLS)  # Uses default settings for OpenAI

    def switch_model(self, use_local: bool):
        """
        Switches between local and OpenAI models.
        :param use_local: Determines whether to switch to a local model or an OpenAI model.
        """
        self.use_local = use_local
        self.initialize_client()

    def generate_response(self, data: str, model_settings: Dict[str, Any], response_model: Union[None, Any]=TextResponse):
        """
        Generates a response from the GPT model based on the provided data and model settings.
        :param data: The input data for the GPT model.
        :param model_settings: Settings for the model such as 'model', 'temperature', etc.
        :param response_model: The Pydantic model for structuring the response, if any.
        :return: The response from the GPT model.
        """
        try:
            if self.use_local:
                # Settings for local model
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": data}
                    ],
                    **model_settings,
                    response_model=response_model,
                )
            else:
                # Settings for OpenAI model
                messages = [
                    {"role": "system", "content": self.system_message},
                    {"role": "user", "content": data}
                ]
                self.client = instructor.patch(OpenAI(), mode=instructor.Mode.TOOLS)
                response = self.client.chat.completions.create(
                    messages=messages,
                    **model_settings,
                    response_model=response_model,
                )

        except Exception as e:
            response = TextResponse(response="An error occurred while generating the response.")
            print(f"An error occurred while generating the response: {e}")
             
        return response
