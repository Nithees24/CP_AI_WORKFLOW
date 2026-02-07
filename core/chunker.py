from typing import List


def chunk_text(text: str,chunk_size,overlap) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text (str): Normalized input text
        chunk_size (int): Max characters per chunk
        overlap (int): Number of overlapping characters

    Returns:
        List[str]: List of text chunks
    """

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(chunk.strip())

        # Move start forward, keeping overlap
        start = end - overlap

        if start < 0:
            start = 0

    return chunks
