"""
data_processor.py
------------------
Contains the actual "processing" logic applied to data downloaded from Azure.
This is a simple example (CSV cleaning + a derived column) — replace the body
of `process_csv` with whatever transformation your project actually needs.
"""

import pandas as pd


def process_csv(input_path: str, output_path: str) -> str:
    """
    Reads a CSV file, cleans it, adds a derived column, and writes the result
    to a new CSV file.

    Example transformations included:
      - Drop fully empty rows
      - Strip whitespace from string columns
      - Fill missing numeric values with the column mean
      - Add a derived column showing each row's percentage of the 'amount' column total
        (only if an 'amount' column exists — otherwise this step is skipped)
    """
    df = pd.read_csv(input_path)

    # 1. Drop rows that are entirely empty
    df = df.dropna(how="all")

    # 2. Strip whitespace from text columns
    string_cols = df.select_dtypes(include="object").columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    # 3. Fill missing numeric values with the column mean
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].mean())

    # 4. Example derived column
    if "amount" in df.columns:
        total = df["amount"].sum()
        df["percent_of_total"] = (df["amount"] / total * 100).round(2) if total else 0

    df.to_csv(output_path, index=False)
    print(f"Processed data written to '{output_path}'")
    return output_path
