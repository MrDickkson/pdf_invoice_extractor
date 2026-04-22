from pathlib import Path
import sqlite3
from typing import Any

DB_PATH = Path("invoice_results.db")


def get_connection() -> sqlite3.Connection:
    """Create and return a SQLite connection."""
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """Create the invoices table if it does not exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                invoice_number TEXT,
                date TEXT,
                amount REAL,
                order_id TEXT,
                status TEXT NOT NULL,
                errors TEXT
            )
            """
        )
        conn.commit()


def save_results(results: list[dict[str, Any]]) -> None:
    """Save extracted invoice results to SQLite."""
    with get_connection() as conn:
        conn.executemany(
            """
            INSERT INTO invoices (
                file_name,
                invoice_number,
                date,
                amount,
                order_id,
                status,
                errors
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    result.get("file_name"),
                    result.get("invoice_number"),
                    result.get("date"),
                    _to_float(result.get("amount")),
                    result.get("order_id"),
                    result.get("status"),
                    result.get("errors"),
                )
                for result in results
            ],
        )
        conn.commit()


def fetch_all_results() -> list[tuple]:
    """Fetch all saved invoice rows."""
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT
                id,
                file_name,
                invoice_number,
                date,
                amount,
                order_id,
                status,
                errors
            FROM invoices
            ORDER BY id DESC
            """
        )
        return cursor.fetchall()


def _to_float(value: Any) -> float | None:
    """Convert amount values safely to float."""
    if value is None or value == "":
        return None
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None