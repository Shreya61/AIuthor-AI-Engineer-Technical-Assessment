from langgraph.graph import StateGraph, END

from app.orchestration.state import BookState

from app.agents.planner import run_planner
from app.agents.writer import run_writer


def chapter_router(state):

    chapters = state["outline"]["chapters"]

    current = state["current_chapter"]

    if current >= len(chapters):
        return "end"

    return "writer"


def prepare_next_chapter(state):

    outline = state.get(
        "outline",
        {}
    )

    chapters = outline.get(
        "chapters",
        []
    )

    current = state.get(
        "current_chapter",
        0
    )

    if current >= len(chapters):

        return {
            **state
        }

    next_chapter = chapters[current]

    return {

        **state,

        "current_chapter_data":
            next_chapter
    }


def build_graph():

    workflow = StateGraph(BookState)

    workflow.add_node("planner", run_planner)

    workflow.add_node(
        "prepare_next_chapter",
        prepare_next_chapter
    )

    workflow.add_node("writer", run_writer)

    workflow.set_entry_point("planner")

    workflow.add_edge(
        "planner",
        "prepare_next_chapter"
    )

    workflow.add_conditional_edges(
        "prepare_next_chapter",
        chapter_router,
        {
            "writer": "writer",
            "end": END
        }
    )

    workflow.add_edge(
        "writer",
        "prepare_next_chapter"
    )

    return workflow.compile()