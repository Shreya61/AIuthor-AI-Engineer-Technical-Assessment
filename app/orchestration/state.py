from typing import TypedDict, Dict, List, Any


class BookState(TypedDict):
    user_brief: Dict[str, Any]
    outline: Dict[str, Any]
    current_chapter: int
    chapter_text: str
    chapters: List[Dict[str, Any]]
    facts: List[Dict[str, Any]]
    callbacks: List[Dict[str, Any]]
    tone_profile: Dict[str, Any]
    logs: List[Dict[str, Any]]