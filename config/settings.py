import os
from pathlib import Path
from dotenv import load_dotenv

# ------------------------------------------------------------------
# PROJECT ROOT
# ------------------------------------------------------------------
# D:\CP_AI_WORKFLOW
load_dotenv()
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# DATA PATHS
# ------------------------------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
INPUT_FILE = DATA_DIR / "input.pdf"

RAW_TEXT_DIR = DATA_DIR / "raw_text"
PROCESSED_TEXT_DIR = DATA_DIR / "processed_text"

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_FILE = OUTPUT_DIR / "structured_output.json"
OUTPUT_FILE_API = OUTPUT_DIR / "structured_output_api.json"
# ------------------------------------------------------------------
# CREATE DIRECTORIES (SAFE)
# ------------------------------------------------------------------
RAW_TEXT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_TEXT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------
# LLM (OLLAMA) SETTINGS
# ------------------------------------------------------------------
#
# Recommended:
#   - "llama3:latest"
#   - "llama3:8b"hi
#
# DO NOT use:
#   - "llama3.2"
#   - "llama3.2:3b"
#
# existing ollama settings (already there)
USE_API_LLM = True

LLM_MODEL       = "llama3.2:3b"
OLLAMA_BASE_URL = "http://localhost:11434"
LLM_TEMPERATURE = 0.2
LLM_TIMEOUT     = 120

# SWITCH FOR LLM AND CLOUD BASED LLM CALLING


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL       = "gemini-2.5-flash"
GEMINI_TEMPERATURE = 0.2

# ------------------------------------------------------------------
# PIPELINE SETTINGS
# ------------------------------------------------------------------
SAVE_ARTIFACTS = True

# Chunking (character-based)
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 0

# LLM retry policy
MAX_LLM_RETRIES = 2

# ------------------------------------------------------------------
# DEBUG / LOGGING
# ------------------------------------------------------------------
DEBUG = True
