import json

from datetime import datetime


def log_trace(
    agent,
    status,
    details=None
):

    entry = {
        "timestamp": str(datetime.now()),
        "agent": agent,
        "status": status,
        "details": details
    }

    with open(
        "traces/agent_trace.jsonl",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(entry)
            + "\n"
        )