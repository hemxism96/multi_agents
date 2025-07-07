"""Test configuration and utilities"""

import os
import sys
import unittest
from unittest.mock import Mock, patch

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src', 'app'))

# Mock external dependencies that might not be available during testing
class MockModule:
    """Mock module for external dependencies"""
    def __getattr__(self, name):
        return Mock()

# Mock heavy dependencies
sys.modules['chromadb'] = MockModule()
sys.modules['langchain_chroma'] = MockModule()
sys.modules['langchain_huggingface'] = MockModule()
sys.modules['langchain_google_genai'] = MockModule()
sys.modules['langchain_core'] = MockModule()
sys.modules['langchain_core.vectorstores'] = MockModule()
sys.modules['langchain.tools'] = MockModule()
sys.modules['langgraph'] = MockModule()
sys.modules['langgraph.graph'] = MockModule()
sys.modules['langgraph.graph.message'] = MockModule()
sys.modules['langgraph.prebuilt'] = MockModule()
sys.modules['yfinance'] = MockModule()
sys.modules['matplotlib'] = MockModule()
sys.modules['matplotlib.pyplot'] = MockModule()

def setup_test_environment():
    """Setup test environment with mocked dependencies"""
    # Mock configuration modules
    mock_config = Mock()
    mock_config.EmbeddingConfig = Mock()
    mock_config.EmbeddingConfig.model_name = "test-model"
    mock_config.PathConfig = Mock()
    mock_config.PathConfig.CHROMA_DB_DIR = "/tmp/test_chroma"
    mock_config.RetrievalConfig = Mock()
    mock_config.RetrievalConfig.collection_name = "test_collection"
    mock_config.RetrievalConfig.search_type = "similarity"
    mock_config.RetrievalConfig.k = 5
    mock_config.LLMConfig = Mock()
    mock_config.LLMConfig.model_name = "test-llm"
    mock_config.LLMConfig.temperature = 0.1
    mock_config.LLMConfig.timeout = 30
    mock_config.LLMConfig.max_retries = 3
    
    sys.modules['config'] = mock_config
    
    # Mock prompts
    mock_prompt = Mock()
    mock_prompt.SYSTEM_PROMPT = "You are a helpful assistant."
    mock_prompt.REWRITER_PROMPT = "Rewrite this query: {user_input}"
    sys.modules['prompt'] = mock_prompt
    
    return mock_config

# Initialize test environment
setup_test_environment()

class BaseTestCase(unittest.TestCase):
    """Base test case with common setup"""
    
    def setUp(self):
        """Set up test environment"""
        self.mock_config = setup_test_environment()
    
    def tearDown(self):
        """Clean up after tests"""
        pass


class TestRunner:
    """Test runner with custom configuration"""
    
    def __init__(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(self.test_dir)
    
    def discover_tests(self):
        """Discover all test files"""
        loader = unittest.TestLoader()
        suite = loader.discover(self.test_dir, pattern='test_*.py')
        return suite
    
    def run_tests(self, verbosity=2):
        """Run all tests"""
        suite = self.discover_tests()
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        return result.wasSuccessful()


if __name__ == '__main__':
    runner = TestRunner()
    success = runner.run_tests()
    sys.exit(0 if success else 1)
