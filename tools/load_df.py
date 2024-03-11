
import pandas as pd

from instructor import OpenAISchema
from pydantic import Field

class LoadDataFrame(OpenAISchema):
    """
    Loads data from a CSV file into a DataFrame.
    """
    
    file_path: str = Field(
        ...,
        example="data/sample.csv",
        description="""
        The path to the CSV file to load.
        Must be a valid path to a .csv file.
        """,
    )
    
    def process(self) -> str:
        try:
            df = pd.read_csv(self.file_path)
            response = f"Data loaded successfully from {self.file_path}."
            tool = "load_df"
            return response, tool
        except Exception as e:
            response = f"Failed to load data from {self.file_path}. Error: {str(e)}"
            tool = "load_df"
            return response, tool
