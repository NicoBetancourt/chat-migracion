from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode

from graph.nodes import Agent, should_continue
from graph.state import State
from graph.tools import tools


def workflow():
    graph = StateGraph(State)

    # tavily = tavilyTool()
    mongo_tools = tools()
    tool_node = ToolNode(mongo_tools)

    agent = Agent(mongo_tools)
    graph.add_node("agent", agent)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", should_continue, ["tools", END])
    graph.add_edge("tools", "agent")

    return graph.compile()
