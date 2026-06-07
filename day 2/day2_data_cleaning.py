"""
Day 2: Data Cleaning and Database Loading
=========================================
This script reads the raw data, cleans it step-by-step, saves it to the
processed folder, and then loads it into an SQLite database.
"""

import pandas as pd
import numpy as np
import os
import sqlite3
from sqlalchemy import create_engine

# ---------------------------------------------------------
# DIRECTORY SETUP
# ---------------------------------------------------------
# We define where our raw data comes from and where the clean data goes.
RAW_DIR = "../day 1/data/raw"
PROCESSED_DIR = "data/processed"
DB_PATH = "sqlite:///bluestock_mf.db"

# Create the processed folder if it doesn't exist yet
os.makedirs(PROCESSED_DIR, exist_ok=True)


def clean_nav_history():
    """
    Cleans the historical NAV (Net Asset Value) prices.
    Why: Financial data often misses weekends/holidays, and dates can be messy.
    """
    print("\n--- Cleaning NAV History ---")
    
    # 1. Load the raw data
    # How: pd.read_csv reads the CSV file into a Pandas DataFrame (a data table)
    file_path = os.path.join(RAW_DIR, "02_nav_history.csv")
    df = pd.read_csv(file_path)
    
    # 2. Parse dates to datetime
    # Why: We need Python to understand these are actual dates, not just text strings.
    # How: pd.to_datetime automatically converts text to date objects.
    df['date'] = pd.to_datetime(df['date'])
    
    # 3. Sort by AMFI code and Date
    # Why: Forward-filling (carrying Friday's price to the weekend) only works if dates are in order!
    df = df.sort_values(by=['amfi_code', 'date'])
    
    # 4. Remove Duplicates
    # Why: If the API accidentally downloaded the same day twice, it will mess up our math later.
    df = df.drop_duplicates(subset=['amfi_code', 'date'])
    
    # 5. Forward-fill missing NAV for holidays/weekends
    # How: Group by each fund (amfi_code), then reindex to a complete daily calendar, and use ffill()
    # Note: Since the prompt says "forward-fill missing NAV for holidays/weekends",
    # we first create a full date range for each fund, then fill missing days.
    
    # Let's create a function to fill dates for a single group
    def fill_dates(group):
        # Set date as index to allow resampling
        group = group.set_index('date')
        # Create a full daily calendar from the start to the end date of this specific fund
        full_date_range = pd.date_range(start=group.index.min(), end=group.index.max(), freq='D')
        # Reindex adds the missing weekend dates, and ffill() copies Friday's NAV into Sat/Sun
        group = group.reindex(full_date_range).ffill()
        # Bring date back as a normal column
        group.index.name = 'date'
        return group.reset_index()

    # Apply the filling function to every single mutual fund independently
    df = df.groupby('amfi_code').apply(fill_dates).reset_index(drop=True)
    
    # 6. Validate NAV > 0
    # Why: A mutual fund cannot have a price of 0 or a negative price. That's a data error.
    # How: Keep only rows where NAV is strictly greater than 0
    df = df[df['nav'] > 0]
    
    # Save the cleaned file
    output_path = os.path.join(PROCESSED_DIR, "cleaned_nav_history.csv")
    df.to_csv(output_path, index=False)
    print(f"Cleaned NAV History saved. Rows: {len(df)}")
    return df


def clean_investor_transactions():
    """
    Cleans the records of people buying and selling mutual funds.
    """
    print("\n--- Cleaning Investor Transactions ---")
    
    file_path = os.path.join(RAW_DIR, "08_investor_transactions.csv")
    df = pd.read_csv(file_path)
    
    # 1. Standardise transaction_type values
    # Why: People might type "S.I.P", "sip", or "SIP". We need one uniform label.
    # How: Convert to title case (e.g. Sip -> SIP, Lumpsum -> Lumpsum, Redemption -> Redemption)
    df['transaction_type'] = df['transaction_type'].str.strip().str.title()
    # Replace 'Sip' with 'SIP' to make it fully capitalized
    df['transaction_type'] = df['transaction_type'].replace('Sip', 'SIP')
    
    # 2. Validate amount > 0
    # Why: You cannot invest negative money.
    df = df[df['amount_inr'] > 0]
    
    # 3. Fix date formats
    # How: Convert to datetime, catching any weird formats
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    # Drop rows where the date was completely broken (became NaT)
    df = df.dropna(subset=['transaction_date'])
    
    # 4. Check KYC status enum values
    # Why: KYC can only be 'Verified', 'Pending', or 'Rejected'. Anything else is a typo.
    valid_kyc = ['Verified', 'Pending', 'Rejected']
    df = df[df['kyc_status'].isin(valid_kyc)]
    
    output_path = os.path.join(PROCESSED_DIR, "cleaned_investor_transactions.csv")
    df.to_csv(output_path, index=False)
    print(f"Cleaned Transactions saved. Rows: {len(df)}")
    return df


def clean_scheme_performance():
    """
    Cleans the yearly performance and fees of the mutual funds.
    """
    print("\n--- Cleaning Scheme Performance ---")
    
    file_path = os.path.join(RAW_DIR, "07_scheme_performance.csv")
    df = pd.read_csv(file_path)
    
    # 1. Validate all return values are numeric
    # Why: "12%" as text can't be used in math. We need numbers like 12.0.
    # How: pd.to_numeric forces columns to be numbers. Anything that fails becomes NaN.
    return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
    for col in return_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # 2. Flag anomalies (Extremely high or low returns)
    # How: Create a new column 'is_anomaly' if 1-year return is crazy (e.g. > 100% or < -50%)
    df['is_anomaly'] = ((df['return_1yr_pct'] > 100) | (df['return_1yr_pct'] < -50))
    
    # 3. Check expense_ratio range (0.1% – 2.5%)
    # Why: Mutual funds in India legally cannot charge extreme fees.
    # How: Keep only rows where expense ratio is within limits.
    df = df[(df['expense_ratio_pct'] >= 0.1) & (df['expense_ratio_pct'] <= 2.5)]
    
    output_path = os.path.join(PROCESSED_DIR, "cleaned_scheme_performance.csv")
    df.to_csv(output_path, index=False)
    print(f"Cleaned Performance saved. Rows: {len(df)}")
    return df

def process_remaining_files():
    """
    Loads all other raw files, does basic cleaning (dropping empty rows),
    and saves them to processed so we have exactly 10 cleaned CSVs.
    """
    print("\n--- Cleaning Remaining Files ---")
    raw_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv') and f.startswith(('01','03','04','05','06','09','10'))]
    processed_dfs = {}
    
    for file in raw_files:
        df = pd.read_csv(os.path.join(RAW_DIR, file))
        # Basic clean: drop completely empty rows
        df = df.dropna(how='all')
        
        out_name = f"cleaned_{file[3:]}" # remove the "01_" prefix
        df.to_csv(os.path.join(PROCESSED_DIR, out_name), index=False)
        processed_dfs[out_name] = df
        print(f"Processed {out_name} - Rows: {len(df)}")
        
    return processed_dfs

def create_dim_date(nav_df):
    """
    Creates a Date Dimension table (dim_date).
    Why: A Star Schema requires a central calendar table to easily group things
    by Year, Month, Quarter, or Day of Week.
    """
    print("\n--- Creating dim_date ---")
    min_date = nav_df['date'].min()
    max_date = nav_df['date'].max()
    
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    dim_date = pd.DataFrame({'date': date_range})
    dim_date['date_key'] = dim_date['date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['year'] = dim_date['date'].dt.year
    dim_date['month'] = dim_date['date'].dt.month
    dim_date['day'] = dim_date['date'].dt.day
    dim_date['quarter'] = dim_date['date'].dt.quarter
    dim_date['day_of_week'] = dim_date['date'].dt.day_name()
    dim_date['is_weekend'] = dim_date['date'].dt.dayofweek >= 5
    
    # Save it
    dim_date.to_csv(os.path.join(PROCESSED_DIR, "dim_date.csv"), index=False)
    print(f"Created dim_date. Rows: {len(dim_date)}")
    return dim_date


def load_into_sqlite(dfs_dict):
    """
    Loads all cleaned Pandas DataFrames into our SQLite Database.
    How: SQLAlchemy create_engine creates a connection, and df.to_sql writes the data.
    """
    print("\n--- Loading into SQLite Database ---")
    
    # 1. Create connection to database
    engine = create_engine(DB_PATH)
    
    # 2. Loop through our dictionary of cleaned dataframes and save them
    for table_name, df in dfs_dict.items():
        # Clean up table name (e.g. cleaned_fund_master -> dim_fund)
        sql_table_name = table_name.replace("cleaned_", "").replace(".csv", "")
        
        # Rename standard tables to match Star Schema naming
        if sql_table_name == "fund_master": sql_table_name = "dim_fund"
        elif sql_table_name == "nav_history": sql_table_name = "fact_nav"
        elif sql_table_name == "investor_transactions": sql_table_name = "fact_transactions"
        elif sql_table_name == "scheme_performance": sql_table_name = "fact_performance"
        elif sql_table_name == "aum_by_fund_house": sql_table_name = "fact_aum"
        
        # Write to SQLite. if_exists='replace' overwrites it if we run the script twice.
        df.to_sql(sql_table_name, con=engine, if_exists='replace', index=False)
        
        # Verification check
        # How: We ask SQLite to count the rows, and we check if it matches our Pandas rows.
        from sqlalchemy import text
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {sql_table_name}")).scalar()
            print(f"Table '{sql_table_name}' loaded. DB Rows: {result} | Pandas Rows: {len(df)}")
            if result == len(df):
                print(f"  [OK] Row counts match perfectly.")
            else:
                print(f"  [ERROR] Row counts mismatch!")


def main():
    print("Starting Day 2 Data Cleaning & DB Load...")
    
    # Run all cleaning functions
    df_nav = clean_nav_history()
    df_trans = clean_investor_transactions()
    df_perf = clean_scheme_performance()
    
    df_dim_date = create_dim_date(df_nav)
    
    remaining_dfs = process_remaining_files()
    
    # Bundle everything into a dictionary to load into the database easily
    all_clean_data = {
        "fact_nav": df_nav,
        "fact_transactions": df_trans,
        "fact_performance": df_perf,
        "dim_date": df_dim_date
    }
    
    # Add the remaining ones
    for name, df in remaining_dfs.items():
        all_clean_data[name] = df
        
    # Finally, load them all into SQLite
    load_into_sqlite(all_clean_data)
    
    print("\nSuccess! All Day 2 tasks completed.")


if __name__ == "__main__":
    main()
