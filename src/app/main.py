from functools import partial

from langgraph.graph import StateGraph, START, END
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from schema import State
from prompt import SYSTEM_PROMPT, REWRITER_PROMPT
from tools import stock_price_api_reader, retriever_tool, graph_creator_tool


def query_rewriter(state: State) -> State:
    user_input = state["original_user_query"]

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        timeout=30,
        max_retries=2,
    )
    prompt_text = REWRITER_PROMPT.format(user_input=user_input)
    rewritten = llm.invoke([HumanMessage(content=prompt_text)])
    print(rewritten.content)
    state["messages"].append(HumanMessage(content=rewritten.content))
    return state


def chatbot(llm_with_tools, state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


def build_graph(llm_with_tools, tools) -> CompiledStateGraph:
    graph_builder = StateGraph(State)

    graph_builder.add_node("query_rewriter", query_rewriter)
    graph_builder.add_node("chatbot", partial(chatbot, llm_with_tools))
    graph_builder.add_node("tools", ToolNode(tools=tools))

    graph_builder.add_edge(START, "query_rewriter")
    graph_builder.add_edge("query_rewriter", "chatbot")
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition
    )
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.add_edge("chatbot", END)

    graph = graph_builder.compile()

    return graph

def run(question: str):
    print(f"User question: {question}")
    tools = [stock_price_api_reader, retriever_tool, graph_creator_tool]
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        timeout=30,
        max_retries=2,
    )
    llm_wiht_tools = llm.bind_tools(tools)
    graph = build_graph(llm_wiht_tools, tools)
    res = graph.invoke(
        State(
            messages=[
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=question)
            ],
            original_user_query=question
        )
    )
    print(res["messages"][-1].content)
    

if __name__ == "__main__":
    question_list = [
        "Summarize the Renaultion plan report when it’s announced in 2021.",
        "Identify the members of the board of directors in 2021.",
        "Outline the changes in the board of directors between 2023 and 2022.",
        "What was the total number of vehicles sold by Renault in 2023?",
        "Create a graph illustrating the number of vehicles sold per year from 2020 onwards.",
        "Create a graph that compares Renault's stock price on result announcement days since 2020 with the overall performance of CAC40 during the same period.",
        "Analyze the correlation between Renault's annual vehicle sales and its stock price, specifically on result announcement days, since 2020.",
        "DPEF indicators.",
        "Summarize the progress of Renault's plan since 2021."
    ]
    run(question_list[4])