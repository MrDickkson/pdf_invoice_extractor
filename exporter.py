from pathlib import Path
from typing import Any

import pandas as pd


def export_to_csv(data_list: list[dict[str, Any]], output_path: Path) -> None:
    """Export extracted data to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(data_list)
    df.to_csv(output_path, index=False)


def export_to_excel(data_list: list[dict[str, Any]], output_path: Path) -> None:
    """Export extracted data to Excel."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(data_list)
    df.to_excel(output_path, index=False)