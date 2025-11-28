from .utils.chunker import chunk_text
from .utils.embeddings import embed_texts, embed_text
from .utils.db import DB

# Store raw HTML sources in memory
HTML_SOURCES = {}


def ingest_document(text: str, metadata: dict):
    """
    Splits document into chunks, embeds each chunk,
    and stores embeddings + metadata in the vector database.
    """
    chunks = chunk_text(text)
    vecs = embed_texts(chunks)

    for chunk, vec in zip(chunks, vecs):
        md = metadata.copy()
        md.update({"text": chunk})
        DB.add(vec, md)


def store_html_source(filename: str, raw_html: str):
    """
    Save raw HTML source to in-memory storage for script generation.
    """
    HTML_SOURCES[filename] = raw_html


def get_html_source(filename: str):
    """
    Retrieve stored HTML source by filename.
    """
    return HTML_SOURCES.get(filename)


def search_kb(query: str, top_k: int = 5):
    """
    Embed the query, search the vector DB, and return metadata
    for the top_k most relevant chunks.
    """
    qv = embed_text(query)
    results = DB.search(qv, top_k=top_k)

    # Extract metadata only
    return [r["metadata"] for r in results]
