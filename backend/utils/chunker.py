from typing import List


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    """
    Simple character-based text chunker.

    Splits text into overlapping chunks:
    - chunk_size: max size of each chunk
    - overlap: how much to overlap between chunks
    """
    chunks = []
    i = 0
    n = len(text)

    while i < n:
        end = i + chunk_size
        chunks.append(text[i:end])
        i = end - overlap  # move pointer backward for overlap

    return chunks
