import streamlit as st

from app.orchestration.graph import (
    build_graph
)

from app.logging.cost_tracker import (
    get_cost_summary
)


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="AIuthor",
    layout="wide"
)

st.title("📚 AIuthor")

st.subheader(
    "Agentic Book Generation System"
)


# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.header(
    "Book Configuration"
)

topic = st.sidebar.text_input(
    "Topic",
    "Personal Finance"
)

tone = st.sidebar.selectbox(
    "Tone",
    [
        "Conversational",
        "Academic",
        "Storyteller",
        "Motivational",
        "Witty"
    ]
)

chapter_count = st.sidebar.slider(
    "Chapters",
    3,
    10,
    5
)

generate = st.sidebar.button(
    "Generate Book"
)


# ---------------------------------------------------
# GENERATION
# ---------------------------------------------------

if generate:

    graph = build_graph()

    initial_state = {

        "user_brief": {
            "topic": topic,
            "tone": tone,
            "chapters": chapter_count
        },

        "outline": {},

        "current_chapter": 0,

        "current_chapter_data": {},

        "chapter_text": "",

        "chapters": [],

        "facts": [],

        "references": [],

        "glossary": [],

        "callbacks": [],

        "tone_profile": {},

        "logs": [],

        "generated_docx": ""
    }

    with st.spinner(
        "Generating book..."
    ):

        result = graph.invoke(
            initial_state
        )

    # DEBUG

    st.write(
        result.keys()
    )

    # ---------------------------------------------------
    # TABS
    # ---------------------------------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "📖 Chapters",
            "🧠 Outline",
            "📜 Logs"
        ]
    )

    # ---------------------------------------------------
    # CHAPTERS
    # ---------------------------------------------------

    with tab1:

        outline = result.get(
            "outline",
            {}
        )

        book_title = outline.get(
            "book_title",
            "Untitled Book"
        )

        st.title(
            book_title
        )

        chapters = result.get(
            "chapters",
            []
        )

        if len(chapters) == 0:

            st.warning(
                "No chapters generated."
            )

        else:

            for chapter in chapters:

                st.markdown(
                    f"## Chapter {chapter['chapter_number']}: "
                    f"{chapter['title']}"
                )

                st.write(
                    chapter["content"]
                )

                st.divider()

    # ---------------------------------------------------
    # OUTLINE
    # ---------------------------------------------------

    with tab2:

        st.json(
            result.get(
                "outline",
                {}
            )
        )

    # ---------------------------------------------------
    # LOGS
    # ---------------------------------------------------

    with tab3:

        st.json(
            result.get(
                "logs",
                []
            )
        )

    # ---------------------------------------------------
    # METRICS
    # ---------------------------------------------------

    st.subheader(
        "System Metrics"
    )

    cost_summary = get_cost_summary()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "LLM Calls",
            cost_summary["total_llm_calls"]
        )

    with col2:

        st.metric(
            "Callbacks Stored",
            len(
                result.get(
                    "callbacks",
                    []
                )
            )
        )

    # ---------------------------------------------------
    # DOWNLOAD DOCX
    # ---------------------------------------------------

    if result.get("generated_docx"):

        st.success(
            "DOCX generated successfully!"
        )

        with open(
            result["generated_docx"],
            "rb"
        ) as file:

            st.download_button(

                label="📥 Download DOCX",

                data=file,

                file_name="generated_book.docx",

                mime=(
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            )