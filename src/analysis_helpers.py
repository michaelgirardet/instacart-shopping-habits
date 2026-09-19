"""Helpers pour l'exploration : tables annexes."""

from pathlib import Path

import pandas as pd

from src.prepare_data import DEFAULT_DATA_DIR


def load_departments(data_dir: str | Path | None = None) -> pd.DataFrame:
    data_dir = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR
    df = pd.read_csv(data_dir / "departments.csv")
    # Normalize department labels: prefer ampersand for clarity (Dairy & Eggs)
    df['department'] = df['department'].astype(str).str.replace(
        r'(?i)\bdairy\s*eggs\b', 'dairy & eggs', regex=True
    )
    return df
