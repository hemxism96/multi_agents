"""
pytest configuration for Renault Intelligence Agent tests
"""
import os
import sys
import pytest
from pathlib import Path
from unittest.mock import Mock

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src' / 'app'))

# Set testing environment
os.environ['TESTING'] = '1'

class MockModule:
    """Mock module for external dependencies"""
    def __getattr__(self, name):
        return Mock()
    
    def __call__(self, *args, **kwargs):
        return Mock()
    
    def __getitem__(self, key):
        return Mock()
    
    def __setitem__(self, key, value):
        pass

# Mock external dependencies before any imports
mock_modules = [
    'chromadb',
    'langchain_chroma', 
    'langchain_huggingface',
    'langchain_google_genai',
    'langchain_core',
    'langchain_core.vectorstores',
    'langchain.tools',
    'langgraph',
    'langgraph.graph',
    'langgraph.graph.message',
    'langgraph.prebuilt',
    'yfinance',
    'matplotlib',
    'matplotlib.pyplot',
    'sentence_transformers',
    'tiktoken',
    'gradio',
    'google.generativeai',
    'torch',
    'transformers'
]

for module in mock_modules:
    sys.modules[module] = MockModule()

@pytest.fixture(scope='session')
def mock_config():
    """Mock configuration for all tests"""
    config = Mock()
    config.EmbeddingConfig = Mock()
    config.EmbeddingConfig.model_name = "sentence-transformers/all-MiniLM-L6-v2"
    config.PathConfig = Mock()
    config.PathConfig.CHROMA_DB_DIR = "/tmp/test_chroma"
    config.RetrievalConfig = Mock()
    config.RetrievalConfig.collection_name = "test_collection"
    config.RetrievalConfig.search_type = "similarity"
    config.RetrievalConfig.k = 5
    config.LLMConfig = Mock()
    config.LLMConfig.model_name = "gemini-pro"
    config.LLMConfig.temperature = 0.1
    config.LLMConfig.timeout = 30
    config.LLMConfig.max_retries = 3
    
    sys.modules['config'] = config
    return config

@pytest.fixture(scope='session')
def mock_prompt():
    """Mock prompt templates for all tests"""
    prompt = Mock()
    prompt.SYSTEM_PROMPT = "You are a helpful assistant for Renault Group analysis."
    prompt.REWRITER_PROMPT = "Rewrite this query: {user_input}"
    
    sys.modules['prompt'] = prompt
    return prompt

@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing"""
    return [
        {"date": "2023-01-01", "open": 100.0, "close": 101.0, "ticker": "RNO.PA"},
        {"date": "2023-01-02", "open": 101.0, "close": 102.0, "ticker": "RNO.PA"},
        {"date": "2023-01-03", "open": 102.0, "close": 103.0, "ticker": "RNO.PA"}
    ]

@pytest.fixture
def sample_documents():
    """Sample documents for testing retrieval"""
    return [
        "Renault Group reported revenue of €52.4 billion in 2023.",
        "The company sold 2.2 million vehicles worldwide in 2023.",
        "Renault's stock price increased by 15% in 2023."
    ]

@pytest.fixture
def sample_state():
    """Sample state for testing"""
    return {
        'messages': [],
        'original_user_query': 'What is Renault\'s stock price?'
    }

# Configure pytest
def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow"
    )
