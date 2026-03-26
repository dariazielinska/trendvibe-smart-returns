from src.models.schemas import ExtractionResult


def mock_extraction():
    return ExtractionResult(
        reason="Uszkodzenie",
        sentiment=2,
        request="Zwrot Środków",
        legal_threat=False,
        confidence=0.9
    )