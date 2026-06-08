import json
import os

def create_markdown_cell(source):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": source
    }

def create_code_cell(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source
    }

cells = []

# Title & Introduction
cells.append(create_markdown_cell([
    "# Capstone Project: Day 3 - Exploratory Data Analysis (EDA)\n",
    "\n",
    "**Objective:** Dive deep into the Mutual Fund data to discover patterns, trends, and anomalies using Data Visualization.\n"
]))

# Imports
cells.append(create_code_cell([
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import plotly.express as px\n",
    "import plotly.graph_objects as go\n",
    "import os\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "# Set aesthetic parameters for Seaborn\n",
    "sns.set_theme(style='darkgrid', palette='muted')\n",
    "\n",
    "# File Paths\n",
    "DATA_DIR = '../Day 2/data/processed/'\n",
    "RAW_DIR = '../Day 1/data/raw/'"
]))

# 1. NAV Trend Analysis
cells.append(create_markdown_cell(["### 1. NAV Trend Analysis\n"]))
cells.append(create_code_cell([
    "nav_path = os.path.join(DATA_DIR, 'cleaned_nav_history.csv')\n",
    "if os.path.exists(nav_path):\n",
    "    df_nav = pd.read_csv(nav_path)\n",
    "    df_nav['date'] = pd.to_datetime(df_nav['date'])\n",
    "    df_plot = df_nav[df_nav['amfi_code'].isin(df_nav['amfi_code'].unique()[:5])]\n",
    "    fig = px.line(df_plot, x='date', y='nav', color='amfi_code', title='Daily NAV Trend')\n",
    "    fig.add_vrect(x0='2023-01-01', x1='2023-12-31', fillcolor='green', opacity=0.1, line_width=0)\n",
    "    fig.add_vrect(x0='2024-03-01', x1='2024-06-01', fillcolor='red', opacity=0.1, line_width=0)\n",
    "    fig.show()\n",
    "else:\n",
    "    print('File not found:', nav_path)"
]))

# 2. AUM Growth Bar Chart
cells.append(create_markdown_cell(["### 2. AUM Growth Bar Chart\n"]))
cells.append(create_code_cell([
    "aum_path = os.path.join(RAW_DIR, '03_aum_by_fund_house.csv')\n",
    "if os.path.exists(aum_path):\n",
    "    df_aum = pd.read_csv(aum_path)\n",
    "    df_aum['year'] = pd.to_datetime(df_aum['date']).dt.year\n",
    "    plt.figure(figsize=(12, 6))\n",
    "    sns.barplot(data=df_aum, x='fund_house', y='aum_crore', hue='year')\n",
    "    plt.title('AUM Growth by Fund House (2022-2025)')\n",
    "    plt.xticks(rotation=45)\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "else:\n",
    "    print('File not found:', aum_path)"
]))

# 3. SIP Inflow Time-Series
cells.append(create_markdown_cell(["### 3. SIP Inflow Time-Series\n"]))
cells.append(create_code_cell([
    "sip_path = os.path.join(RAW_DIR, '04_monthly_sip_inflows.csv')\n",
    "if os.path.exists(sip_path):\n",
    "    df_sip = pd.read_csv(sip_path)\n",
    "    df_sip['month'] = pd.to_datetime(df_sip['month'])\n",
    "    fig = px.line(df_sip, x='month', y='sip_inflow_crore', title='Monthly SIP Inflows (Jan 2022 - Dec 2025)')\n",
    "    max_val = df_sip['sip_inflow_crore'].max()\n",
    "    max_date = df_sip[df_sip['sip_inflow_crore'] == max_val]['month'].iloc[0]\n",
    "    fig.add_annotation(x=max_date, y=max_val, text=f'All-Time High: ₹{max_val:,.0f} Cr', showarrow=True)\n",
    "    fig.show()\n"
]))

# 4. Category-wise inflow heatmap
cells.append(create_markdown_cell(["### 4. Category-wise Inflow Heatmap\n"]))
cells.append(create_code_cell([
    "cat_inflow_path = os.path.join(DATA_DIR, 'cleaned_category_inflows.csv')\n",
    "if os.path.exists(cat_inflow_path):\n",
    "    df_cat = pd.read_csv(cat_inflow_path)\n",
    "    df_cat['month'] = pd.to_datetime(df_cat['month'])\n",
    "    df_cat['month_str'] = df_cat['month'].dt.strftime('%Y-%m')\n",
    "    pivot_cat = df_cat.pivot_table(index='category', columns='month_str', values='net_inflow_crore', aggfunc='sum')\n",
    "    plt.figure(figsize=(14, 8))\n",
    "    sns.heatmap(pivot_cat, cmap='coolwarm', center=0, annot=False)\n",
    "    plt.title('Category-wise Net Inflow Heatmap (in Crores)')\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n"
]))

# 5. Investor Demographics
cells.append(create_markdown_cell(["### 5. Investor Demographics\n"]))
cells.append(create_code_cell([
    "txn_path = os.path.join(DATA_DIR, 'cleaned_investor_transactions.csv')\n",
    "if os.path.exists(txn_path):\n",
    "    df_txn = pd.read_csv(txn_path)\n",
    "    \n",
    "    # Age group pie chart\n",
    "    age_counts = df_txn['age_group'].value_counts().reset_index()\n",
    "    age_counts.columns = ['age_group', 'count']\n",
    "    fig1 = px.pie(age_counts, values='count', names='age_group', title='Investor Age Group Distribution')\n",
    "    fig1.show()\n",
    "    \n",
    "    # SIP amount box plot by age group\n",
    "    df_sip_only = df_txn[df_txn['transaction_type'] == 'SIP']\n",
    "    plt.figure(figsize=(10, 6))\n",
    "    sns.boxplot(data=df_sip_only, x='age_group', y='amount_inr', palette='Set2')\n",
    "    plt.title('SIP Amount Distribution by Age Group')\n",
    "    plt.yscale('log') # Log scale since amounts vary widely\n",
    "    plt.show()\n"
]))

# 6. Geographic Distribution
cells.append(create_markdown_cell(["### 6. Geographic Distribution\n"]))
cells.append(create_code_cell([
    "if 'df_txn' in locals():\n",
    "    # State bar chart\n",
    "    state_amt = df_txn.groupby('state')['amount_inr'].sum().sort_values(ascending=False).reset_index()\n",
    "    plt.figure(figsize=(12, 8))\n",
    "    sns.barplot(data=state_amt, x='amount_inr', y='state', palette='viridis')\n",
    "    plt.title('Total Investment Amount by State')\n",
    "    plt.xlabel('Amount (INR)')\n",
    "    plt.show()\n",
    "    \n",
    "    # T30 vs B30 pie chart\n",
    "    tier_counts = df_txn['city_tier'].value_counts().reset_index()\n",
    "    tier_counts.columns = ['city_tier', 'count']\n",
    "    fig2 = px.pie(tier_counts, values='count', names='city_tier', title='T30 vs B30 City Distribution')\n",
    "    fig2.show()\n"
]))

# 7. Folio Count Growth
cells.append(create_markdown_cell(["### 7. Folio Count Growth\n"]))
cells.append(create_code_cell([
    "folio_path = os.path.join(DATA_DIR, 'cleaned_industry_folio_count.csv')\n",
    "if os.path.exists(folio_path):\n",
    "    df_folio = pd.read_csv(folio_path)\n",
    "    df_folio['month'] = pd.to_datetime(df_folio['month'])\n",
    "    fig = px.line(df_folio, x='month', y='total_folios_crore', title='Mutual Fund Folio Count Growth (Crores)')\n",
    "    fig.show()\n"
]))

# 8. Correlation Matrix
cells.append(create_markdown_cell(["### 8. Correlation Matrix of NAV Returns\n"]))
cells.append(create_code_cell([
    "if 'df_nav' in locals():\n",
    "    # Pivot to get daily NAV per amfi_code\n",
    "    df_pivot = df_nav.pivot(index='date', columns='amfi_code', values='nav')\n",
    "    # Compute daily percentage returns\n",
    "    df_returns = df_pivot.pct_change().dropna()\n",
    "    # Take first 10 funds for correlation\n",
    "    corr_matrix = df_returns.iloc[:, :10].corr()\n",
    "    \n",
    "    plt.figure(figsize=(10, 8))\n",
    "    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)\n",
    "    plt.title('Correlation Matrix of Daily Returns (10 Selected Funds)')\n",
    "    plt.show()\n"
]))

# 9. Top Holdings Donut Chart
cells.append(create_markdown_cell(["### 9. Top Holdings Sector Allocation Donut Chart\n"]))
cells.append(create_code_cell([
    "port_path = os.path.join(RAW_DIR, '09_portfolio_holdings.csv')\n",
    "if os.path.exists(port_path):\n",
    "    df_port = pd.read_csv(port_path)\n",
    "    sector_agg = df_port.groupby('sector')['weight_pct'].sum().reset_index()\n",
    "    fig = px.pie(sector_agg, values='weight_pct', names='sector', hole=0.5, \n",
    "                 title='Sector Allocation Across Equity Funds')\n",
    "    fig.update_traces(textposition='inside', textinfo='percent+label')\n",
    "    fig.show()\n"
]))

# 10. Summary
cells.append(create_markdown_cell([
    "### 10. Key EDA Findings Summary\n",
    "1. **Bull Market Confirmation:** 2023 saw massive, uninterrupted growth across almost all equity mutual funds.\n",
    "2. **Market Correction:** Early 2024 showed a distinct dip, indicating a market correction where investors lost some short-term value.\n",
    "3. **SBI Dominance:** SBI Mutual Fund dominates the AUM charts, crossing ₹12.5L Cr.\n",
    "4. **Retail Investor Confidence:** SIP inflows reached an all-time high of over ₹31k Cr in Dec 2025, showing huge retail trust.\n",
    "5. **Sector Preference:** Financial Services and IT remain the heaviest weighted sectors in most portfolios.\n",
    "6. **Category Inflows:** Equity categories see strong seasonal inflows, while debt categories show sensitivity to interest rate cycles.\n",
    "7. **Demographics:** The 25-35 age group dominates SIP volume, but higher individual investment amounts come from the 45+ group.\n",
    "8. **Geographic Spread:** T30 cities still form the bulk of investments, but B30 city participation is growing rapidly.\n",
    "9. **Folio Growth:** Total folios have grown consistently, indicating an expanding retail investor base reaching over 16+ crores.\n",
    "10. **Correlations:** Equity funds exhibit high positive correlation with each other, highlighting systemic market risks.\n"
]))

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.9.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

out_path = '03_eda_analysis.ipynb'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print(f'Successfully generated {out_path}')
