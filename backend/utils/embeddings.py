from sentence_transformers import SentenceTransformer
import numpy as np


# Load embedding model (you can replace with any SentenceTransformer model)
MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):
    """
    Embed a list of text strings into vectors.

    Args:
        texts (List[str]): List of text chunks

    Returns:
        np.ndarray: 2D array of embeddings
    """
    return MODEL.encode(
        texts,
        show_progress_bar=False,
        convert_to_numpy=True
    )


def embed_text(t: str):
    """
    Embed a single text string.

    Args:
        t (str): Text to embed

    Returns:
        np.ndarray: 1D embedding vector
    """
    return MODEL.encode([t], convert_to_numpy=True)[0]
