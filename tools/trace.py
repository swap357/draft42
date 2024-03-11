from instructor import OpenAISchema
from pydantic import Field
from typing import Optional
from tools.df_manipulation import DataFrameManipulation

class Trace(OpenAISchema):
    """
    Class to represent a single trace in a chart.
    """
    name: str = Field(
        ...,
        description="The name of the trace."
    )
    df_file_path: str = Field(
        ...,
        description="The file path to the DataFrame source."
    )
    x_column: str = Field(
        ...,
        description="The column to be used for x-axis data."
    )
    y_column: str = Field(
        ...,
        description="The column to be used for y-axis data."
    )
    yaxis: str = Field(
        "y",
        examples=["y", "y2"],
        description="The type of the y-axis - y for primary, y2 for secondary"
    )
    mode: str = Field(
        "lines+markers",
        description="The mode of the plot (e.g., lines, markers)."
    )
    color: str = Field(
        '#1f77b4',
        examples=[
            '#1f77b4',  # muted blue
            '#ff7f0e',  # safety orange
            '#2ca02c',  # cooked asparagus green
            '#d62728',  # brick red
            '#9467bd',  # muted purple
            '#8c564b',  # chestnut brown
            '#e377c2',  # raspberry yogurt pink
            '#7f7f7f',  # middle gray
            '#bcbd22',  # curry yellow-green
            '#17becf'   # blue-teal
        ],
        description="The color of the trace."
    ) 
    legend_group: Optional[str] = Field(None, 
            description="The name of the legend group to which this trace belongs.")
    legendgrouptitle_text: Optional[str] = Field(None, 
            description="The title of the legend group to which this trace belongs.")
    visible: Optional[bool] = Field(None, 
            description="Whether the trace is visible by default.")
