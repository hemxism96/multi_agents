import logging

logger = logging.getLogger(__name__)

import json

import yfinance as yf
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from app.utils import error_handler


class StockHistoryArgs(BaseModel):
    ticker: str = Field(
        description="Ticker symbol of the stock in CAC40 (e.g., 'RNO.PA' for Renault and '^FCHI' for CAC40).",
        enum=["RNO.PA", "^FCHI"],
    )
    start: str = Field(
        description="Start date for the stock history in YYYY-MM-DD format."
    )
    end: str = Field(description="End date for the stock history in YYYY-MM-DD format.")


def get_stock_history(ticker: str, start: str, end: str):
    """
    Get the historical stock prices of a company on Euronext Paris between two dates.
    Args:
        ticker (str): Ticker symbol of the stock (e.g., 'RNO.PA' for Renault).
        start (str): Start date in YYYY-MM-DD format.
        end (str): End date in YYYY-MM-DD format.
    Returns:
        str: Historical stock prices in JSON format.
    """
    logger.info(f"Fetching stock history")
    logger.info(f"Ticker: {ticker}, Start: {start}, End: {end}")
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(start=start, end=end)

        result = []
        for i, row in history.iterrows():
            result.append(
                {
                    "date": i.strftime("%Y-%m-%d"),
                    "open": float(row["Open"]),
                    "close": float(row["Close"]),
                    "ticker": ticker,
                }
            )
        return json.dumps(result)
    except Exception as e:
        error_handler(e)
        return "An error occurred while fetching stock history."


stock_price_api_reader = StructuredTool.from_function(
    func=get_stock_history,
    name="get_stock_history",
    description="Get the historical stock prices of a company on Euronext Paris between two dates.",
    args_schema=StockHistoryArgs,
    return_direct=False,
)
