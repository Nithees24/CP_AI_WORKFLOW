import sys
from pathlib import Path
import json
import time

# ------------------------------------------------------------------
# Ensure project root is in PYTHONPATH
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# ------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------
from core.extractor import extract_lines_from_pdf
from core.normalizer import normalize_text
from core.chunker import chunk_text
from core.parser import StepParser, LLMParserError
from core.llm_client import OllamaLLMClient

from config.settings import (
    INPUT_FILE,
    RAW_TEXT_DIR,
    PROCESSED_TEXT_DIR,
    OUTPUT_FILE,
    SAVE_ARTIFACTS,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    MAX_LLM_RETRIES,
    LLM_MODEL,
    OLLAMA_BASE_URL,
)

# ------------------------------------------------------------------
# FEATURE FLAG
# ------------------------------------------------------------------
USE_CHUNKING = True

# ------------------------------------------------------------------
# Main Pipeline
# ------------------------------------------------------------------
def main():
    start=time.time()
    print("CP-AI-WORKFLOW started")

    # --------------------------------------------------------------
    # 1. Extract text from PDF
    # --------------------------------------------------------------
    print("Extracting text from PDF...")
    raw_pages = extract_lines_from_pdf(INPUT_FILE)
    raw_text = "\n\n".join(page["text"] for page in raw_pages)

    if SAVE_ARTIFACTS:
        RAW_TEXT_DIR.mkdir(parents=True, exist_ok=True)
        (RAW_TEXT_DIR / "input.txt").write_text(raw_text, encoding="utf-8")

    # --------------------------------------------------------------
    # 2. Normalize text
    # --------------------------------------------------------------
    print("Normalizing text...")
    normalized_text = normalize_text(raw_text)

    if SAVE_ARTIFACTS:
        PROCESSED_TEXT_DIR.mkdir(parents=True, exist_ok=True)
        (PROCESSED_TEXT_DIR / "input_cleaned.txt").write_text(
            normalized_text, encoding="utf-8"
        )

    # --------------------------------------------------------------
    # 3. Prepare input (with or without chunking)
    # --------------------------------------------------------------
    if USE_CHUNKING:
        print("Chunking enabled")
        chunks = chunk_text(
            normalized_text,
            chunk_size=CHUNK_SIZE,
            overlap=CHUNK_OVERLAP
        )
    else:
        print("Chunking disabled (single-pass extraction)")
        chunks = [normalized_text]

    print(f"Total units to process: {len(chunks)}")

    # --------------------------------------------------------------
    # 4. Initialize LLM + Parser
    # --------------------------------------------------------------
    llm_client = OllamaLLMClient(
        model=LLM_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=0.0
    )

    parser = StepParser(
        llm_client=llm_client,
        max_retries=MAX_LLM_RETRIES
    )

    # --------------------------------------------------------------
    # 5. Parse input(s)
    # --------------------------------------------------------------
    print("Parsing with LLM...")
    all_steps = []
    step_id = 1

    for idx, text_unit in enumerate(chunks, start=1):
        label = "chunk" if USE_CHUNKING else "document"
        print(f"→ Processing {label} {idx}/{len(chunks)}")

        try:
            extraction = parser.parse(text_unit)

        except LLMParserError as e:
            print(f" LLM failed on {label} {idx}: {e}")
            print("Skipping and continuing...\n")
            continue

        except Exception as e:
            print(f" Unexpected error on {label} {idx}: {e}")
            print("Skipping and continuing...\n")
            continue

        for step in extraction.steps:
            step.step_id = step_id
            all_steps.append(step)
            step_id += 1

    if not all_steps:
        raise RuntimeError("No steps were extracted from the document.")

    # --------------------------------------------------------------
    # 6. Save output
    # --------------------------------------------------------------
    print("Saving structured output...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(
            {"steps": [s.model_dump() for s in all_steps]},
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("Pipeline completed successfully ")
    print(f"Output written to: {OUTPUT_FILE}")
    time.sleep(1)
    end=time.time()
    print(f"Total runtime of the program is {end - start} seconds")


if __name__ == "__main__":
    main()
