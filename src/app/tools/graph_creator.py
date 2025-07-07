"""Renault Intelligence Agent - Graph Creation Tool Module
This module provides a tool to create graphs based on provided data."""

import logging

logger = logging.getLogger(__name__)

import io

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")
import json
from typing import List, Optional, Union

import pandas as pd
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from utils import error_handler


class GraphArgs(BaseModel):
    """Arguments for creating a graph."""

    graph_type: str = Field(description="graph type to create", enum=["bar", "line"])
    data: str = Field(
        description="json strings of data to plot periodically"
    )
    graph_title: str = Field(description="title of the graph to create")
    x_axis: str = Field(description="x-axis label on data for the graph")
    y_axis: str = Field(
        description="y-axis label on data for the graph. It must be a column name in the data"
    )


def create_graph(
    graph_type: str,
    data: str,
    graph_title: str,
    x_axis: str,
    y_axis,
) -> str:
    """Create a graph based on the provided data."""
    logger.info("Creating graph")
    try:
        plt.figure(figsize=(8, 4))
        df = pd.read_json(io.StringIO(data))
        if graph_type == "bar":
            plt.bar(df[x_axis], df[y_axis], alpha=0.7)
        elif graph_type == "line":
            plt.plot(df[x_axis], df[y_axis])
        plt.title(graph_title)
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.tight_layout()
        plt.savefig("graph.png")
        plt.close()
        return f"{graph_title}: Graph of type '{graph_type}' created successfully."
    except Exception as e:
        error_handler(e)
        return f"An error occurred while creating the graph: {str(e)}"


graph_creator_tool = StructuredTool.from_function(
    func=create_graph,
    name="create_graph",
    description="Create a graph with extracted data from the other tools.",
    args_schema=GraphArgs,
    return_direct=False,
)
