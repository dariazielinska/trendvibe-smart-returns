import json
import re
from openai import OpenAI
from src.utils.config import OPENAI_API_KEY
from src.models.schemas import ExtractionResult

client = OpenAI(api_key=OPENAI_API_KEY)


def clean_json(text: str) -> str:
    """
    Usuwa zbędne elementy z odpowiedzi LLM i wyciąga czysty JSON
    """
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE)

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)

    return text.strip()


def extract(message: str) -> ExtractionResult:
    prompt = f"""
Zwróć WYŁĄCZNIE JSON (bez komentarzy, bez dodatkowego tekstu).

Format:
{{
  "reason": "Uszkodzenie | Zły Rozmiar | Opóźnienie w Dostawie | Inne",
  "sentiment": 1-5,
  "request": "Zwrot Środków | Wymiana | Brak Sprecyzowania",
  "legal_threat": true/false
}}

Zasady:
- jeśli klient wspomina o prawniku, sądzie, UOKiK → legal_threat = true
- jeśli problem z dostawą → Opóźnienie w Dostawie
- jeśli produkt uszkodzony → Uszkodzenie
- jeśli rozmiar nie pasuje → Zły Rozmiar

Wiadomość:
\"\"\"{message}\"\"\"
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        raw = response.choices[0].message.content.strip()

        cleaned = clean_json(raw)

        data = json.loads(cleaned)

        return ExtractionResult(**data)

    except Exception as e:
        print("LLM parsing error:", e)

        return ExtractionResult(
            reason="Inne",
            sentiment=3,
            request="Brak Sprecyzowania",
            legal_threat=False,
            confidence=0.0
        )