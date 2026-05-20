from app.utils.llm import get_fast_llm

from app.logging.prompt_logger import (
    log_prompt
)

from app.logging.trace_logger import (
    log_trace
)

from app.logging.cost_tracker import (
    increment_calls
)

from app.utils.json_parser import (
    clean_json_response
)

fact_checker_prompt = """
You are the Fact Checker Agent.

TASK:
- soften exaggerated claims
- remove fake certainty
- preserve readability

Return ONLY valid JSON.

FORMAT:
{
  "chapter_number": 1,
  "corrected_content": "",
  "flagged_claims": [],
  "softened_claims": []
}
"""


def run_fact_checker(state):

    try:

        llm = get_fast_llm()

        increment_calls()

        latest_chapter = (
            state["chapters"][-1]
        )

        final_prompt = (
            fact_checker_prompt
            + f"\n\nCHAPTER:\n{latest_chapter}"
        )

        response = llm.invoke(
            final_prompt
        )

        raw_output = response.content

        print("\nFACT CHECKER RAW OUTPUT:\n")
        print(raw_output)

        log_prompt(
            "fact_checker",
            final_prompt,
            raw_output
        )

        parsed = clean_json_response(
            raw_output
        )

        corrected_content = parsed.get(
            "corrected_content",
            latest_chapter["content"]
        )

        updated_chapters = (
            state["chapters"][:]
        )

        updated_chapters[-1]["content"] = (
            corrected_content
        )

        log_trace(
            "fact_checker",
            "SUCCESS"
        )

        return {

            **state,

            "chapters":
                updated_chapters,

            "logs":
                state["logs"] + [
                    {
                        "agent":
                            "fact_checker",

                        "flagged_claims":
                            parsed.get(
                                "flagged_claims",
                                []
                            ),

                        "softened_claims":
                            parsed.get(
                                "softened_claims",
                                []
                            )
                    }
                ]
        }

    except Exception as e:

        print(
            "FACT CHECKER ERROR:",
            e
        )

        log_trace(
            "fact_checker",
            "FAILED",
            str(e)
        )

        return {

            **state,

            "logs":
                state["logs"] + [
                    {
                        "agent":
                            "fact_checker",

                        "error":
                            str(e)
                    }
                ]
        }