from pydantic import BaseModel, Field
from typing import Union

from tools.shell import ShellCommand
from tools.text_response import TextResponse
from instructor import OpenAISchema

class Tools(OpenAISchema):
    """
    Represents a response from a GPT model, including additional metadata for context and debugging.
    """
    
    action: Union[ShellCommand, TextResponse] = Field(
        ...,
        description="Best function to respond to user's query, use text_response for most cases and other functions for specific use cases."
    )

    def process(self):
        """Process the action."""
        output = self.action.process()
        # restrict the output to limited openai tokens length, some might be less than 4096
        output = output[:4096]
        return output