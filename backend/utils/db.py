import faiss
import numpy as np
from typing import List, Dict


class VectorDB:
    """
    A simple in-memory FAISS vector database.
    Stores vectors and metadata in parallel lists.
    """

    def __init__(self, dim: int = 384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)  # L2 similarity index
        self.metadatas: List[Dict] = []
        self.vectors: List[np.ndarray] = []

    def add(self, vector: np.ndarray, metadata: dict):
        """
        Add a vector + its metadata to the FAISS index.
        """
        v = np.array([vector]).astype("float32")
        self.index.add(v)
        self.metadatas.append(metadata)
        self.vectors.append(v)

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        """
        Search for the nearest vectors to the query vector.
        Returns a list of metadata dicts.
        """
        q = np.array([query_vector]).astype("float32")
        D, I = self.index.search(q, top_k)

        results = []
        for idx in I[0]:
            if idx < len(self.metadatas):
                results.append({"metadata": self.metadatas[idx]})

        return results


# Create a global DB instance
DB = VectorDB(dim=384)
