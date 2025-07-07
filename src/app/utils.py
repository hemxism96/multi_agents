"""Renault Intelligence Agent - Utility Functions"""

import logging

from schema import ErrorResponse

logger = logging.getLogger(__name__)


def error_handler(error: Exception) -> ErrorResponse:
    """
    Handles errors by printing the error message and returning a standardized error response.

    Args:
        error (Exception): The error to handle.

    Returns:
        dict: A dictionary containing the error message.
    """
    logger.error(f"An error occurred: {error}\n" f"Type: {type(error).__name__}")
    return ErrorResponse(error=str(error), type=type(error).__name__)
