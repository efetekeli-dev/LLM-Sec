import os
from openai import OpenAI
from core.scorer import SecurityScorer
from core.guardrails import evaluate_with_llm_guard

class LLMSecurityProxy:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self.scorer = SecurityScorer()

    def process_request(self, user_prompt: str) -> dict:
        # Layer 1: Heuristic Risk Scoring & Fast Pattern Matching Engine
        evaluation = self.scorer.evaluate_risk(user_prompt)

        if evaluation["action"] == "BLOCK":
            return {
                "status": "BLOCKED",
                "risk_score": evaluation["risk_score"],
                "message": "Access denied: High-risk pattern detected by Risk Engine."
            }

        # Layer 2: Semantic Analysis via LLM Guardrail
        is_safe, guard_reason = evaluate_with_llm_guard(evaluation["normalized_text"])
        
        if not is_safe:
            return {
                "status": "BLOCKED",
                "risk_score": max(evaluation["risk_score"], 0.90),
                "message": f"Access denied by LLM Guardrail: {guard_reason}"
            }

        # Layer 3: Forward Validated & Sanitized Request to Target LLM
        try:
            response = self.client.chat.completions.create(
                model="qwen/qwen3.8-27b",
                messages=[
                    {"role": "system", "content": "You are a secure, helpful assistant."},
                    {"role": "user", "content": evaluation["normalized_text"]}
                ]
            )
            return {
                "status": "SUCCESS",
                "risk_score": evaluation["risk_score"],
                "response": response.choices[0].message.content
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "message": f"Upstream LLM Execution Error: {str(e)}"
            }
