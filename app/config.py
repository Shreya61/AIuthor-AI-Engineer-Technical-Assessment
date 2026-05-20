from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("GROQ_API_KEY")

OUTPUT_DIR = "outputs"
TRACE_DIR = "traces"
LOG_DIR = "logs"