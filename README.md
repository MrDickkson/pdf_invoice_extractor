# PDF Invoice Extractor

A Python project that extracts key invoice and receipt data from PDF files, validates the results, exports them to CSV/Excel, and visualizes processing outcomes through a simple dashboard and Streamlit web app.

## Features

- Extracts invoice number, date, amount, and order ID from PDF invoices
- Batch processes multiple PDF files from a folder
- Validates missing or suspicious fields
- Exports results to CSV and Excel
- Generates a summary dashboard with status counts and revenue metrics
- Includes a Streamlit app for interactive viewing
- - Stores processed invoice results in SQLite

## Tech Stack

- Python
- pdfplumber
- pandas
- matplotlib
- Streamlit
- openpyxl
