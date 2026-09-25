import re
from core.normalizer import TextNormalizer

class SecurityScorer:
    def __init__(self):
        self.normalizer = TextNormalizer()
        self.jailbreak_keywords = [
            "ignore previous instructions", 
            "system prompt", 
            "developer mode", 
            "god mode"
        ]
        self.sql_patterns = [r"union\s+select", r"drop\s+table", r"--;"]

    def evaluate_risk(self, raw_text: str) -> dict:
        text = self.normalizer.normalize(raw_text)
        text_lower = text.lower()
        
        risk_score = 0.0

        # Excessive input length penalty
        if len(text) > 4000:
            risk_score += 0.3

        # Check for known jailbreak keywords
        for kw in self.jailbreak_keywords:
            if kw in text_lower:
                risk_score += 0.4

        # Check for SQL injection signature patterns
        for pattern in self.sql_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                risk_score += 0.5

        final_score = min(round(risk_score, 2), 1.0)

        action = "ALLOW"
        if final_score >= 0.8:
            action = "BLOCK"
        elif final_score >= 0.4:
            action = "REVIEW_AND_SANITIZE"

        return {
            "normalized_text": text,
            "risk_score": final_score,
            "action": action
        }
