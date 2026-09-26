# LLM-Sec: AI Security Guardrail Proxy 🛡️

A lightweight, high-performance security gateway for Large Language Models (LLMs) built with **FastAPI** and powered by **Groq (`qwen/qwen3.8-27b`)**.

`LLM-Sec` acts as an inspection layer between end-users and the LLM API to mitigate threats like **Prompt Injection**, **System Prompt Leakage**, and **Jailbreak attempts** before they reach the main model.

---

## 🏗️ Architecture & Security Pipeline

Every incoming prompt undergoes a multi-layered verification process:

1. **Input Normalizer (`core/normalizer.py`)**: Sanitizes inputs, removes zero-width characters, obfuscated encoding, and standardizes text formats.
2. **Pattern Risk Scorer (`core/scorer.py`)**: Evaluates attack patterns using heuristics and regular expressions to assign a threat probability score.
3. **Semantic Guardrails (`core/guardrails.py`)**: Enforces policy checks and context-aware guardrails using LLM verification.
4. **LLM Proxy (`core/proxy.py`)**: Securely proxies safe requests to the underlying Groq LLM endpoint.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- A valid **Groq API Key**

### 2. Installation & Setup

Clone the repository:

```
git clone [https://github.com/efetekeli-dev/LLM-Sec.git](https://github.com/efetekeli-dev/LLM-Sec.git)
cd LLM-Sec

Set up a virtual environment and install dependencies:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Set your environment variables:

export GROQ_API_KEY="your_groq_api_key_here"


Start the FastAPI application using Uvicorn:

uvicorn api:app --port 8000 --reload

The API will be live at http://127.0.0.1:8000. You can test the endpoints via Interactive Swagger Docs at http://127.0.0.1:8000/docs.

Running the Fuzzer

While the Uvicorn server is running, execute the fuzzer in a separate terminal:

python3 fuzzer.py

Expected Fuzzer Output:

[*] Starting Local API Test: [http://127.0.0.1:8000/v1/chat/secure-completions](http://127.0.0.1:8000/v1/chat/secure-completions)
==================================================
[+] Payload: 'Normal test message...'
    - Status Code: 200
    - Response: {"status":"SUCCESS","risk_score":0.0,...}

[+] Payload: 'IGNORE PREVIOUS INSTRUCTIONS; ...'
    - Status Code: 403
    - Response: {"detail":{"status":"BLOCKED","message":"Access denied by LLM Guardrail: Attempted system prompt exfiltration..."}}

[+] Payload: '<script>alert(1)</script>...'
    - Status Code: 403
    - Response: {"detail":{"status":"BLOCKED","message":"Access denied by LLM Guardrail: Input contains a Cross-Site Scripting (XSS)..."}}
