from openai import OpenAI
from src.utils.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_response(status, extracted, row):
    prompt = f"""
Napisz uprzejmego maila do klienta sklepu TrendVibe.

Dane:
- Powód zgłoszenia: {extracted.reason}
- Nastrój klienta (1-5): {extracted.sentiment}
- Decyzja: {status}

Dostosuj ton:
- jeśli sentiment ≤ 2 → bardziej empatyczny
- jeśli sentiment ≥ 4 → neutralny / pozytywny

Instrukcje:
- odnieś się konkretnie do problemu klienta
- nie pisz ogólników
- max 5-6 zdań
- język: naturalny, ludzki

Decyzje:
- AUTO_REFUND → poinformuj o zwrocie pieniędzy
- DISCOUNT_15 → zaproponuj rabat 15%
- STANDARD_RETURN_PROCEDURE → opisz standardową procedurę

Podpisz jako:
Zespół TrendVibe

Mail:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()