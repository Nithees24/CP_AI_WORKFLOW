from pathlib import Path
import os

# ------------------------------------------------------------------
# PROJECT ROOT
# ------------------------------------------------------------------
# D:\CP_AI_WORKFLOW
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

# ------------------------------------------------------------------
# CREATE DIRECTORIES (SAFE)
# ------------------------------------------------------------------
RAW_TEXT_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_TEXT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------
# CLOUD LLM API SETTINGS
# ------------------------------------------------------------------
# This workflow is now designed for cloud-hosted LLM APIs.
# Configure credentials using environment variables.
#
# Examples:
#   export LLM_API_KEY="<your-api-key>"
#   export LLM_BASE_URL="https://api.openai.com/v1"
#   export LLM_MODEL="gpt-4o-mini"

LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

LLM_TEMPERATURE = 0.0
LLM_TIMEOUT = 120  # seconds

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
