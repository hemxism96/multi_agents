"""Renault Intelligence Agent - Main Execution Module"""

import logging
from functools import partial
from typing import List

from config import LLMConfig
from langchain.tools import StructuredTool
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from prompt import REWRITER_PROMPT, SYSTEM_PROMPT
from schema import State
from tools import (current_date_tool, graph_creator_tool, retriever_tool,
                   stock_price_api_reader)
from utils import error_handler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # 터미널에 출력
    ],
)
logger = logging.getLogger(__name__)


def query_rewriter(state: State) -> State:
    """
    Rewrite user queries to be more specific and effective for analysis.

    This function takes the original user query and uses an LLM to rewrite it with
    additional context such as time periods, specific financial metrics, and comparison
    requirements to improve the effectiveness of subsequent tool usage.

    Args:
        state (State): The current state containing the original user query and messages

    Returns:
        State: Updated state with the rewritten query appended to messages

    Raises:
        Exception: Handled by error_handler if LLM invocation fails
    """
    logger.info("Rewriting user query")
    user_input = state["original_user_query"]

    try:
        llm = ChatGoogleGenerativeAI(
            model=LLMConfig.model_name,
            temperature=LLMConfig.temperature,
            timeout=LLMConfig.timeout,
            max_retries=LLMConfig.max_retries,
        )
        prompt_text = REWRITER_PROMPT.format(user_input=user_input)
        rewritten = llm.invoke([HumanMessage(content=prompt_text)])
        state["messages"].append(HumanMessage(content=rewritten.content))
        logger.info(f"Rewritten query: {rewritten.content}")
    except Exception as e:
        error_handler(e)

    return state


def chatbot(llm_with_tools: Runnable, state: State) -> State:
    """
    Main chatbot function that processes messages and generates responses.

    This function invokes the LLM with bound tools to process the current messages
    and generate a response. It appends the LLM's response to the message history.

    Args:
        llm_with_tools (Runnable): LLM instance with tools bound to it
        state (State): Current state containing message history

    Returns:
        State: Updated state with LLM response
    """
    state["messages"].append(llm_with_tools.invoke(state["messages"]))
    return state


def build_graph(
    llm_with_tools: Runnable, tools: List[StructuredTool]
) -> CompiledStateGraph:
    """
    Build and compile the LangGraph workflow for the agent system.

    Creates a directed graph with nodes for query rewriting, chatbot interaction,
    and tool usage. The graph flow is:
    START -> query_rewriter -> chatbot -> (conditionally) tools -> chatbot -> END

    Args:
        llm_with_tools (Runnable): LLM instance with tools bound to it
        tools (List[StructuredTool]): List of available tools for the agent

    Returns:
        CompiledStateGraph: Compiled graph ready for execution
    """
    graph_builder = StateGraph(State)

    graph_builder.add_node("query_rewriter", query_rewriter)
    graph_builder.add_node("chatbot", partial(chatbot, llm_with_tools))
    graph_builder.add_node("tools", ToolNode(tools=tools))

    graph_builder.add_edge(START, "query_rewriter")
    graph_builder.add_edge("query_rewriter", "chatbot")
    graph_builder.add_conditional_edges("chatbot", tools_condition)
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge("chatbot", END)

    graph = graph_builder.compile()

    return graph


def run(question: str) -> str:
    """
    Execute the complete single-agent workflow for a given question.

    This is the main entry point that orchestrates the entire process:
    1. Initializes the LLM with tools
    2. Builds the execution graph
    3. Runs the graph with the user question
    4. Returns the final answer

    Args:
        question (str): User's question about Renault Group data

    Returns:
        str: Generated answer from the gent system

    Example:
        >>> answer = run("What was Renault's revenue in 2023?")
        >>> print(answer)
    """
    logger.info(f"Running with question: {question}")
    tools = [
        stock_price_api_reader,
        retriever_tool,
        graph_creator_tool,
        current_date_tool,
    ]
    llm = ChatGoogleGenerativeAI(
        model=LLMConfig.model_name,
        temperature=LLMConfig.temperature,
        timeout=LLMConfig.timeout,
        max_retries=LLMConfig.max_retries,
    )
    llm_with_tools = llm.bind_tools(tools)
    graph = build_graph(llm_with_tools, tools)
    res = graph.invoke(
        State(
            messages=[
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=question),
            ],
            original_user_query=question,
        )
    )
    answer = res["messages"][-1].content
    print(f"Generated answer: {answer}")
    return answer


if __name__ == "__main__":
    question_list = [
        "Summarize the Renaultion plan report when it’s announced in 2021.",
        "Identify the members of the board of directors in 2021.",
        "Outline the changes in the board of directors between 2023 and 2022.",
        "What was the total number of vehicles sold by Renault in 2023?",
        "Create a graph illustrating renault's stock price flow in 2023",
        "Create a graph illustrating the number of vehicles sold per year from 2020 onwards.",
        "Create a graph that compares Renault's stock price on result announcement days since 2020 with the overall performance of CAC40 during the same period.",
        "Analyze the correlation between Renault's annual vehicle sales and its stock price, specifically on result announcement days, since 2020.",
        "DPEF indicators.",
        "Summarize the progress of Renault's plan since 2021.",
    ]
    run(question_list[6])
