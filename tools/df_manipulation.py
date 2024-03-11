from instructor import OpenAISchema
from pydantic import Field
from typing import List, Dict, Union

class FilterOperation(OpenAISchema):
    """
    Represents a filtering operation on a DataFrame.
    """
    column: str = Field(..., 
            description="The column to apply the filter on.")
    operation: str = Field(..., 
            examples=["equals", "greater_than", "less_than", "between"],
            description="The operation to perform (e.g., 'equals', 'greater_than').")
    value: List[Union[str, int, float]] = Field(..., 
            description="A list of values to compare against. For 'equals', 'greater_than', 'less_than' operations, use one value. "
            "For 'between', use two values representing the lower and upper bounds.")
    value_type: str = Field(..., 
            description="The type of the value to compare against (e.g., 'string', 'number').")

class CleanOperation(OpenAISchema):
    """
    Represents a data cleaning operation on a DataFrame.
    """
    column: str = Field(..., 
            description="The column to clean.")
    method: str = Field(..., 
            description="The cleaning method (e.g., 'fill_missing', 'drop').")
    value: Union[str, int, float, None] = Field(None, 
            description="The value to use for filling missing data, if applicable.")
    value_type: str = Field(..., 
            description="The type of the value to use for filling missing data, if applicable (e.g., 'string', 'number').")
    
class DeriveOperation(OpenAISchema):
    """
    Represents an operation to derive a new column from existing columns.
    """
    new_column: str = Field(..., 
            description="The name of the new column to create.")
    operation: str = Field(..., 
            description="The operation to perform (e.g., 'add', 'subtract').")
    columns: List[str] = Field(..., 
            description="The columns to use in the operation.")
    value_type: str = Field(..., 
            description="The type of the value to use for filling missing data, if applicable (e.g., 'string', 'number').")

class UniqueFilterOperation(OpenAISchema):
    """
    Represents an operation to filter DataFrame rows based on unique values in a column.
    """
    column: str = Field(..., description="The column to filter by unique values.")

class DataFrameManipulation(OpenAISchema):
    """
    Encapsulates instructions for manipulating a DataFrame.
    """
    files: List[str] = Field([], 
            description="A list of file paths to read into a DataFrame for query.")
    filters: List[FilterOperation] = Field([], 
            description="A list of filtering operations by which to filter the DataFrame.")
    cleans: List[CleanOperation] = Field([], 
            description="A list of cleaning operations to apply to the DataFrame.")

