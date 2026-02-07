import re


def normalize_text(text: str) -> str:
    """
    Normalize extracted text to make it LLM-friendly
    without changing semantic meaning.
    """

    if not text:
        return ""

    # 1. Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 2. Remove trailing spaces on each line
    text = "\n".join(line.rstrip() for line in text.splitlines())

    # 3. Collapse multiple blank lines into max two
    text = re.sub(r"\n{3,}", "\n\n", text)

    # 4. Fix broken lines where sentences are split badly
    #    Example:
    #    "Mode – READ\nWRITE" -> "Mode – READ WRITE"
    text = re.sub(r"([a-zA-Z0-9,–\-])\n([a-zA-Z0-9])", r"\1 \2", text)

    # 5. Normalize common bullet symbols
    text = text.replace("•", "-").replace("●", "-")

    return text.strip()
