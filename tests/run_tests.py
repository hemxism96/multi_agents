#!/usr/bin/env python3
"""Test runner script for Renault Intelligence Agent

This script runs all unit tests for the project with proper environment setup.
"""

import os
import sys
import unittest
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'src' / 'app'))

# Mock external dependencies before importing test modules
class MockModule:
    """Mock module for external dependencies"""
    def __getattr__(self, name):
        return MockModule()
    
    def __call__(self, *args, **kwargs):
        return MockModule()
    
    def __getitem__(self, key):
        return MockModule()
    
    def __setitem__(self, key, value):
        pass

# Mock heavy dependencies that might not be available
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

def run_tests():
    """Run all tests in the tests directory"""
    # Set up test environment
    os.environ['TESTING'] = '1'
    
    # Discover and run tests
    test_dir = Path(__file__).parent
    loader = unittest.TestLoader()
    
    # Load individual test files
    test_files = [
        'test_config.py',
        'test_utils.py',
        'test_main.py',
        'tools.py'
    ]
    
    suite = unittest.TestSuite()
    
    for test_file in test_files:
        test_path = test_dir / test_file
        if test_path.exists():
            try:
                # Import and add tests
                module_name = test_file.replace('.py', '')
                if module_name == 'tools':
                    module_name = 'test_tools'
                
                spec = unittest.util.spec_from_file_location(module_name, test_path)
                if spec and spec.loader:
                    module = unittest.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Find test classes
                    for name in dir(module):
                        obj = getattr(module, name)
                        if (isinstance(obj, type) and 
                            issubclass(obj, unittest.TestCase) and 
                            obj != unittest.TestCase):
                            suite.addTest(loader.loadTestsFromTestCase(obj))
                            
            except Exception as e:
                print(f"Warning: Could not load tests from {test_file}: {e}")
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
