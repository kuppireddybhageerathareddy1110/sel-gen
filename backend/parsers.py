import json
from bs4 import BeautifulSoup
import fitz  # PyMuPDF


def parse_pdf_bytes(b: bytes):
    """Extract text from PDF using PyMuPDF."""
    text = ""
    doc = fitz.open(stream=b, filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text, None


def parse_html_bytes(b: bytes):
    """Extract visible text and raw HTML."""
    s = b.decode("utf-8", errors="ignore")
    soup = BeautifulSoup(s, "html.parser")
    text = soup.get_text(separator="\n")
    return text, s


def parse_text_bytes(b: bytes):
    """Parse plain text or MD files."""
    return b.decode("utf-8", errors="ignore"), None


def parse_json_bytes(b: bytes):
    """Parse JSON file and pretty print it."""
    obj = json.loads(b)
    pretty = json.dumps(obj, indent=2)
    return pretty, None


def parse_any_file(filename: str, content: bytes):
    """
    Auto-detect file type and return:
    - extracted text
    - raw html (if applicable)
    """
    fname = filename.lower()

    if fname.endswith(".pdf"):
        return parse_pdf_bytes(content)

    if fname.endswith(".html") or fname.endswith(".htm"):
        return parse_html_bytes(content)

    if fname.endswith(".json"):
        return parse_json_bytes(content)

    if fname.endswith(".md") or fname.endswith(".txt"):
        return parse_text_bytes(content)

    # fallback
    try:
        return parse_text_bytes(content)
    except:
        return "", None
