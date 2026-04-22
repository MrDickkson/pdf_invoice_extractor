from pathlib import Path
import logging
import pandas as pd

from dashboard import generate_dashboard
from exporter import export_to_csv, export_to_excel
from processor import process_folder
from database import init_db, save_results

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FOLDER = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_FILE_CSV = OUTPUT_DIR / "results.csv"
OUTPUT_FILE_EXCEL = OUTPUT_DIR / "results.xlsx"


def main() -> None:
    """Run batch PDF invoice extraction from the data folder."""
    if not DATA_FOLDER.exists():
        logger.error("Data folder does not exist: %s", DATA_FOLDER)
        return

    init_db()

    results = process_folder(DATA_FOLDER)

    if not results:
        logger.warning("No PDF files found in %s", DATA_FOLDER)
        return

    export_to_csv(results, OUTPUT_FILE_CSV)
    export_to_excel(results, OUTPUT_FILE_EXCEL)
    save_results(results)

    df = pd.DataFrame(results)
    summary = {
        "total_files": len(df),
        "successful": len(df[df["status"] == "SUCCESS"]),
        "partial": len(df[df["status"] == "PARTIAL"]),
        "failed": len(df[df["status"] == "FAILED"]),
    }

    logger.info("Summary: %s", summary)
    generate_dashboard(results)


if __name__ == "__main__":
    main()