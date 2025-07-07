"""Renault Intelligence Agent - Schema Definitions"""

from typing import Annotated

from langgraph.graph.message import add_messages
from typing_extensions import TypedDict


class State(TypedDict):
    """State of the agent system"""

    messages: Annotated[list, add_messages]
    original_user_query: str


class ErrorResponse(TypedDict):
    """Error response schema"""

    error: str
    type: str
