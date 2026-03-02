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
from core.parser import StepParser, LLMParserError
from core.llm_client import OllamaLLMClient,GeminiLLMClient

from config.settings import (
    INPUT_FILE,
    RAW_TEXT_DIR,
    PROCESSED_TEXT_DIR,
    OUTPUT_FILE,
    OUTPUT_FILE_API,
    SAVE_ARTIFACTS,
    MAX_LLM_RETRIES,
    LLM_MODEL,
    OLLAMA_BASE_URL,
    LLM_TEMPERATURE,
    LLM_TIMEOUT,
    USE_API_LLM,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GEMINI_TEMPERATURE,
)

# ------------------------------------------------------------------
# Main Pipeline
# ------------------------------------------------------------------
def main():
    start=time.time()
    print("CP-AI-WORKFLOW started")

    # --------------------------------------------------------------
    # 1. Extract raw text blocks from PDF
    # --------------------------------------------------------------
    print("Extracting text from PDF...")
    raw_blocks = extract_lines_from_pdf(INPUT_FILE)

    if not raw_blocks:
        raise RuntimeError("No text extracted from PDF.")



    # --------------------------------------------------------------
    # 2. PAGE-CHANGE–BASED CHUNKING (CORE LOGIC)
    # --------------------------------------------------------------
    print("Chunking strictly by page boundaries...")

    page_chunks = []

    current_page = None
    current_text_parts = []

    for block in raw_blocks:
        page_no = block.get("page_number",0)
        text = block.get("text", "").strip()

        if not text:
            continue  # skip empty blocks safely

        # First block initialization
        if current_page is None:
            current_page = page_no

        # Page changed → finalize previous page chunk
        if page_no != current_page:
            page_chunks.append("\n".join(current_text_parts))
            current_text_parts = []
            current_page = page_no

        # Accumulate text for current page
        current_text_parts.append(text)

    # Finalize last page
    if current_text_parts:
        page_chunks.append("\n".join(current_text_parts))

    print(f"Total page-wise chunks created: {len(page_chunks)}")

    if not page_chunks:
        raise RuntimeError("No page chunks created after processing.")

    if SAVE_ARTIFACTS:
        RAW_TEXT_DIR.mkdir(parents=True, exist_ok=True)
        (RAW_TEXT_DIR / "input.txt").write_text(
            "\n\n--- PAGE BREAK ---\n\n".join(page_chunks),
            encoding="utf-8"
        )
    # --------------------------------------------------------------
    # 3. Normalize text PER PAGE
    # --------------------------------------------------------------
    print("Normalizing text per page...")
    normalized_chunks = []

    PROCESSED_TEXT_DIR.mkdir(parents=True, exist_ok=True)

    for idx, chunk in enumerate(page_chunks, start=1):
        normalized = normalize_text(chunk)
        normalized_chunks.append(normalized)

    if SAVE_ARTIFACTS:
        (PROCESSED_TEXT_DIR / "normalized.txt").write_text(
            "\n\n--- PAGE BREAK ---\n\n".join(normalized_chunks),
            encoding="utf-8"
        )
    #-----------------------------verified till this-------------------------------
    # --------------------------------------------------------------
    # 4. Initialize LLM + Parser
    # --------------------------------------------------------------

    if USE_API_LLM:
        print("Using Gemini API")
        llm_client = GeminiLLMClient(GEMINI_MODEL, GEMINI_API_KEY, GEMINI_TEMPERATURE)
    else:
        print("Using Ollama Local")
        llm_client = OllamaLLMClient(LLM_MODEL, OLLAMA_BASE_URL, LLM_TEMPERATURE, LLM_TIMEOUT)
    parser = StepParser(
        llm_client=llm_client,
        max_retries=MAX_LLM_RETRIES
    )

    # --------------------------------------------------------------
    # 5. Parse each page with LLM
    # --------------------------------------------------------------
    print("Parsing pages with LLM...")
    all_steps = []
    step_id = 1

    for idx, text_unit in enumerate(normalized_chunks, start=1):
        print(f"→ Processing page {idx}/{len(normalized_chunks)}")

        try:
            extraction = parser.parse(text_unit)

        except LLMParserError as e:
            print(f"LLM failed on page {idx}: {e}")
            print("Skipping this page...\n")
            continue

        except Exception as e:
            print(f"Unexpected error on page {idx}: {e}")
            print("Skipping this page...\n")
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
    if USE_API_LLM:
        OUTPUT_FILE_API.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE_API.write_text(
            json.dumps(
                {"steps": [s.model_dump() for s in all_steps]},
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )
    else:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_FILE.write_text(
            json.dumps(
                {"steps": [s.model_dump() for s in all_steps]},
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )
    print("Pipeline completed successfully")
    if USE_API_LLM:
        print(f"Output written to: {OUTPUT_FILE_API}")
    else:
        print(f"Output written to: {OUTPUT_FILE}")
    time.sleep(1)
    end = time.time()
    print(f"Total runtime of the program is {end - start} seconds")


if __name__ == "__main__":
    main()
