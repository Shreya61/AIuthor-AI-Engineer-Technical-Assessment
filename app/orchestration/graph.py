from langgraph.graph import (
    StateGraph,
    END
)

from app.orchestration.state import (
    BookState
)

from app.agents.planner import (
    run_planner
)

from app.agents.writer import (
    run_writer
)

from app.agents.fact_checker import (
    run_fact_checker
)

from app.agents.humanizer import (
    run_humanizer
)

from app.agents.assembler import (
    run_assembler
)

from app.agents.glossary import (
    run_glossary
)

from app.agents.references import (
    run_references
)


def chapter_router(state):

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

    print(
        "PREPARING CHAPTER:",
        current
    )

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
            next_chapter,

        "current_chapter":
            current + 1
    }


def build_graph():

    workflow = StateGraph(
        BookState
    )

    workflow.add_node(
        "planner",
        run_planner
    )

    workflow.add_node(
        "prepare_next_chapter",
        prepare_next_chapter
    )

    workflow.add_node(
        "writer",
        run_writer
    )

    workflow.add_node(
        "fact_checker",
        run_fact_checker
    )

    workflow.add_node(
        "humanizer",
        run_humanizer
    )

    workflow.add_node(
        "references",
        run_references
    )

    workflow.add_node(
        "glossary",
        run_glossary
    )

    workflow.add_node(
        "assembler",
        run_assembler
    )

    workflow.set_entry_point(
        "planner"
    )

    workflow.add_edge(
        "planner",
        "prepare_next_chapter"
    )

    workflow.add_conditional_edges(

        "prepare_next_chapter",

        chapter_router,

        {
            "writer": "writer",
            "end": "references"
        }
    )

    workflow.add_edge(
        "writer",
        "fact_checker"
    )

    workflow.add_edge(
        "fact_checker",
        "humanizer"
    )

    workflow.add_edge(
        "humanizer",
        "prepare_next_chapter"
    )

    workflow.add_edge(
        "references",
        "glossary"
    )

    workflow.add_edge(
        "glossary",
        "assembler"
    )

    workflow.add_edge(
        "assembler",
        END
    )

    return workflow.compile()