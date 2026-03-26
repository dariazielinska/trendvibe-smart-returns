from pydantic import BaseModel
from typing import Literal


class ExtractionResult(BaseModel):
    reason: Literal[
        "Uszkodzenie",
        "Zły Rozmiar",
        "Opóźnienie w Dostawie",
        "Inne"
    ]
    sentiment: int
    request: Literal[
        "Zwrot Środków",
        "Wymiana",
        "Brak Sprecyzowania"
    ]
    legal_threat: bool
    confidence: float = 1.0