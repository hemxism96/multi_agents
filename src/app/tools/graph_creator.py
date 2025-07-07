import io
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import List, Optional, Union


class GraphArgs(BaseModel):
    graph_type: str = Field(description="graph type to create", enum=["bar", "line"])
    data: List[str] = Field(description="a list of json strings of data to plot periodically")
    graph_title: str = Field(description="title of the graph to create")
    x_axis: str = Field(description="x-axis label on data for the graph")
    y_axis: str = Field(description="y-axis label on data for the graph. It must be a column name in the data")
    labels: List[str] = Field(description="a list of ticker labels for each datasets")


def create_graph(
    graph_type: str,
    data: List[str],
    graph_title: str,
    x_axis: str,
    y_axis,
    labels: List[str]
) -> str:
    print("===GRAPH CREATION===")
    plt.figure(figsize=(8, 4))
    for idx, d in enumerate(data):
        df = pd.read_json(io.StringIO(d))
        label = labels[idx] if labels and idx < len(labels) else f"data{idx+1}"
        if graph_type == "bar":
            plt.bar(df[x_axis], df[y_axis], label=label, alpha=0.7)
        elif graph_type == "line":
            plt.plot(df[x_axis], df[y_axis], label=label)
    plt.title(graph_title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.legend(loc="best")
    plt.tight_layout()
    plt.savefig("graph.png")
    plt.close()
    return f"{graph_title}: Graph of type '{graph_type}' created successfully."


graph_creator_tool = StructuredTool.from_function(
    func=create_graph,
    name="create_graph",
    description="Create a graph with extracted data from the other tools.",
    args_schema=GraphArgs,
    return_direct=False
)
