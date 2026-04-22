from typing import Any


def validate_data(data: dict[str, Any]) -> list[str]:
    """Validate extracted invoice data."""
    errors: list[str] = []

    if not data.get("invoice_number"):
        errors.append("Missing invoice number")

    if not data.get("date"):
        errors.append("Missing date")

    amount = data.get("amount")
    if amount is None:
        errors.append("Missing amount")
    else:
        try:
            numeric_amount = float(str(amount).replace(",", ""))
            if numeric_amount == 0:
                errors.append("Zero amount invoice")
        except ValueError:
            errors.append("Invalid amount format")

    return errors