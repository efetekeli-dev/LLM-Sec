# LLM-Sec: AI Security Guardrail Proxy 🛡️

A lightweight, high-performance security gateway for Large Language Models (LLMs) built with **FastAPI** and powered by **Groq (`qwen/qwen3.8-27b`)**.

`LLM-Sec` acts as an inspection layer between end-users and the LLM API to mitigate threats like **Prompt Injection**, **System Prompt Leakage**, and **Jailbreak attempts** before they reach the main model.

---

## 🏗️ Architecture & Security Pipeline

Every incoming prompt undergoes a multi-layered verification process:

1. **Input Normalizer (`core/normalizer.py`)**: Sanitizes inputs, removes zero-width characters, obfuscated encoding, and standardizes text formats.
2. **Pattern Risk Scorer (`core/scorer.py`)**: Evaluates attack patterns using heuristics and regular expressions to assign a threat probability score.
3. **Semantic Guardrails (`core/guardrails.py`)**: Enforces policy checks and context-aware guardrails.
4. **LLM Proxy (`core/proxy.py`)**: Securely proxies safe requests to the underlying Groq LLM endpoint.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- A valid **Groq API Key**

### 2. Installation & Setup

Clone the repository:
```bash
git clone [https://github.com/efetekeli-dev/LLM-Sec.git](https://github.com/efetekeli-dev/LLM-Sec.git)
cd LLM-Sec

#Set up a virtual environment and install dependencies: 

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


#Set your environment variables:

export GROQ_API_KEY="your_groq_api_key_here"


#Start the FastAPI application using Uvicorn: 

uvicorn api:app --port 8000 --reload



