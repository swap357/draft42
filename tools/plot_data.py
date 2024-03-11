"""
Plotly plot function class 
"""

from instructor import OpenAISchema
from pydantic import Field
from typing import List, Optional  # Updated to include Optional

class PlotData(OpenAISchema):
    """
    A class to represent the data needed to create a plotly plot, extended to support filtering, coloring, and labeling.
    """
    file_path: str = Field(
        ...,
        description="The path to the csv file."
    )
    x: str = Field(
        ...,
        description="A column header of dataframe, where each header is used as the x values for a trace."
    )
    y: List[str] = Field(
        ...,
        description="A list of column headers of dataframe, where each header is used as the y values for a trace."
    )
    titles: List[str] = Field(
        ...,
        description="A list of titles, one for each trace."
    )
    secondary_y: bool = Field(
        False,
        description="A boolean indicating if there should be a secondary y-axis."
    )
    
    colors: Optional[List[str]] = Field(
        None,
        description="A list of colors for each trace. Required for all y values"
    )
    x_label: Optional[str] = Field(
        None,
        description="The label for the x-axis."
    )
    y_label: Optional[str] = Field(
        None,
        description="The label for the y-axis."
    )
    legend_title: Optional[str] = Field(
        None,
        description="The title for the legend."
    )

