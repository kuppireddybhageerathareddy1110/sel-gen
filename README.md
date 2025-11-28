
---

# 📘 **Autonomous QA Agent — Test Case & Selenium Script Generator**

An intelligent **RAG-powered QA automation agent** that reads project documentation + HTML, builds a knowledge base, generates **grounded test cases**, and produces **runnable Selenium Python scripts**.

Backend → **FastAPI**
Frontend → **Streamlit**
RAG Engine → **FAISS + SentenceTransformer**
LLM → **Groq (Mixtral-8x7B)**
Documents → Product Specs, UI/UX Guide, API doc, checkout.html

---

# 🚀 **Features**

### ✅ **1. Knowledge Base Builder**

* Upload support docs (PDF, MD, TXT, JSON, HTML)
* Extract text using custom parsers (PyMuPDF, BeautifulSoup, JSON loader)
* Chunk text using sliding window
* Generate embeddings using `all-MiniLM-L6-v2`
* Store vectors + metadata in FAISS DB
* Store raw HTML separately for script generation

---

### ✅ **2. RAG Test Case Generator**

User enters query:

```
Generate all positive and negative test cases for the discount code feature
```

Pipeline:

1. Embed query
2. Retrieve top-K relevant chunks from vector DB
3. Pass context + query to LLM (Groq)
4. Generate structured output:

   * Test_ID
   * Feature
   * Test_Scenario
   * Steps[]
   * Expected_Result
   * Grounded_In (document source)

---

### ✅ **3. Selenium Script Generator**

* Select a test case
* Pass HTML + context + test case to LLM
* LLM generates **runnable Selenium Python code**
* Selenium uses:

  * Chrome WebDriver
  * WebDriverWait
  * Correct HTML selectors

---

# 📁 **Project Structure**

```
qa-autonomous-agent/
│
├── backend/
│   ├── app.py                 # FastAPI server
│   ├── parsers.py             # PDF/HTML/JSON/Text parser
│   ├── rag_engine.py          # Chunk → Embed → Store → Search
│   ├── llm_wrapper.py         # Groq LLM wrapper
│   ├── test_case_agent.py     # Generate test cases using RAG
│   ├── script_agent.py        # Generate Selenium scripts
│   └── utils/
│       ├── chunker.py
│       ├── embeddings.py
│       └── db.py
│
├── streamlit_app/
│   └── ui.py                  # Main user interface
│
├── assets/
│   ├── checkout.html          # Target project HTML
│   ├── product_specs.md       # Support doc
│   ├── ui_ux_guide.txt
│   ├── api_endpoints.json
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ **Installation & Setup**

### **1. Clone the repository**

```bash
git clone https://github.com/<your_username>/sel-gen.git
cd sel-gen
```

---

### **2. Create virtual environment**

```bash
python -m venv venv
venv\Scripts\activate       # Windows
```

---

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

---

### **4. Setup environment variables**

Create a file called **.env** (not included in repo):

```
GROQ_API_KEY=your_groq_api_key
HF_API_TOKEN=your_hf_token   # optional if using huggingface models
```

(Use `.env.example` as reference)

---

# ▶️ **Running the Application**

### **1. Start FastAPI backend**

```bash
uvicorn backend.app:app --reload --port 8000
```

Server runs at:
👉 [http://localhost:8000](http://localhost:8000)

---

### **2. Start Streamlit UI**

```bash
streamlit run streamlit_app/ui.py
```

UI runs at:
👉 [http://localhost:8501](http://localhost:8501)

---

# 🧭 **How to Use**

## **Step 1 — Upload Files & Build KB**

In Streamlit:

1. Upload:

   * checkout.html
   * product_specs.md
   * ui_ux_guide.txt
   * api_endpoints.json
   * Any PDF support docs
2. Click **“Build Knowledge Base”**

You will see:

```
Knowledge Base Built!
```

---

## **Step 2 — Generate Test Cases**

1. Enter query:

```
Generate positive and negative test cases for discount code
```

2. Click **Generate Test Cases**
3. JSON output appears & saved in session

---

## **Step 3 — Generate Selenium Script**

1. Choose a test case from dropdown
2. Click **Generate Selenium Script**
3. A runnable Python script appears with:

   * Selectors matched to HTML
   * WebDriverWait
   * Comments referencing grounding docs

---

# 🔍 **How RAG Works (Internal Architecture)**

### **1. Document Parsing**

| Type   | Library       | Notes                 |
| ------ | ------------- | --------------------- |
| PDF    | PyMuPDF       | Extracts page text    |
| HTML   | BeautifulSoup | Raw HTML + inner text |
| JSON   | json          | Pretty-formatted      |
| MD/TXT | builtin       | Direct decode         |

---

### **2. Chunking**

```python
chunk_size = 800 characters
overlap = 100 characters
```

Ensures maximum context recall.

---

### **3. Embeddings**

Using **all-MiniLM-L6-v2** (384-dimensional vectors):

* Lightweight
* Fast CPU inference
* Ideal for QA knowledge bases

---

### **4. Vector DB (FAISS)**

Stores:

* embeddings
* metadata (source file, chunk text)

Searches via cosine similarity.

---

### **5. LLM (Groq Mixtral)**

Two agent chains:

### **Test Case Agent**

* Retrieves chunks
* Sends strict JSON prompt
* Ensures grounding in documents

### **Selenium Script Agent**

* Inputs:

  * Test Case
  * HTML Source
  * Relevant docs
* Produces runnable automation script

---

# 📦 **Included Support Documents**

### **checkout.html**

A full interactive checkout page containing:

* Add to cart
* Cart summary
* Discount input
* User details form
* Form validation
* Shipping radio buttons
* Payment radio buttons
* Pay Now → “Payment Successful!”

### **product_specs.md**

Examples:

```
SAVE15 = 15% discount
Express shipping = $10
Standard shipping = free
```

### **ui_ux_guide.txt**

Examples:

```
Validation errors must appear in red
"Pay Now" button should be green
```

### **api_endpoints.json**

Mock API endpoints for submit order.

---

# 🧪 **Example Output**

### **Generated Test Case**

```json
{
  "Test_ID": "TC-001",
  "Feature": "Discount Code",
  "Test_Scenario": "Apply valid discount SAVE15",
  "Steps": ["Enter SAVE15", "Click Apply"],
  "Expected_Result": "Price reduces by 15%",
  "Grounded_In": "product_specs.md"
}
```

---

### **Generated Selenium Script (excerpt)**

```python
driver.find_element(By.ID, "discount_code").send_keys("SAVE15")
driver.find_element(By.ID, "apply_discount").click()
WebDriverWait(driver, 10).until(
    EC.text_to_be_present_in_element((By.ID, "total_price"), ""))
```

---


---

# 📌 **Future Improvements**

* Persistent vector DB (Chroma / Qdrant)
* Multi-page HTML crawling
* Full E2E automation execution
* Downloadable ZIP of test scripts

---

# 🤝 **Contributions**

PRs welcome!
Open issues for bugs or enhancements.

---

# 📄 **License**

MIT License.

---
report
🎥 A full demo video script
