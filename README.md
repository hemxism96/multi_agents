# Single Agent System for Corporate Research Analysis

A single agent system built with LangGraph that analyzes Renault Group corporate data, finance data flow, creates visualizations, and provides intelligent insights using various tools and data sources.

## Features

- **Query Rewriting**: Automatically rewrites user queries to be more specific and effective for analysis
- **Document Retrieval**: Searches through Renault Group documents and reports
- **Stock Price Analysis**: Fetches real-time and historical stock price data using Yahoo Finance API
- **Graph Creation**: Creates bar charts and line graphs from extracted data
- **Multi-tool Integration**: Seamlessly combines multiple data sources and analysis tools

## Architecture

The system uses a graph-based workflow with the following components:

1. **Query Rewriter**: Enhances user queries with additional context
2. **Chatbot**: Main orchestrator that processes messages and coordinates tool usage
3. **Tools**: Specialized tools for different data analysis tasks
4. **State Management**: Maintains conversation state and data flow

## Tools

### Core Tools

- **Stock Price API Reader**: Fetches stock price data from Yahoo Finance
- **Retriever Tool**: Searches through document collections
- **Graph Creator**: Creates visualizations (bar charts, line graphs)
- **Current Date Tool**: Provides current date information

### Graph Creator Features

- Supports bar charts and line graphs
- Handles multiple datasets with custom labels
- Customizable titles and axis labels
- Automatic legend generation

## Installation

### Prerequisites

- Python 3.11 - 3.13
- Poetry or pip for package management

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd corporate_analysis
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
# Add your Google API key for Gemini
export GOOGLE_API_KEY="your-api-key-here"
```

## Usage

### Running the System

w/o interface
```
python src/app/main.py
```

w/ interface
```
python src/app/gradio_app.py
```

### Example Queries

The system can handle various types of queries:

```python
# Financial analysis
run("Summarize the Renaultion plan report when it's announced in 2021.")

# Board information
run("Identify the members of the board of directors in 2021.")

# Sales data
run("What was the total number of vehicles sold by Renault in 2023?")

# Visualizations
run("Create a graph illustrating renault's stock price flow in 2023")

# Comparative analysis
run("Create a graph that compares Renault's stock price on result announcement days since 2020 with the overall performance of CAC40 during the same period.")
```

## Configuration

### LLM Configuration

The system uses Google's Gemini model with configurable parameters:

- **Model**: Google Generative AI (Gemini)
- **Temperature**: Adjustable for response creativity
- **Timeout**: Request timeout settings
- **Max Retries**: Retry logic for failed requests

### Graph Types

The graph creator supports:
- **Bar Charts**: For categorical data comparison
- **Line Graphs**: For time series and trend analysis

## Project Structure

```
multi_agents/
├── src/app/
│   ├── main.py              # Main application logic
│   ├── tools/
│   │   └── graph_creator.py # Graph creation functionality
│   ├── config.py            # Configuration settings
│   ├── prompt.py            # System prompts
│   ├── schema.py            # Data schemas
│   └── utils.py             # Utility functions
├── pyproject.toml           # Project dependencies
└── README.md               # This file
```

## Dependencies

Key dependencies include:
- **LangChain**: For LLM orchestration and tool integration
- **LangGraph**: For graph-based workflow management
- **Google Generative AI**: For LLM capabilities
- **Matplotlib**: For graph creation
- **Pandas**: For data manipulation
- **yfinance**: For stock price data
- **ChromaDB**: For document storage and retrieval

## Development

### Adding New Tools

1. Create a new tool in the `tools/` directory
2. Follow the `StructuredTool` pattern
3. Add the tool to the main tool list in `main.py`

### Extending Graph Types

To add new graph types:
1. Update the `GraphArgs` enum in `graph_creator.py`
2. Add the visualization logic in the `create_graph` function

## Error Handling

The system includes comprehensive error handling:
- Tool execution errors are caught and logged
- Graceful degradation when tools fail
- Detailed error messages for debugging

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For questions or issues, please open an issue in the repository.