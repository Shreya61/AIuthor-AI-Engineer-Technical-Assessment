from typing import (
    TypedDict,
    Dict,
    List,
    Any
)


class BookState(TypedDict):

    user_brief: Dict[str, Any]

    outline: Dict[str, Any]

    current_chapter: int

    current_chapter_data: Dict[str, Any]

    chapter_text: str

    chapters: List[Dict[str, Any]]

    facts: List[Dict[str, Any]]

    glossary: List[Dict[str, Any]]
    
    references: List[str]

    callbacks: List[Dict[str, Any]]

    tone_profile: Dict[str, Any]

    logs: List[Dict[str, Any]]

    generated_docx: str