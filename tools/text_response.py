""" This module contains the TextResponse class, which represents a response from a GPT model, including additional metadata for context and debugging. """
from instructor import OpenAISchema
from pydantic import Field
from typing import Optional, List

class TextResponse(OpenAISchema):
    """
    Represents a response from a GPT model, including additional metadata for context and debugging.
    """

    response: str = Field(
        ...,
        example="Hello, how can I help you?",
        description="The response from the GPT model.",
    )
    
    # currently not used, but can be used to provide additional context to the response
    significant_context: Optional[List[str]] = Field(
        [],
        example=["User's name is John Doe", 
                 "User does not like being told what to do", 
                 "response using function 'cpu-usage' is more preferred by user over 'shell' for cpu usage queries"],
        description="The significant context from the conversation that may affect the response.",
    )

    def process(self) -> str:
        
        tool = "text"
        return self.response, tool
