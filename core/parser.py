import json
import re


from schemas.step_schema import DocumentExtraction
from prompts.step_extraction_prompt import build_step_extraction_prompt


class LLMParserError(Exception): #custom exception
    """Raised when LLM parsing fails after retries."""


class StepParser:
    def __init__(self, llm_client, max_retries: int = 2):
        self.llm_client = llm_client
        self.max_retries = max_retries

    def parse(self, document_text: str) -> DocumentExtraction:
        base_prompt = build_step_extraction_prompt(document_text)
        last_error: Optional[Exception] = None

        for attempt in range(1, self.max_retries + 1):
            try:
                prompt = self._tighten_prompt(base_prompt, attempt) if attempt > 1 else base_prompt

                raw_response = self.llm_client.generate(prompt)

                if not raw_response or not raw_response.strip():
                    raise ValueError("LLM returned empty response")

                json_text = self._extract_json(raw_response)
                parsed_json = json.loads(json_text)

                extraction = DocumentExtraction.model_validate(parsed_json)
                self._sanity_check(extraction)

                return extraction

            except Exception as e:
                last_error = e

        raise LLMParserError(
            f"LLM parsing failed after {self.max_retries} attempts"
        ) from last_error

    @staticmethod
    def _extract_json(text: str) -> str:
        """
        Extracts the first JSON object from LLM output.
        """
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in LLM output")
        return match.group(0)

    @staticmethod
    def _sanity_check(extraction: DocumentExtraction) -> None:
        for step in extraction.steps:
            if not step.statement.strip():
                raise ValueError(
                    f"Empty statement found in step_id={step.step_id}"
                )

            if not isinstance(step.syntax, list):
                raise ValueError(
                    f"Syntax must be a list in step_id={step.step_id}"
                )

            if not isinstance(step.output, list):
                raise ValueError(
                    f"Output must be a list in step_id={step.step_id}"
                )

    @staticmethod
    def _tighten_prompt(prompt: str, attempt: int) -> str:
        return f"""
{prompt}

IMPORTANT:
Return ONLY valid JSON.
No explanations.
If no steps exist, return: {{ "steps": [] }}
"""
