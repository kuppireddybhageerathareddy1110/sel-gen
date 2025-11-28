from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from typing import List
import uvicorn

from backend.parsers import parse_any_file
from backend.rag_engine import ingest_document, store_html_source, search_kb
from backend.test_case_agent import generate_test_cases_from_query
from backend.script_agent import generate_selenium_script_for_test


app = FastAPI()

UPLOADED_DOCS = []


@app.post("/build_kb")
async def build_kb(docs: List[UploadFile] = File(...)):
    """
    Endpoint accepts a list of files (support docs + checkout.html).
    """
    html_source = None

    for f in docs:
        content = await f.read()
        text, raw = parse_any_file(f.filename, content)
        metadata = {"source": f.filename}

        ingest_document(text, metadata)

        if f.filename.lower().endswith(".html"):
            store_html_source(f.filename, raw)

        UPLOADED_DOCS.append(f.filename)

    return JSONResponse({"message": "Knowledge Base Built", "uploaded": UPLOADED_DOCS})


@app.post("/generate_test_cases")
async def generate_test_cases(query: str = Form(...)):
    """
    Generate test cases based on user query using RAG + LLM.
    """
    cases = generate_test_cases_from_query(query)
    return JSONResponse({"test_cases": cases})


@app.post("/generate_script")
async def generate_script(test_id: str = Form(...)):
    """
    Convert selected test case into Selenium Python script.
    """
    import json

    test_case = json.loads(test_id)
    script = generate_selenium_script_for_test(test_case)
    return JSONResponse({"script": script})


if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
