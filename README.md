# Renault Intelligence Agent

An advanced LLM-powered agent system designed to analyze and respond to queries using structured and unstructured multi-modal data from various sources. Built with LangGraph, this intelligent agent specializes in comprehensive analysis of Renault Group's corporate ecosystem, combining diverse data formats from websites, APIs, and documents to provide strategic insights.

The agent's knowledge base encompasses:
- **Renault's Renaulution Strategy Plan**: Deep analysis of the transformation roadmap
- **CEO Luca di Meo's Vision**: Insights from executive communications and strategic talks
- **Real-time Stock Performance**: Current year stock price analysis and market trends
- **CAC40 Market Benchmarking**: Comparative analysis against French market performance

This system seamlessly integrates multi-modal data sources to deliver contextual, data-driven responses that support strategic decision-making and corporate research.

## Features

- **Multi-Modal Data Integration**: Processes text, structured data, and API responses from diverse sources
- **Query Rewriting**: Automatically rewrites user queries to be more specific and effective for analysis
- **Document Retrieval**: Searches through Renault Group documents and reports
- **Stock Price Analysis**: Fetches real-time and historical stock price data using Yahoo Finance API
- **Graph Creation**: Creates bar charts and line graphs from extracted data
- **Strategic Intelligence**: Specialized analysis of Renaulution plan and executive communications

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
cd renault_intelligence_agent
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

### Building the Vector Database

Before running the system, you need to build the vector database:

```bash
python src/app/vector_database_builder.py
```

### Running the System

w/o interface
```bash
python src/app/main.py
```

w/ interface
```bash
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
renault_intelligence_agent/
├── src/app/
│   ├── __init__.py   
│   ├── main.py                    # Main application logic
│   ├── gradio_app.py              # Gradio web interface
│   ├── vector_database_builder.py # Vector database creation
│   ├── config/
│   │   ├── __init__.py           
│   │   ├── models.py         
│   │   ├── paths.py    
│   │   └── youtube_urls.py    
│   ├── prompt.py                  # System prompts
│   ├── schema.py                  # Data schemas
│   ├── utils.py                   # Utility functions
│   └── tools/
│       ├── __init__.py            # Tools module initialization
│       ├── api_tool.py            # Stock price API tool
│       ├── graph_creator.py       # Graph creation functionality
│       ├── retrieve_tool.py       # Document retrieval tool
│       └── data_tool.py   # Current date utility tool
├── pyproject.toml                 # Project dependencies
└── README.md                     
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
