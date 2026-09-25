import re
import base64

class TextNormalizer:
    @staticmethod
    def normalize(text: str) -> str:
        if not text:
            return ""
        
        # 1. Clean excessive whitespaces and hidden Unicode characters (e.g., Zero-Width spaces)
        cleaned = re.sub(r'\s+', ' ', text).strip()
        cleaned = re.sub(r'[\u200b-\u200d\ufeff]', '', cleaned)
        
        # 2. Detect and decode potential Base64 encoded payloads
        # Analyze only if string length is >= 8, valid Base64 length, and matches Base64 character set
        if len(cleaned) >= 8 and len(cleaned) % 4 == 0 and re.match(r'^[A-Za-z0-9+/=]+$', cleaned):
            try:
                decoded_bytes = base64.b64decode(cleaned, validate=True)
                decoded_str = decoded_bytes.decode('utf-8', errors='ignore')
                
                # Check if decoded string contains printable ASCII/UTF-8 characters
                if decoded_str.strip() and all(32 <= ord(c) <= 126 or c in '\n\r\t' for c in decoded_str):
                    cleaned = f"{cleaned} (Decoded Payload: {decoded_str})"
            except Exception:
                pass

        return cleaned
