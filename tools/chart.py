from instructor import OpenAISchema
from pydantic import Field
from typing import List, Optional, Dict
from tools.trace import Trace

class PlotLike(OpenAISchema):
    """
    A class to represent the data needed to create a plotly-like plot, using OpenAISchema and Pydantic for validation.
    """
    title: str = Field(
        ...,
        description="The title of the plot."
    )
    layout_title: str = Field(
        ...,
        description="The title of the layout.",
        examples=["Chart for X vs Y"]
    )
    layout_xaxis_title: str = Field(
        ...,
        description="The title of the x-axis.",
        examples=["X"]
    )
    layout_xaxis_type: str = Field(
        ...,
        description="The type of the x-axis.",
        examples=["date"]
    )
    layout_yaxis_title: str = Field(
        ...,
        description="The title of the y-axis.",
        examples=["Y"]
    )
    layout_yaxis_type: str = Field(
        ...,
        description="The type of the y-axis.",
        examples=["linear", "log", "category", "date", "multicategory"]
    )
    yaxis2_title: Optional[str] = Field(
        ...,
        description="The title of the y-axis 2.",
        examples=["Y2"]
    )
    yaxis2_type: Optional[str] = Field(
        ...,
        description="The type of the y-axis 2.",
        examples=["linear", "log", "category", "date", "multicategory"]
    )
    xaxis_range: Optional[List[int]] = Field(
        ...,
        examples=[[0, 10], [0, 100], [0, 1000], [0, 10000]],
        description="The range of the x-axis."
    )
    yaxis_range: Optional[List[int]] = Field(
        ...,
        examples=[[0, 10], [0, 100], [0, 1000], [0, 10000]],
        description="The range of the y-axis."
    )
    traces: List[Trace] = Field(
        ...,
        description="The traces to be plotted."
    )
