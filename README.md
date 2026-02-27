# CP AI Workflow (Cloud API Version)

## Overview
This project extracts procedural steps from PDF documents and converts them into structured JSON.

### Pipeline
1. PDF Document
2. Text + Layout Extraction
3. Chunking (line / paragraph / block)
4. Pre-processing Rules
5. Confidence Scoring
6. Cloud LLM API Parsing
7. Step-wise Structured Output

## Configuration
Set environment variables before running:

```bash
export LLM_API_KEY="<your-api-key>"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="gpt-4o-mini"
```

Optional:

```bash
export LLM_MODEL="gpt-4o-mini"
```

## Run
```bash
python main.py
```

Alternative page-wise pipeline:
```bash
python new_main.py
```

## Output
Structured extraction is written to:

- `output/structured_output.json`

## Notes
- The workflow no longer depends on a local Ollama server.
- The LLM client uses OpenAI-compatible `chat/completions` APIs.
