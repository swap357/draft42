"""Shell Function"""
import subprocess

from instructor import OpenAISchema
from pydantic import Field
from typing_extensions import Literal

class ShellCommand(OpenAISchema):
    """
    Executes a shell command and returns the output (result).
    """
    
    command: str = Field(
        ...,
        example="ls -la",
        descriptions="""
        The shell command to execute.
        Must be a valid, safe shell command with a short expected output.
        """,
    )
    
    def process(self) -> str:
        process = subprocess.Popen(
            self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        output, _ = process.communicate()
        output = output.decode("utf-8")[0:2048]
        exit_code = process.returncode
        # construct the response with command executed, exit code and output to be shown on markdown code block
        response = f"```shell\n{self.command}\n\nExit Code: {exit_code}\n\n{output}\n```"
        tool = "shell"
        return response, tool
