"""
live_nav_fetch.py -- Fetch Live Mutual Fund NAV Data
====================================================
This script connects to the mfapi.in API (a free, public API for Indian mutual
fund data) and downloads the NAV (Net Asset Value) history for 6 blue-chip
mutual fund schemes.

What is NAV?
    NAV = Net Asset Value = the "price" of one unit of a mutual fund.
    If a fund's NAV is Rs.50, you pay Rs.50 for one unit.

What is mfapi.in?
    It's a free API that serves AMFI (Association of Mutual Funds in India)
    data. Every mutual fund in India has a unique AMFI scheme code.

What this script does:
    1. Sends a request to mfapi.in for each fund's scheme code
    2. Gets back the fund's name + its NAV on every date since inception
    3. Saves each fund's data as a CSV file in data/raw/
    4. Also creates a combined CSV with all funds together
"""

import requests
import pandas as pd
import os
import time
from datetime import datetime


# ------------------------------------------------------------------------------
# CONFIGURATION -- The 6 mutual fund schemes we want to fetch
# ------------------------------------------------------------------------------
# Each entry: "Short Name": AMFI_Scheme_Code
# You can find scheme codes at: https://www.amfiindia.com/

SCHEMES = {
    "HDFC_Top_100":    125497,
    "SBI_Bluechip":    119551,
    "ICICI_Bluechip":  120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip":   119092,
    "Kotak_Bluechip":  120841,
}

# API base URL
API_BASE = "https://api.mfapi.in/mf"

# Where to save the CSV files
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUTPUT_DIR = os.path.join(ROOT_DIR, "data", "raw")


def fetch_nav_data(scheme_code, scheme_name):
    """
    Fetch NAV data for a single mutual fund scheme from mfapi.in.

    How the API works:
        - URL: https://api.mfapi.in/mf/{scheme_code}
        - Returns JSON with two parts:
            1. "meta" -- fund name, house, type, category
            2. "data" -- list of {"date": "DD-MM-YYYY", "nav": "123.45"}

    Parameters:
        scheme_code (int): The AMFI scheme code (e.g., 125497)
        scheme_name (str): A friendly name for the fund (e.g., "HDFC_Top_100")

    Returns:
        pandas DataFrame with columns: [date, nav, scheme_code, scheme_name, fund_house, category]
        Returns None if the fetch fails.
    """
    url = f"{API_BASE}/{scheme_code}"
    print(f"\n[FETCH] Fetching: {scheme_name} (Code: {scheme_code})")
    print(f"   URL: {url}")

    try:
        # Send GET request to the API
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # Raise error if status != 200

        # Parse the JSON response
        json_data = response.json()

        # Extract meta information (fund details)
        meta = json_data.get("meta", {})
        fund_house = meta.get("fund_house", "Unknown")
        scheme_type = meta.get("scheme_type", "Unknown")
        scheme_category = meta.get("scheme_category", "Unknown")
        scheme_full_name = meta.get("scheme_name", scheme_name)

        print(f"   [OK] Fund: {scheme_full_name}")
        print(f"   [INFO] Fund House: {fund_house}")
        print(f"   [INFO] Category: {scheme_category}")

        # Extract NAV data (list of date-nav pairs)
        nav_data = json_data.get("data", [])
        print(f"   [DATA] Data points: {len(nav_data)}")

        if not nav_data:
            print(f"   [WARN] No NAV data returned for {scheme_name}")
            return None

        # Convert to DataFrame
        df = pd.DataFrame(nav_data)

        # Clean up the data:
        # - Convert "nav" from string to number (some entries might be "N/A")
        # - Convert "date" from string to proper date format
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")  # "coerce" turns bad values into NaN
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")

        # Add extra columns for identification
        df["scheme_code"] = scheme_code
        df["scheme_name"] = scheme_name
        df["fund_house"] = fund_house
        df["category"] = scheme_category

        # Sort by date (oldest first)
        df = df.sort_values("date").reset_index(drop=True)

        # Show the latest NAV
        latest = df.dropna(subset=["nav"]).tail(1)
        if not latest.empty:
            print(f"   [NAV] Latest NAV: Rs.{latest['nav'].values[0]:.4f} on {latest['date'].values[0]}")

        return df

    except requests.exceptions.RequestException as e:
        print(f"   [ERROR] Error fetching {scheme_name}: {e}")
        return None


def save_individual_csv(df, scheme_name, output_dir):
    """
    Save a single fund's NAV data as its own CSV file.
    Example: data/raw/nav_HDFC_Top_100.csv
    """
    filepath = os.path.join(output_dir, f"nav_{scheme_name}.csv")
    df.to_csv(filepath, index=False)
    print(f"   [SAVED] {filepath} ({len(df)} rows)")
    return filepath


def main():
    """Main function -- orchestrates the entire fetch process."""

    print("=" * 70)
    print("LIVE NAV FETCHER -- Blue Stock Internship Project")
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Fetch data for all schemes
    all_dataframes = []
    successful = 0
    failed = 0

    for scheme_name, scheme_code in SCHEMES.items():
        df = fetch_nav_data(scheme_code, scheme_name)

        if df is not None:
            # Save individual CSV
            save_individual_csv(df, scheme_name, OUTPUT_DIR)
            all_dataframes.append(df)
            successful += 1
        else:
            failed += 1

        # Be polite to the API -- wait 1 second between requests
        time.sleep(1)

    # Combine all data into one big CSV
    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        combined_path = os.path.join(OUTPUT_DIR, "nav_all_schemes_combined.csv")
        combined_df.to_csv(combined_path, index=False)

        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"   [OK] Successful: {successful}/{len(SCHEMES)} schemes")
        print(f"   [FAIL] Failed:   {failed}/{len(SCHEMES)} schemes")
        print(f"   [DATA] Total rows: {len(combined_df)}")
        print(f"   [SAVED] Combined file: {combined_path}")
        print(f"   [DATE] Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")

        # Quick data quality check
        print("\n[DATA] Per-scheme breakdown:")
        for name in SCHEMES:
            scheme_df = combined_df[combined_df["scheme_name"] == name]
            if not scheme_df.empty:
                nav_nulls = scheme_df["nav"].isna().sum()
                print(f"   {name}: {len(scheme_df)} rows, {nav_nulls} missing NAVs")

    else:
        print("\n[ERROR] No data was fetched successfully. Check your internet connection.")

    print("\n[DONE] Live NAV fetch complete!")


if __name__ == "__main__":
    main()
