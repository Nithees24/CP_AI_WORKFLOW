from schemas.step_schema import DocumentExtraction


class ValidationError(Exception):
    """Raised when semantic validation fails."""


def validate_extraction(extraction: DocumentExtraction) -> None:
    """
    Perform semantic validation on extracted steps.
    Raises ValidationError if issues are found.
    """

    for step in extraction.steps:
        _validate_statement(step)
        _validate_syntax(step)
        _validate_output(step)


def _validate_statement(step) -> None:
    if not step.statement or len(step.statement.strip()) < 5:
        raise ValidationError(
            f"Invalid or empty statement in step_id={step.step_id}"
        )

    # Prevent meta / useless statements
    forbidden_phrases = [
        "this section",
        "this document",
        "explains the above",
        "described below"
    ]

    lower_stmt = step.statement.lower()
    if any(p in lower_stmt for p in forbidden_phrases):
        raise ValidationError(
            f"Vague statement in step_id={step.step_id}: {step.statement}"
        )


def _validate_syntax(step) -> None:
    for syntax in step.syntax:
        # Syntax should contain at least one non-word character
        # to avoid hallucinated prose like "run the command"
        if syntax.isalpha():
            raise ValidationError(
                f"Suspicious syntax in step_id={step.step_id}: {syntax}"
            )


def _validate_output(step) -> None:
    for output in step.output:
        if len(output.strip()) < 3:
            raise ValidationError(
                f"Suspiciously short output in step_id={step.step_id}"
            )
