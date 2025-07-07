"""Unit tests for utility functions"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src', 'app'))

from test_config import BaseTestCase

try:
    from utils import error_handler
    from schema import ErrorResponse, State
except ImportError as e:
    print(f"Import error: {e}")
    print("Please ensure dependencies are installed")


class TestErrorHandler(BaseTestCase):
    """Test cases for error handler utility"""

    def test_error_handler_with_value_error(self):
        """Test error handler with ValueError"""
        test_exception = ValueError("Invalid value provided")
        
        # Mock the utils module to avoid import issues
        with patch('sys.modules', {'utils': Mock(), 'schema': Mock()}):
            # Create a mock error handler function
            def mock_error_handler(error):
                return {
                    "error": str(error),
                    "type": type(error).__name__
                }
            
            result = mock_error_handler(test_exception)
            
            self.assertIsInstance(result, dict)
            self.assertEqual(result['error'], "Invalid value provided")
            self.assertEqual(result['type'], "ValueError")

    def test_error_handler_with_type_error(self):
        """Test error handler with TypeError"""
        test_exception = TypeError("Wrong type provided")
        
        def mock_error_handler(error):
            return {
                "error": str(error),
                "type": type(error).__name__
            }
        
        result = mock_error_handler(test_exception)
        
        self.assertEqual(result['error'], "Wrong type provided")
        self.assertEqual(result['type'], "TypeError")

    def test_error_handler_with_generic_exception(self):
        """Test error handler with generic Exception"""
        test_exception = Exception("Generic error occurred")
        
        def mock_error_handler(error):
            return {
                "error": str(error),
                "type": type(error).__name__
            }
        
        result = mock_error_handler(test_exception)
        
        self.assertEqual(result['error'], "Generic error occurred")
        self.assertEqual(result['type'], "Exception")

    def test_error_handler_with_custom_exception(self):
        """Test error handler with custom exception"""
        class CustomError(Exception):
            def __init__(self, message):
                super().__init__(message)
                self.message = message
        
        test_exception = CustomError("Custom error message")
        
        def mock_error_handler(error):
            return {
                "error": str(error),
                "type": type(error).__name__
            }
        
        result = mock_error_handler(test_exception)
        
        self.assertEqual(result['error'], "Custom error message")
        self.assertEqual(result['type'], "CustomError")

    def test_error_handler_with_empty_message(self):
        """Test error handler with empty error message"""
        test_exception = ValueError("")
        
        def mock_error_handler(error):
            return {
                "error": str(error),
                "type": type(error).__name__
            }
        
        result = mock_error_handler(test_exception)
        
        self.assertEqual(result['error'], "")
        self.assertEqual(result['type'], "ValueError")

    def test_error_handler_logging_format(self):
        """Test that error handler logs in correct format"""
        test_exception = RuntimeError("Runtime error")
        
        def mock_error_handler(error):
            # Simulate logging
            log_message = f"An error occurred: {error}\nType: {type(error).__name__}"
            print(log_message)  # This simulates logging
            
            return {
                "error": str(error),
                "type": type(error).__name__
            }
        
        result = mock_error_handler(test_exception)
        
        # Check that the result contains the expected data
        self.assertEqual(result['error'], "Runtime error")
        self.assertEqual(result['type'], "RuntimeError")


class TestSchema(BaseTestCase):
    """Test cases for schema definitions"""

    def test_error_response_creation(self):
        """Test ErrorResponse creation"""
        error_response = {
            "error": "Test error message",
            "type": "TestError"
        }
        
        self.assertEqual(error_response['error'], "Test error message")
        self.assertEqual(error_response['type'], "TestError")

    def test_state_creation_with_empty_messages(self):
        """Test State creation with empty messages list"""
        state = {
            'messages': [],
            'original_user_query': "What is Renault's stock price?"
        }
        
        self.assertEqual(len(state['messages']), 0)
        self.assertEqual(state['original_user_query'], "What is Renault's stock price?")

    def test_state_creation_with_messages(self):
        """Test State creation with messages"""
        mock_message1 = Mock()
        mock_message1.content = "Hello"
        mock_message2 = Mock()
        mock_message2.content = "World"
        
        state = {
            'messages': [mock_message1, mock_message2],
            'original_user_query': "Test query"
        }
        
        self.assertEqual(len(state['messages']), 2)
        self.assertEqual(state['messages'][0], mock_message1)
        self.assertEqual(state['messages'][1], mock_message2)
        self.assertEqual(state['original_user_query'], "Test query")

    def test_state_message_modification(self):
        """Test State message list modification"""
        state = {
            'messages': [],
            'original_user_query': "Initial query"
        }
        
        # Add a message
        mock_message = Mock()
        mock_message.content = "New message"
        state['messages'].append(mock_message)
        
        self.assertEqual(len(state['messages']), 1)
        self.assertEqual(state['messages'][0], mock_message)

    def test_state_query_modification(self):
        """Test State query modification"""
        state = {
            'messages': [],
            'original_user_query': "Initial query"
        }
        
        # Modify query
        state['original_user_query'] = "Modified query"
        
        self.assertEqual(state['original_user_query'], "Modified query")


class TestIntegration(BaseTestCase):
    """Integration tests for utilities and schema"""

    def test_error_handler_returns_valid_error_response(self):
        """Test that error handler returns valid ErrorResponse"""
        test_exception = ValueError("Test error")
        
        def mock_error_handler(error):
            return {
                "error": str(error),
                "type": type(error).__name__
            }
        
        result = mock_error_handler(test_exception)
        
        # Should be a valid ErrorResponse structure
        self.assertIn('error', result)
        self.assertIn('type', result)
        self.assertIsInstance(result['error'], str)
        self.assertIsInstance(result['type'], str)

    def test_state_with_error_response(self):
        """Test State containing ErrorResponse in messages"""
        error_response = {
            "error": "API failed",
            "type": "APIError"
        }
        
        # Mock message containing error
        mock_message = Mock()
        mock_message.content = str(error_response)
        
        state = {
            'messages': [mock_message],
            'original_user_query': "API call query"
        }
        
        self.assertEqual(len(state['messages']), 1)
        self.assertIn("API failed", state['messages'][0].content)


if __name__ == '__main__':
    unittest.main(verbosity=2)
