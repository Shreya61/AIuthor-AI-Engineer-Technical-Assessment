from app.orchestration.graph import build_graph


def run_pipeline():

    graph = build_graph()

    initial_state = {
        "user_brief": {
            "topic": "Personal Finance",
            "tone": "Conversational",
            "chapters": 5
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

    print(result["outline"])


if __name__ == "__main__":
    run_pipeline()