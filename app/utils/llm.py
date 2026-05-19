from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import MODEL_WRITER, MODEL_FAST


def get_writer_llm():
    return ChatGoogleGenerativeAI(
        model=MODEL_WRITER,
        temperature=0.8
    )


def get_fast_llm():
    return ChatGoogleGenerativeAI(
        model=MODEL_FAST,
        temperature=0.3
    )