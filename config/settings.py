from pathlib import Path

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
# LLM (OLLAMA) SETTINGS
# ------------------------------------------------------------------
# IMPORTANT:
# Use ONLY model names that appear in `ollama list`
#
# Recommended:
#   - "llama3:latest"
#   - "llama3:8b"
#
# DO NOT use:
#   - "llama3.2"
#   - "llama3.2:3b"
#
LLM_MODEL = "llama3.1:8b"

OLLAMA_BASE_URL = "http://localhost:11434"

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
