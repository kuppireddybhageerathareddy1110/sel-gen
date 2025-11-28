import streamlit as st
import requests
import json

# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Autonomous QA Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🤖 Autonomous QA Agent — Test Case & Selenium Script Generator")

st.write("Upload documents, build a knowledge base, generate test cases, then produce Selenium scripts.")


# -----------------------------
# 1) Upload Support Documents & HTML
# -----------------------------
st.header("📁 Step 1: Upload Support Documents & checkout.html")

uploaded_files = st.file_uploader(
    "Upload support files (PDF, MD, TXT, JSON, HTML)",
    type=["pdf", "md", "txt", "json", "html"],
    accept_multiple_files=True
)

if st.button("📦 Build Knowledge Base"):
    if not uploaded_files:
        st.error("Please upload at least one support document including checkout.html.")
    else:
        files = []

        for f in uploaded_files:
            files.append(
                (
                    "docs",
                    (f.name, f.getvalue(), "application/octet-stream")
                )
            )

        try:
            response = requests.post(
                "http://localhost:8000/build_kb",
                files=files
            )

            if response.status_code == 200:
                st.success("Knowledge Base Built Successfully!")
                st.json(response.json())
            else:
                st.error("❌ Backend error: " + response.text)

        except Exception as e:
            st.error(f"❌ Failed to connect to backend: {e}")


# -----------------------------
# 2) Generate Test Cases
# -----------------------------
st.header("🧪 Step 2: Generate Test Cases")

query = st.text_input(
    "Enter your test-case prompt (Example: Generate all positive and negative test cases for discount code)"
)

if st.button("📝 Generate Test Cases"):
    if not query:
        st.error("Please enter a query.")
    else:
        try:
            response = requests.post(
                "http://localhost:8000/generate_test_cases",
                data={"query": query}
            )

            if response.status_code == 200:
                result = response.json()
                test_cases = result.get("test_cases", [])

                if not test_cases:
                    st.warning("No test cases generated.")
                else:
                    st.success("Test Cases Generated!")
                    st.session_state["test_cases"] = test_cases
                    st.json(test_cases)

            else:
                st.error("❌ Backend error: " + response.text)

        except Exception as e:
            st.error(f"❌ Failed to connect to backend: {e}")


# -----------------------------
# 3) Generate Selenium Script
# -----------------------------
st.header("🤖 Step 3: Generate Selenium Script")

if "test_cases" in st.session_state:
    test_case_strings = [
        json.dumps(tc, indent=2) for tc in st.session_state["test_cases"]
    ]

    selected_case = st.selectbox(
        "Select a test case to convert into Selenium script:",
        test_case_strings
    )

    if st.button("⚙️ Generate Selenium Script"):
        try:
            response = requests.post(
                "http://localhost:8000/generate_script",
                data={"test_id": selected_case}
            )

            if response.status_code == 200:
                script = response.json().get("script")
                st.success("Selenium Script Generated!")
                st.code(script, language="python")
            else:
                st.error("❌ Backend error: " + response.text)

        except Exception as e:
            st.error(f"❌ Failed to connect to backend: {e}")

else:
    st.info("Please generate test cases first to enable this section.")
