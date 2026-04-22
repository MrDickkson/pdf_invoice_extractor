from pathlib import Path
from typing import Any
import logging
import re

import pdfplumber

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: Path) -> str:
    """Extract all text from a PDF file."""
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    return text


def extract_invoice_number(text: str) -> str | None:
    """Extract invoice number from text."""
    patterns = [
        r"Invoice\s*(?:Number|No\.?|#)?[:\s]+([A-Za-z0-9-]+)",
        r"#\s*([A-Za-z0-9-]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def extract_date(text: str) -> str | None:
    """Extract invoice date from text."""
    patterns = [
        r"([A-Za-z]{3}\s\d{2}\s\d{4})",     # Mar 06 2012
        r"([A-Za-z]{3}\s\d{1,2},\s\d{4})",  # Jun 5, 2023
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    return None


def extract_amount(text: str) -> str | None:
    """Extract invoice total amount from text."""
    total_match = re.search(r"Total:\s*\$?([0-9,.]+)", text, re.IGNORECASE)
    if total_match:
        return total_match.group(1)

    amounts = re.findall(r"\$([0-9,.]+)", text)
    if amounts:
        return amounts[-1]

    return None


def extract_order_id(text: str) -> str | None:
    """Extract order ID from text."""
    match = re.search(r"Order ID\s*:\s*([A-Za-z0-9-]+)", text, re.IGNORECASE)
    if match:
        return match.group(1)

    return None


def extract_data_from_pdf(file_path: Path) -> dict[str, Any]:
    """Extract invoice fields from a PDF file."""
    data: dict[str, Any] = {
        "invoice_number": None,
        "date": None,
        "amount": None,
        "order_id": None,
    }

    try:
        text = extract_text_from_pdf(file_path)

        data["invoice_number"] = extract_invoice_number(text)
        data["date"] = extract_date(text)
        data["amount"] = extract_amount(text)
        data["order_id"] = extract_order_id(text)

    except Exception:
        logger.exception("Error processing file: %s", file_path)

    return data