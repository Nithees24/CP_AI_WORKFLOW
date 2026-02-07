from textwrap import dedent


def build_step_extraction_prompt(document_text: str) -> str:
    """
    Builds a strict prompt to extract procedural steps
    (statement, syntax, output) from unstructured text.
    """

    return dedent(f"""
    You are an expert technical document analyst.

    Your task is to extract PROCEDURAL STEPS from the given document text.
    Each step represents ONE conceptual action or instruction.
 
    --- OUTPUT FORMAT (STRICT) ---
    Return ONLY valid JSON matching this schema:

    {{
      "steps": [
        {{
          "step_id": 1,
          "statement": "string (required)",
          "syntax": ["string", "..."],
          "output": ["string", "..."],
          "confidence": "explicit | implicit | example_based"
        }}
      ]
    }}

    --- EXTRACTION RULES ---
    1. Do NOT invent information.
    2. Search for the syntax precisely and If syntax is not explicitly shown, return an empty list.
    3. If output is not explicitly described, return an empty list.
    4. Output may contain MULTIPLE lines — preserve each line as a separate list item.
    5. One step = one conceptual action (do not merge unrelated actions).
    6. Tables should be interpreted semantically (columns may map to statement/syntax/output).
    7. If information is inferred from examples or weak cues, set confidence = "implicit" or "example_based".
    8. Do NOT include explanations, comments, or extra text outside JSON.
    9. Ensure step_id values are sequential starting from 1.

    --- DOCUMENT TEXT ---
    {document_text}
    """).strip()
