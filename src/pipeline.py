from src.llm.llm_extractor import extract
from src.rules.rules_engine import decide
from src.llm.llm_generator import generate_response
from datetime import datetime

AUTO_STATUSES = {
    "AUTO_REFUND",
    "DISCOUNT_15",
    "STANDARD_RETURN_PROCEDURE"
}

MANUAL_STATUSES = {
    "ESCALATE_LEGAL",
    "MANUAL_INSPECTION"
}


def process(df):
    auto_results = []
    manual_results = []

    for _, row in df.iterrows():
        try:
            extracted = extract(row["CUSTOMER_MESSAGE"])
            status = decide(row, extracted)

            processed_date = datetime.now().strftime("%Y-%m-%d")

            if status in AUTO_STATUSES:
                response_text = generate_response(status, extracted, row)

                auto_results.append({
                    "TICKET_ID": row["TICKET_ID"],
                    "CUSTOMER_ID": row.get("CUSTOMER_ID"),
                    "ORDER_ID": row.get("ORDER_ID"),
                    "PRODUCT_ID": row.get("PRODUCT_ID"),
                    "REASON": extracted.reason,
                    "SENTIMENT": extracted.sentiment,
                    "STATUS": status,
                    "RESPONSE": response_text,
                    "PROCESSED_AT": processed_date
                })

            else:
                manual_results.append({
                    "TICKET_ID": row["TICKET_ID"],
                    "CUSTOMER_ID": row.get("CUSTOMER_ID"),
                    "ORDER_ID": row.get("ORDER_ID"),
                    "PRODUCT_ID": row.get("PRODUCT_ID"),
                    "REASON": extracted.reason,
                    "SENTIMENT": extracted.sentiment,
                    "STATUS": status,
                    "PROCESSED_AT": processed_date
                })

        except Exception as e:
            print(f"Error processing ticket {row.get('TICKET_ID')}: {e}")

    manual_results = sorted(
        manual_results,
        key=lambda x: 0 if x["STATUS"] == "ESCALATE_LEGAL" else 1
    )

    return auto_results, manual_results