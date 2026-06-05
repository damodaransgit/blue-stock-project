"""
data_ingestion.py -- Load, Inspect & Validate All Datasets
==========================================================
This script loads all CSV datasets (both the provided ones and the ones
we fetched from the API) and performs initial inspection.

What this script does:
    1. Scans the data/raw/ folder for all CSV files
    2. For each CSV: prints shape, data types, and first 5 rows
    3. Flags anomalies: missing values, duplicate rows, wrong types
    4. Explores fund_master data: unique fund houses, categories, risk grades
    5. Validates AMFI codes: checks if codes in fund_master exist in nav data
    6. Writes a data quality summary report

Key terms for beginners:
    - .shape     -> (rows, columns) -- how big is the data?
    - .dtypes    -> what type is each column? (number, text, date, etc.)
    - .head()    -> shows the first 5 rows (a quick peek)
    - .isnull()  -> finds missing/empty values
    - .duplicated() -> finds duplicate rows
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime


# ------------------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------------------

RAW_DATA_DIR = os.path.join("data", "raw")
PROCESSED_DATA_DIR = os.path.join("data", "processed")
REPORTS_DIR = "reports"


def load_and_inspect_csv(filepath):
    """
    Load a single CSV file and print its basic information.

    This is like opening a spreadsheet and checking:
    - How many rows and columns does it have?
    - What are the column names and their types?
    - What does the first few rows look like?
    - Are there any empty cells?

    Parameters:
        filepath (str): Path to the CSV file

    Returns:
        pandas DataFrame (the loaded data), or None if it fails
    """
    filename = os.path.basename(filepath)
    print(f"\n{'-' * 70}")
    print(f"[FILE] {filename}")
    print(f"   Path: {filepath}")
    print(f"{'-' * 70}")

    try:
        # Load the CSV
        df = pd.read_csv(filepath)

        # 1. Shape: how many rows x columns
        rows, cols = df.shape
        print(f"\n   [SHAPE] {rows:,} rows x {cols} columns")

        # 2. Data types: what type is each column?
        print(f"\n   [DTYPES] Column Data Types:")
        for col_name, col_type in df.dtypes.items():
            print(f"      - {col_name}: {col_type}")

        # 3. First 5 rows: a quick preview
        print(f"\n   [HEAD] First 5 rows:")
        print(df.head().to_string(index=False))

        # 4. Check for anomalies
        print(f"\n   [QUALITY] Data Quality Check:")
        anomalies = []

        # Missing values
        missing = df.isnull().sum()
        total_missing = missing.sum()
        if total_missing > 0:
            print(f"      [WARN] Missing values found: {total_missing} total")
            for col, count in missing[missing > 0].items():
                pct = (count / len(df)) * 100
                print(f"         - {col}: {count} missing ({pct:.1f}%)")
                anomalies.append(f"Missing values in '{col}': {count} ({pct:.1f}%)")
        else:
            print(f"      [OK] No missing values")

        # Duplicate rows
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            print(f"      [WARN] Duplicate rows: {dup_count}")
            anomalies.append(f"Duplicate rows: {dup_count}")
        else:
            print(f"      [OK] No duplicate rows")

        # Check for "N/A", "null", "None" strings (common in raw data)
        for col in df.select_dtypes(include=["object"]).columns:
            bad_values = df[col].isin(["N/A", "null", "None", "NA", "-", ""]).sum()
            if bad_values > 0:
                print(f"      [WARN] Column '{col}' has {bad_values} placeholder values (N/A, null, etc.)")
                anomalies.append(f"Placeholder values in '{col}': {bad_values}")

        # Memory usage
        mem_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
        print(f"\n   [MEM] Memory usage: {mem_mb:.2f} MB")

        return df, anomalies

    except Exception as e:
        print(f"   [ERROR] Error loading {filename}: {e}")
        return None, [f"Failed to load: {e}"]


def explore_fund_master(df, filename):
    """
    Explore the fund_master dataset specifically.

    Fund master is like a "phone book" of all mutual funds in India.
    Each row is one fund scheme, with details like:
    - Fund house (e.g., HDFC, SBI, ICICI)
    - Category (e.g., Equity, Debt, Hybrid)
    - Sub-category (e.g., Large Cap, Mid Cap, Small Cap)
    - Risk grade (e.g., High, Moderate, Low)
    - AMFI scheme code (unique ID for each fund)
    """
    # Only run this for files that look like fund_master
    if "fund_master" not in filename.lower() and "combined" not in filename.lower():
        return

    print(f"\n{'=' * 70}")
    print(f"[EXPLORE] FUND MASTER EXPLORATION: {filename}")
    print(f"{'=' * 70}")

    # Try to find and print unique values for key columns
    # (Column names might vary, so we check for common names)

    column_mapping = {
        "fund_house": ["fund_house", "Fund_House", "amc_name", "AMC", "fund_family", "Mutual_Fund_Family"],
        "category": ["category", "Category", "scheme_category", "Scheme_Category", "fund_category"],
        "sub_category": ["sub_category", "Sub_Category", "scheme_sub_category", "sub_cat", "Subcategory"],
        "risk_grade": ["risk_grade", "Risk_Grade", "risk", "Risk", "risk_level", "Risk_Level", "riskometer"],
        "scheme_code": ["scheme_code", "Scheme_Code", "amfi_code", "AMFI_Code", "code", "Code", "SchemeCode"],
    }

    for label, possible_names in column_mapping.items():
        matched_col = None
        for name in possible_names:
            if name in df.columns:
                matched_col = name
                break

        if matched_col:
            unique_vals = df[matched_col].nunique()
            print(f"\n   [INFO] Unique {label} ({matched_col}): {unique_vals}")
            # Print all unique values if there aren't too many
            if unique_vals <= 30:
                for val in sorted(df[matched_col].dropna().unique()):
                    count = (df[matched_col] == val).sum()
                    print(f"      - {val} ({count} schemes)")
            else:
                # Print top 15
                print(f"      (Showing top 15 of {unique_vals}):")
                top_vals = df[matched_col].value_counts().head(15)
                for val, count in top_vals.items():
                    print(f"      - {val} ({count} schemes)")

    # AMFI Code structure explanation
    scheme_col = None
    for name in column_mapping["scheme_code"]:
        if name in df.columns:
            scheme_col = name
            break

    if scheme_col:
        print(f"\n   [KEY] AMFI Scheme Code Structure ({scheme_col}):")
        codes = df[scheme_col].dropna()
        print(f"      - Total codes: {len(codes)}")
        print(f"      - Unique codes: {codes.nunique()}")
        print(f"      - Sample codes: {list(codes.head(5))}")
        if codes.dtype in ['int64', 'float64']:
            print(f"      - Range: {codes.min():.0f} to {codes.max():.0f}")
        # Check for duplicates in scheme codes
        dup_codes = codes[codes.duplicated()].nunique()
        if dup_codes > 0:
            print(f"      [WARN] {dup_codes} duplicate scheme codes found!")
        else:
            print(f"      [OK] All scheme codes are unique")


def validate_amfi_codes(all_dataframes):
    """
    Validate that every AMFI code in fund_master exists in nav_history.

    Think of it like checking: "Is every phone number in our contact list
    actually a valid, working phone number?"

    Parameters:
        all_dataframes (dict): Dictionary of {filename: DataFrame}
    """
    print(f"\n{'=' * 70}")
    print(f"[VALIDATE] AMFI CODE VALIDATION")
    print(f"{'=' * 70}")

    # Find fund_master and nav data
    fund_master_df = None
    nav_dfs = []
    fund_master_code_col = None
    nav_code_col = None

    # Identify fund_master
    for filename, df in all_dataframes.items():
        if "fund_master" in filename.lower():
            fund_master_df = df
            # Find the scheme code column
            for col in ["scheme_code", "Scheme_Code", "amfi_code", "AMFI_Code", "code", "Code", "SchemeCode"]:
                if col in df.columns:
                    fund_master_code_col = col
                    break

    # Identify nav data files
    for filename, df in all_dataframes.items():
        if "nav" in filename.lower() and "fund_master" not in filename.lower():
            nav_dfs.append((filename, df))
            if nav_code_col is None:
                for col in ["scheme_code", "Scheme_Code", "amfi_code", "AMFI_Code", "code", "Code", "SchemeCode"]:
                    if col in df.columns:
                        nav_code_col = col
                        break

    if fund_master_df is None:
        print("   [WARN] No fund_master file found. Skipping AMFI code validation.")
        print("   [INFO] If you have a fund_master CSV, place it in data/raw/ and re-run.")
        return

    if not nav_dfs:
        print("   [WARN] No NAV data files found. Skipping AMFI code validation.")
        return

    if fund_master_code_col is None:
        print("   [WARN] Could not find scheme_code column in fund_master.")
        print(f"   [INFO] Available columns: {list(fund_master_df.columns)}")
        return

    # Get scheme codes from fund_master
    master_codes = set(fund_master_df[fund_master_code_col].dropna().unique())
    print(f"\n   [INFO] Fund Master: {len(master_codes)} unique scheme codes")

    # Get scheme codes from nav data
    all_nav_codes = set()
    for filename, df in nav_dfs:
        if nav_code_col and nav_code_col in df.columns:
            nav_codes = set(df[nav_code_col].dropna().unique())
            all_nav_codes.update(nav_codes)
            print(f"   [DATA] {filename}: {len(nav_codes)} unique scheme codes")

    if not all_nav_codes:
        print("   [WARN] No scheme codes found in NAV data files.")
        return

    # Cross-check
    # Codes in fund_master but NOT in nav data
    missing_from_nav = master_codes - all_nav_codes
    # Codes in nav data but NOT in fund_master
    extra_in_nav = all_nav_codes - master_codes
    # Codes in both
    matched = master_codes & all_nav_codes

    print(f"\n   [RESULTS] Cross-Validation Results:")
    print(f"      [OK]   Matched codes (in both):          {len(matched)}")
    print(f"      [WARN] In fund_master but NOT in NAV:    {len(missing_from_nav)}")
    print(f"      [WARN] In NAV but NOT in fund_master:    {len(extra_in_nav)}")

    match_pct = (len(matched) / len(master_codes) * 100) if master_codes else 0
    print(f"      [RATE] Match rate: {match_pct:.1f}%")

    if missing_from_nav and len(missing_from_nav) <= 10:
        print(f"\n      Missing from NAV: {sorted(missing_from_nav)}")
    if extra_in_nav and len(extra_in_nav) <= 10:
        print(f"      Extra in NAV: {sorted(extra_in_nav)}")

    return {
        "matched": len(matched),
        "missing_from_nav": len(missing_from_nav),
        "extra_in_nav": len(extra_in_nav),
        "match_rate": match_pct,
    }


def write_data_quality_report(all_dataframes, all_anomalies, validation_results):
    """
    Write a data quality summary report to the reports/ folder.

    This creates a human-readable text file summarizing:
    - What files were loaded
    - How big each file is
    - What problems (anomalies) were found
    - Whether AMFI codes match across datasets
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(REPORTS_DIR, "data_quality_report.txt")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("DATA QUALITY REPORT -- Blue Stock Internship Project\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        # Summary table
        f.write("DATASET SUMMARY\n")
        f.write("-" * 70 + "\n")
        f.write(f"{'File':<40} {'Rows':>10} {'Cols':>6} {'Issues':>8}\n")
        f.write("-" * 70 + "\n")

        for filename, df in all_dataframes.items():
            issues = len(all_anomalies.get(filename, []))
            f.write(f"{filename:<40} {len(df):>10,} {len(df.columns):>6} {issues:>8}\n")

        f.write("\n\n")

        # Anomalies detail
        f.write("ANOMALIES DETECTED\n")
        f.write("-" * 70 + "\n")
        for filename, anomalies in all_anomalies.items():
            if anomalies:
                f.write(f"\n{filename}:\n")
                for a in anomalies:
                    f.write(f"  [!] {a}\n")

        any_anomalies = any(anomalies for anomalies in all_anomalies.values())
        if not any_anomalies:
            f.write("  [OK] No anomalies detected in any dataset.\n")

        # AMFI validation
        if validation_results:
            f.write("\n\nAMFI CODE VALIDATION\n")
            f.write("-" * 70 + "\n")
            f.write(f"  Matched codes:            {validation_results['matched']}\n")
            f.write(f"  Missing from NAV data:    {validation_results['missing_from_nav']}\n")
            f.write(f"  Extra in NAV data:        {validation_results['extra_in_nav']}\n")
            f.write(f"  Match rate:               {validation_results['match_rate']:.1f}%\n")

        f.write("\n" + "=" * 70 + "\n")
        f.write("END OF REPORT\n")

    print(f"\n[REPORT] Data quality report saved: {report_path}")
    return report_path


def main():
    """Main function -- loads all CSVs, inspects them, validates, and reports."""

    print("=" * 70)
    print("DATA INGESTION -- Blue Stock Internship Project")
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Check if raw data directory exists
    if not os.path.exists(RAW_DATA_DIR):
        print(f"\n[ERROR] Directory not found: {RAW_DATA_DIR}")
        print("   Please run live_nav_fetch.py first, or place CSV files in data/raw/")
        return

    # Find all CSV files
    csv_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith(".csv")]

    if not csv_files:
        print(f"\n[ERROR] No CSV files found in {RAW_DATA_DIR}")
        print("   Please run live_nav_fetch.py first, or place CSV files in data/raw/")
        return

    print(f"\n[FOUND] {len(csv_files)} CSV file(s) in {RAW_DATA_DIR}:")
    for f in sorted(csv_files):
        size_kb = os.path.getsize(os.path.join(RAW_DATA_DIR, f)) / 1024
        print(f"   - {f} ({size_kb:.1f} KB)")

    # Load and inspect each CSV
    all_dataframes = {}
    all_anomalies = {}

    for csv_file in sorted(csv_files):
        filepath = os.path.join(RAW_DATA_DIR, csv_file)
        df, anomalies = load_and_inspect_csv(filepath)
        if df is not None:
            all_dataframes[csv_file] = df
            all_anomalies[csv_file] = anomalies

    # Explore fund_master if present
    for filename, df in all_dataframes.items():
        explore_fund_master(df, filename)

    # Explore the combined NAV file as fund master equivalent
    for filename, df in all_dataframes.items():
        if "combined" in filename.lower():
            explore_fund_master(df, filename)

    # Validate AMFI codes
    validation_results = validate_amfi_codes(all_dataframes)

    # Write data quality report
    write_data_quality_report(all_dataframes, all_anomalies, validation_results)

    # Final summary
    print(f"\n{'=' * 70}")
    print("FINAL SUMMARY")
    print(f"{'=' * 70}")
    print(f"   [FILES] Files loaded:    {len(all_dataframes)}")
    total_rows = sum(len(df) for df in all_dataframes.values())
    print(f"   [DATA]  Total rows:      {total_rows:,}")
    total_issues = sum(len(a) for a in all_anomalies.values())
    print(f"   [WARN]  Total issues:    {total_issues}")
    print(f"\n[DONE] Data ingestion complete!")


if __name__ == "__main__":
    main()
