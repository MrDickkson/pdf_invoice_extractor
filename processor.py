from pathlib import Path
from typing import Any

from extractor import extract_data_from_pdf
from validator import validate_data


def process_pdf(file_path: Path) -> dict[str, Any]:
    """Process one PDF and return normalized invoice data."""
    data = extract_data_from_pdf(file_path)
    errors = validate_data(data)

    if "Missing amount" in errors:
        status = "FAILED"
    elif errors:
        status = "PARTIAL"
    else:
        status = "SUCCESS"

    data["status"] = status
    data["errors"] = ", ".join(errors)
    data["file_name"] = file_path.name

    return data


def process_folder(folder_path: Path) -> list[dict[str, Any]]:
    """Process all PDF files in a folder."""
    results: list[dict[str, Any]] = []

    for file_path in folder_path.glob("*.pdf"):
        results.append(process_pdf(file_path))

    return results