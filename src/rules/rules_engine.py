def is_vip(row):
    return row["TOTAL_SPENT"] > 2500 and row["RETURN_RATE"] < 0.3


def decide(row, extracted):
    if extracted.legal_threat:
        return "ESCALATE_LEGAL"

    category = str(row.get("CATEGORY", ""))
    if "Premium" in category or category == "Bielizna":
        return "MANUAL_INSPECTION"

    if is_vip(row) and extracted.request != "Wymiana":
        return "AUTO_REFUND"

    if (
        extracted.sentiment <= 2 and
        extracted.reason == "Opóźnienie w Dostawie"
    ):
        return "DISCOUNT_15"

    return "STANDARD_RETURN_PROCEDURE"