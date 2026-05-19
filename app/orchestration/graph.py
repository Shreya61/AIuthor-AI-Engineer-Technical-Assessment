from langgraph.graph import StateGraph, END

from app.orchestration.state import BookState
from app.agents.planner import run_planner


def build_graph():

    workflow = StateGraph(BookState)

    workflow.add_node("planner", run_planner)

    workflow.set_entry_point("planner")

    workflow.add_edge("planner", END)

    return workflow.compile()