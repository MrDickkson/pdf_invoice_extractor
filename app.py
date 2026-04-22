from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from processor import process_folder

DATA_FOLDER = Path("data")

st.set_page_config(page_title="Invoice Dashboard", layout="wide")
st.title("PDF Invoice Dashboard")
st.write("Process all PDF invoices in the local data folder.")


def build_dataframe() -> pd.DataFrame:
    """Process PDFs and return results as a DataFrame."""
    results = process_folder(DATA_FOLDER)
    return pd.DataFrame(results)


if st.button("Run Processing"):
    if not DATA_FOLDER.exists():
        st.error(f"Data folder does not exist: {DATA_FOLDER}")
    else:
        df = build_dataframe()

        if df.empty:
            st.warning("No PDF files found in the data folder.")
        else:
            st.success("Processing complete.")

            st.subheader("Invoice Data")
            st.dataframe(df, use_container_width=True)

            st.subheader("Summary Metrics")
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Total Files", len(df))
            col2.metric("Success", len(df[df["status"] == "SUCCESS"]))
            col3.metric("Partial", len(df[df["status"] == "PARTIAL"]))
            col4.metric("Failed", len(df[df["status"] == "FAILED"]))

            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
            total_revenue = df["amount"].sum()
            st.metric("Total Revenue", f"${total_revenue:.2f}")

            st.subheader("Status Breakdown")
            fig, ax = plt.subplots()
            df["status"].value_counts().plot(kind="bar", ax=ax)
            plt.tight_layout()
            st.pyplot(fig)