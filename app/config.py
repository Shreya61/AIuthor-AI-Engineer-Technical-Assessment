from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY = os.getenv("AIzaSyCfP4AXadrlGf29yrl8xzMl3UDpnfJ1G84")

MODEL_WRITER = "gemini-1.5-pro"
MODEL_FAST = "gemini-1.5-flash"

OUTPUT_DIR = "outputs"
TRACE_DIR = "traces"
LOG_DIR = "logs"