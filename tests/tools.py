"""Unit tests for tools module"""

import json
import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import io
from datetime import datetime, date

# Add src to path for imports
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'app'))

try:
    from tools.api_tool import get_stock_history, StockHistoryArgs
    from tools.date_tool import get_current_date, DateArgs
    from tools.graph_creator import create_graph, GraphArgs
    from tools.retrieve_tool import retrieve, get_retriever, RetrieverArgs
    from utils import error_handler
    from schema import ErrorResponse
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure you are running tests from the project root directory")
    sys.exit(1)


class TestApiTool(unittest.TestCase):
    """Test cases for API tool functionality"""

    @patch('tools.api_tool.yf.Ticker')
    def test_get_stock_history_success(self, mock_ticker):
        """Test successful stock history retrieval"""
        # Mock yfinance response
        mock_stock = Mock()
        mock_ticker.return_value = mock_stock
        
        # Create mock history data
        mock_history = pd.DataFrame({
            'Open': [100.0, 102.0],
            'Close': [101.0, 103.0]
        })
        mock_history.index = pd.DatetimeIndex(['2023-01-01', '2023-01-02'])
        mock_stock.history.return_value = mock_history
        
        # Test the function
        result = get_stock_history('RNO.PA', '2023-01-01', '2023-01-02')
        
        # Verify results
        self.assertIn('RNO.PA', result)
        self.assertIn('2023-01-01', result)
        self.assertIn('Open=100.0', result)
        self.assertIn('Close=101.0', result)
        mock_ticker.assert_called_once_with('RNO.PA')
        mock_stock.history.assert_called_once_with(start='2023-01-01', end='2023-01-02')

    @patch('tools.api_tool.yf.Ticker')
    @patch('tools.api_tool.error_handler')
    def test_get_stock_history_error(self, mock_error_handler, mock_ticker):
        """Test error handling in stock history retrieval"""
        mock_ticker.side_effect = Exception("Network error")
        
        result = get_stock_history('RNO.PA', '2023-01-01', '2023-01-02')
        
        self.assertEqual(result, "An error occurred while fetching stock history.")
        mock_error_handler.assert_called_once()

    def test_stock_history_args_validation(self):
        """Test StockHistoryArgs validation"""
        # Valid args
        args = StockHistoryArgs(
            ticker="RNO.PA",
            start="2023-01-01",
            end="2023-01-02"
        )
        self.assertEqual(args.ticker, "RNO.PA")
        self.assertEqual(args.start, "2023-01-01")
        self.assertEqual(args.end, "2023-01-02")


class TestDateTool(unittest.TestCase):
    """Test cases for date tool functionality"""

    @patch('tools.date_tool.datetime')
    def test_get_current_date_default_format(self, mock_datetime):
        """Test getting current date with default format"""
        mock_datetime.now.return_value.strftime.return_value = "2023-01-01"
        
        result = get_current_date()
        
        self.assertEqual(result, "2023-01-01")
        mock_datetime.now.assert_called_once()
        mock_datetime.now.return_value.strftime.assert_called_once_with("%Y-%m-%d")

    @patch('tools.date_tool.datetime')
    def test_get_current_date_custom_format(self, mock_datetime):
        """Test getting current date with custom format"""
        mock_datetime.now.return_value.strftime.return_value = "01-01-2023"
        
        result = get_current_date("%m-%d-%Y")
        
        self.assertEqual(result, "01-01-2023")
        mock_datetime.now.return_value.strftime.assert_called_once_with("%m-%d-%Y")

    @patch('tools.date_tool.datetime')
    @patch('tools.date_tool.date')
    @patch('tools.date_tool.error_handler')
    def test_get_current_date_error_fallback(self, mock_error_handler, mock_date, mock_datetime):
        """Test error handling and fallback in date tool"""
        mock_datetime.now.return_value.strftime.side_effect = Exception("Format error")
        mock_date.today.return_value.strftime.return_value = "2023-01-01"
        
        result = get_current_date()
        
        self.assertEqual(result, "2023-01-01")
        mock_error_handler.assert_called_once()
        mock_date.today.assert_called_once()

    def test_date_args_validation(self):
        """Test DateArgs validation"""
        args = DateArgs(format="%Y-%m-%d")
        self.assertEqual(args.format, "%Y-%m-%d")
        
        # Test default value
        args_default = DateArgs()
        self.assertEqual(args_default.format, "%Y-%m-%d")


class TestGraphCreator(unittest.TestCase):
    """Test cases for graph creator functionality"""

    @patch('tools.graph_creator.plt')
    @patch('tools.graph_creator.pd.read_json')
    def test_create_graph_bar_success(self, mock_read_json, mock_plt):
        """Test successful bar graph creation"""
        # Mock data
        mock_df = pd.DataFrame({
            'year': [2020, 2021, 2022],
            'sales': [1000, 1100, 1200]
        })
        mock_read_json.return_value = mock_df
        
        # Mock matplotlib
        mock_plt.figure.return_value = None
        mock_plt.bar.return_value = None
        
        test_data = json.dumps([
            {"year": 2020, "sales": 1000},
            {"year": 2021, "sales": 1100},
            {"year": 2022, "sales": 1200}
        ])
        
        result = create_graph("bar", test_data, "Sales by Year", "year", "sales")
        
        self.assertIn("created successfully", result)
        mock_plt.figure.assert_called_once_with(figsize=(8, 4))
        mock_plt.bar.assert_called_once()
        mock_plt.title.assert_called_once_with("Sales by Year")
        mock_plt.xlabel.assert_called_once_with("year")
        mock_plt.ylabel.assert_called_once_with("sales")

    @patch('tools.graph_creator.plt')
    @patch('tools.graph_creator.pd.read_json')
    def test_create_graph_line_success(self, mock_read_json, mock_plt):
        """Test successful line graph creation"""
        mock_df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'price': [100.0, 102.0]
        })
        mock_read_json.return_value = mock_df
        
        test_data = json.dumps([
            {"date": "2023-01-01", "price": 100.0},
            {"date": "2023-01-02", "price": 102.0}
        ])
        
        result = create_graph("line", test_data, "Stock Price", "date", "price")
        
        self.assertIn("created successfully", result)
        mock_plt.plot.assert_called_once()

    @patch('tools.graph_creator.error_handler')
    def test_create_graph_error_handling(self, mock_error_handler):
        """Test error handling in graph creation"""
        invalid_data = "invalid json"
        
        result = create_graph("bar", invalid_data, "Title", "x", "y")
        
        self.assertIn("An error occurred", result)
        mock_error_handler.assert_called_once()

    def test_graph_args_validation(self):
        """Test GraphArgs validation"""
        args = GraphArgs(
            graph_type="bar",
            data='[{"x": 1, "y": 2}]',
            graph_title="Test Graph",
            x_axis="x",
            y_axis="y"
        )
        self.assertEqual(args.graph_type, "bar")
        self.assertEqual(args.data, '[{"x": 1, "y": 2}]')
        self.assertEqual(args.graph_title, "Test Graph")


class TestRetrieveTool(unittest.TestCase):
    """Test cases for retrieve tool functionality"""

    @patch('tools.retrieve_tool.get_retriever')
    def test_retrieve_success(self, mock_get_retriever):
        """Test successful document retrieval"""
        mock_retriever = Mock()
        mock_get_retriever.return_value = mock_retriever
        mock_retriever.invoke.return_value = ["Document 1", "Document 2"]
        
        result = retrieve("What is Renault's plan?")
        
        self.assertIn("Document 1", result)
        self.assertIn("Document 2", result)
        mock_retriever.invoke.assert_called_once_with("What is Renault's plan?")

    @patch('tools.retrieve_tool.get_retriever')
    @patch('tools.retrieve_tool.error_handler')
    def test_retrieve_error_handling(self, mock_error_handler, mock_get_retriever):
        """Test error handling in document retrieval"""
        mock_get_retriever.side_effect = Exception("Database error")
        
        result = retrieve("test question")
        
        self.assertEqual(result, "An error occurred while retrieving documents.")
        mock_error_handler.assert_called_once()

    @patch('tools.retrieve_tool.chromadb.PersistentClient')
    @patch('tools.retrieve_tool.Chroma')
    @patch('tools.retrieve_tool.HuggingFaceEmbeddings')
    def test_get_retriever_initialization(self, mock_embeddings, mock_chroma, mock_client):
        """Test retriever initialization"""
        mock_db = Mock()
        mock_chroma.return_value = mock_db
        mock_retriever = Mock()
        mock_db.as_retriever.return_value = mock_retriever
        
        result = get_retriever()
        
        self.assertEqual(result, mock_retriever)
        mock_embeddings.assert_called_once()
        mock_client.assert_called_once()
        mock_chroma.assert_called_once()

    def test_retriever_args_validation(self):
        """Test RetrieverArgs validation"""
        args = RetrieverArgs(question="What is the stock price?")
        self.assertEqual(args.question, "What is the stock price?")


class TestUtils(unittest.TestCase):
    """Test cases for utility functions"""

    @patch('utils.logger')
    def test_error_handler_with_exception(self, mock_logger):
        """Test error handler with exception"""
        test_exception = ValueError("Test error")
        
        result = error_handler(test_exception)
        
        self.assertIsInstance(result, ErrorResponse)
        self.assertEqual(result['error'], "Test error")
        self.assertEqual(result['type'], "ValueError")
        mock_logger.error.assert_called_once()

    @patch('utils.logger')
    def test_error_handler_with_custom_exception(self, mock_logger):
        """Test error handler with custom exception"""
        class CustomError(Exception):
            pass
        
        test_exception = CustomError("Custom error message")
        
        result = error_handler(test_exception)
        
        self.assertEqual(result['error'], "Custom error message")
        self.assertEqual(result['type'], "CustomError")


class TestIntegration(unittest.TestCase):
    """Integration tests for tools"""

    @patch('tools.api_tool.yf.Ticker')
    @patch('tools.graph_creator.plt')
    @patch('tools.graph_creator.pd.read_json')
    def test_stock_data_to_graph_integration(self, mock_read_json, mock_plt, mock_ticker):
        """Test integration between stock API and graph creator"""
        # Mock stock data
        mock_stock = Mock()
        mock_ticker.return_value = mock_stock
        mock_history = pd.DataFrame({
            'Open': [100.0, 102.0],
            'Close': [101.0, 103.0]
        })
        mock_history.index = pd.DatetimeIndex(['2023-01-01', '2023-01-02'])
        mock_stock.history.return_value = mock_history
        
        # Mock graph creation
        mock_df = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'close': [101.0, 103.0]
        })
        mock_read_json.return_value = mock_df
        
        # Get stock data
        stock_result = get_stock_history('RNO.PA', '2023-01-01', '2023-01-02')
        self.assertIn('RNO.PA', stock_result)
        
        # Create graph with processed data
        graph_data = json.dumps([
            {"date": "2023-01-01", "close": 101.0},
            {"date": "2023-01-02", "close": 103.0}
        ])
        graph_result = create_graph("line", graph_data, "Stock Prices", "date", "close")
        
        self.assertIn("created successfully", graph_result)


if __name__ == '__main__':
    # Configure logging for tests
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Run tests
    unittest.main(verbosity=2)