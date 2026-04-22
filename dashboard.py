from typing import Any

import matplotlib.pyplot as plt
import pandas as pd


def generate_dashboard(data_list: list[dict[str, Any]]) -> None:
    """Generate a simple summary dashboard with console output and chart."""
    df = pd.DataFrame(data_list)

    if df.empty:
        print("No data available for dashboard.")
        return

    if "status" not in df.columns:
        print("Dashboard cannot be generated: missing 'status' column.")
        return

    total_files = len(df)
    success_count = len(df[df["status"] == "SUCCESS"])
    partial_count = len(df[df["status"] == "PARTIAL"])
    failed_count = len(df[df["status"] == "FAILED"])

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    total_revenue = df["amount"].sum()
    zero_amount_count = len(df[df["amount"] == 0])

    print("\n===== DASHBOARD SUMMARY =====")
    print(f"Total Files: {total_files}")
    print(f"Success: {success_count}")
    print(f"Partial: {partial_count}")
    print(f"Failed: {failed_count}")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Zero Amount Invoices: {zero_amount_count}")

    labels = ["SUCCESS", "PARTIAL", "FAILED"]
    values = [success_count, partial_count, failed_count]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Invoice Processing Status")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()