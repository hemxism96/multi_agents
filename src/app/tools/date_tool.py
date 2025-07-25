"""Renault Intelligence Agent - Date Tool Module
This module provides a tool to retrieve the current date
in a specified format, useful for time-based queries and analyses."""

import logging

logger = logging.getLogger(__name__)

from datetime import date, datetime

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

from utils import error_handler


class DateArgs(BaseModel):
    """Arguments for retrieving the current date."""

    format: str = Field(
        default="%Y-%m-%d", description="Date format to return. Default is YYYY-MM-DD."
    )


def get_current_date(format: str = "%Y-%m-%d") -> str:
    """
    Get the current date in the specified format.

    Args:
        format (str): Date format string. Default is "%Y-%m-%d".

    Returns:
        str: Current date in the specified format.
    """
    logger.info(f"Getting current date")
    try:
        current_date = datetime.now().strftime(format)
        logger.info(f"Current date: {current_date}")
        return current_date
    except Exception as e:
        error_handler(e)
        return date.today().strftime("%Y-%m-%d")


current_date_tool = StructuredTool.from_function(
    func=get_current_date,
    name="get_current_date",
    description="Get the current date. Use this when you need today's date for analysis or when users ask for data 'since' a year or 'until now'.",
    args_schema=DateArgs,
    return_direct=False,
)
