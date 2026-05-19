import streamlit as st

from app.orchestration.graph import build_graph


st.title("AIuthor — Agentic Book Generator")


topic = st.text_input("Book Topic")
tone = st.selectbox(
    "Tone",
    [
        "Conversational",
        "Academic",
        "Storyteller",
        "Motivational",
        "Witty"
    ]
)

chapters = st.slider("Number of Chapters", 3, 10, 5)


if st.button("Generate Outline"):

    graph = build_graph()

    initial_state = {
        "user_brief": {
            "topic": topic,
            "tone": tone,
            "chapters": chapters
        },
        "outline": {},
        "current_chapter": 0,
        "chapter_text": "",
        "chapters": [],
        "facts": [],
        "callbacks": [],
        "tone_profile": {},
        "logs": []
    }

    result = graph.invoke(initial_state)

    st.json(result["outline"])