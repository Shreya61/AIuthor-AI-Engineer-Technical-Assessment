import json
import re


def clean_json_response(raw_output):

    if raw_output is None:

        raise Exception(
            "Empty LLM response"
        )

    cleaned = raw_output.strip()

    # remove markdown fences

    cleaned = cleaned.replace(
        "```json",
        ""
    )

    cleaned = cleaned.replace(
        "```",
        ""
    )

    cleaned = cleaned.strip()

    # extract JSON object safely

    match = re.search(
        r'\{.*\}',
        cleaned,
        re.DOTALL
    )

    if not match:

        raise Exception(
            "No JSON object found"
        )

    cleaned = match.group(0)

    # remove invalid control chars

    cleaned = re.sub(
        r'[\x00-\x1F\x7F]',
        ' ',
        cleaned
    )

    # normalize whitespace

    cleaned = re.sub(
        r'\s+',
        ' ',
        cleaned
    )

    try:

        return json.loads(cleaned)

    except Exception as e:

        print("\nBROKEN JSON:\n")
        print(cleaned)

        raise Exception(
            f"JSON PARSE FAILED: {str(e)}"
        )