import json
from .rag_engine import HTML_SOURCES, search_kb
from .llm_wrapper import call_llm


def generate_selenium_script_for_test(test_case: dict, html_filename_hint: str = None):
    """
    Generate a complete Selenium Python script for one test case.
    - Includes relevant HTML
    - Includes relevant documentation
    - Enforces use of valid selectors
    """

    # 1. Select correct HTML source
    if html_filename_hint and html_filename_hint in HTML_SOURCES:
        html_source = HTML_SOURCES[html_filename_hint]
    else:
        html_source = next(iter(HTML_SOURCES.values()), "")

    # 2. Retrieve relevant documentation
    query = f"{test_case.get('Feature', '')} {test_case.get('Test_Scenario', '')}"
    docs = search_kb(query, top_k=4)

    context = "\n\n".join(
        f"[source: {d.get('source')}]\n{d.get('text')}"
        for d in docs if d.get("text")
    )

    # 3. Construct LLM prompt
    prompt = f"""
You are a Selenium (Python) expert.

Generate a complete, runnable Selenium script for the following test case.
Use webdriver-manager and Chrome WebDriver.

TEST CASE:
{json.dumps(test_case, indent=2)}

HTML SOURCE (first 4000 chars):
{html_source[:4000]}

CONTEXT DOCS:
{context}

RULES:
- Use only selectors that actually appear in the HTML.
- Use WebDriverWait where appropriate.
- Include comments referencing Grounded_In.
- Output ONLY the final Python script. No explanations.
"""

    # 4. Generate script via LLM
    return call_llm(prompt, temperature=0.0)
