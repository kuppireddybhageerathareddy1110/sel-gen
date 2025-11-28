import json
from .rag_engine import search_kb
from .llm_wrapper import call_llm


def generate_test_cases_from_query(query: str):
    """
    Generate RAG-based test cases for a given feature/query.
    """

    retrieved = search_kb(query, top_k=6)

    context = "\n\n".join(
        f"[source: {r.get('source')}]\n{r.get('text')}"
        for r in retrieved if r.get("text")
    )

    # Build prompt
    prompt = f"""
You are a QA engineer.

Using only the CONTEXT below, create 6–12 test cases in JSON array format.
Each test case must contain:
- Test_ID
- Feature
- Test_Scenario
- Steps
- Expected_Result
- Grounded_In (source document)

CONTEXT:
{context}

USER QUERY:
{query}

Rules:
- DO NOT hallucinate features.
- Only generate cases derived from context.
"""

    response = call_llm(prompt, temperature=0.0)

    # Return valid JSON if possible
    try:
        return json.loads(response)
    except:
        return [{"raw": response}]
