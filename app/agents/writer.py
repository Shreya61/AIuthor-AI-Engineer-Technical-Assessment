import json

from app.utils.llm import get_writer_llm

from app.schemas.chapter_schema import (
    ChapterOutput
)

from app.memory.tone_profiles import TONES

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

writer_prompt = """
You are the Writer Agent.

Your responsibility:
Write emotionally engaging,
publication-quality chapters
that feel authentically human.

STRICT RULES:
- Maintain strong tone consistency
- Use emotional pacing
- Use natural rhythm variation
- Use vivid examples and metaphors
- Preserve callbacks naturally
- Build continuity across chapters
- Make prose immersive
- Write like a real author
- Use subsection headings
- Vary paragraph lengths
- Use emotionally resonant transitions
- Keep chapter length between 500-700 words

STRUCTURE:
- opening hook
- 2-4 subsection headings
- reflective ending

STYLE RULES:
- Sound confident but natural
- Use second-person where appropriate
- Use varied sentence lengths
- Avoid repetitive openings
- Avoid robotic transitions

Return ONLY valid JSON.

FORMAT:
{
  "chapter_number": 1,
  "title": "",
  "content": "",
  "callbacks_used": []
}
"""


def run_writer(state):

    try:

        llm = get_writer_llm()

        increment_calls()

        chapter = state["current_chapter_data"]

        tone = state["user_brief"]["tone"]

        tone_profile = TONES[tone]

        final_prompt = (
            writer_prompt
            + f"\n\nTONE PROFILE:\n{tone_profile}"
            + f"\n\nCHAPTER:\n{chapter}"
            + f"\n\nPREVIOUS CALLBACKS:\n{state['callbacks']}"
        )

        response = llm.invoke(final_prompt)

        raw_output = response.content

        print("\nWRITER RAW OUTPUT:\n")
        print(raw_output)

        log_prompt(
            "writer",
            final_prompt,
            raw_output
        )

        parsed = clean_json_response(
            raw_output
        )

        validated = ChapterOutput(
            **parsed
        )

        updated_callbacks = (
            state["callbacks"][:]
        )

        for cb in validated.callbacks_used:

            updated_callbacks.append({

                "callback": cb,

                "chapter":
                    validated.chapter_number
            })

        updated_chapters = (
            state["chapters"] + [
                validated.dict()
            ]
        )

        log_trace(
            "writer",
            "SUCCESS"
        )

        return {

            **state,

            "chapters":
                updated_chapters,

            "callbacks":
                updated_callbacks
        }

    except Exception as e:

        print(
            "WRITER ERROR:",
            e
        )

        log_trace(
            "writer",
            "FAILED",
            str(e)
        )

        raise Exception(
            f"WRITER FAILED: {str(e)}"
        )