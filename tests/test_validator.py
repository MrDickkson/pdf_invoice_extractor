
from validator import validate_data


def test_validate_data_success():
    data = {
        "invoice_number": "12345",
        "date": "Mar 06 2012",
        "amount": "58.11",
        "order_id": "CA-2012-AB10015140-40974",
    }

    errors = validate_data(data)
    assert errors == []


def test_validate_data_missing_fields():
    data = {
        "invoice_number": None,
        "date": None,
        "amount": None,
        "order_id": None,
    }

    errors = validate_data(data)
    assert "Missing invoice number" in errors
    assert "Missing date" in errors
    assert "Missing amount" in errors


def test_validate_zero_amount():
    data = {
        "invoice_number": None,
        "date": "Jun 5, 2023",
        "amount": "0.00",
        "order_id": None,
    }

    errors = validate_data(data)
    assert "Zero amount invoice" in errors