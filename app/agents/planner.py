from app.utils.llm import get_writer_llm


planner_prompt = """
You are the Planner Agent for an AI book generation system.

Your job:
- Create a complete book outline
- Define chapter sequence
- Define callback opportunities
- Maintain tone consistency
- Create emotionally engaging chapter titles

Return valid JSON only.

JSON FORMAT:
{
  "book_title": "",
  "chapters": [
    {
      "chapter_number": 1,
      "title": "",
      "summary": "",
      "callback_candidates": []
    }
  ]
}
"""


def run_planner(state):
    llm = get_writer_llm()

    response = llm.invoke(
        planner_prompt + f"\n\nUSER BRIEF:\n{state['user_brief']}"
    )

    return {
        **state,
        "outline": response.content
    }