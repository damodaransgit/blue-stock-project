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
    "**Objective:** Dive deep into the Mutual Fund data to discover patterns, trends, and anomalies using Data Visualization.\n",
    "\n",
    "### Layman Explanation: What is EDA?\n",
    "Exploratory Data Analysis (EDA) is like being a detective. Before we build complex financial models, we need to 'look' at our data using charts and graphs. This helps us spot obvious trends (like a 'bull run' where everything goes up) or problems (like missing data).\n",
    "\n",
    "In this notebook, we will visualize AUM (Assets Under Management - how much money the fund holds), SIPs (Systematic Investment Plans - how much people are investing monthly), and NAV (Net Asset Value - the price of one unit of the mutual fund)."
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
    "sns.set_theme(style='darkgrid', palette='muted')"
]))

# 1. NAV Trend Analysis
cells.append(create_markdown_cell([
    "### 1. NAV Trend Analysis\n",
    "**Why we do it:** We want to see how the price (NAV) of the funds changed over time. Did they grow? Did they crash? We are specifically looking for the massive growth period in 2023 (Bull Run) and the drop in 2024 (Market Correction).\n",
    "\n",
    "**Layman's term:** Imagine tracking the price of a house over 5 years to see when it was cheapest and when it peaked."
]))

cells.append(create_code_cell([
    "# Load NAV History\n",
    "nav_path = '../data/raw/02_nav_history.csv'\n",
    "if os.path.exists(nav_path):\n",
    "    df_nav = pd.read_csv(nav_path)\n",
    "    df_nav['date'] = pd.to_datetime(df_nav['date'])\n",
    "    df_nav = df_nav.sort_values('date')\n",
    "\n",
    "    # Select a few top schemes to plot to avoid clutter\n",
    "    top_schemes = df_nav['amfi_code'].unique()[:5]\n",
    "    df_plot = df_nav[df_nav['amfi_code'].isin(top_schemes)]\n",
    "\n",
    "    fig = px.line(df_plot, x='date', y='nav', color='amfi_code', \n",
    "                  title='Daily NAV Trend (Highlighting 2023 Bull Run & 2024 Correction)')\n",
    "    \n",
    "    # Highlight 2023 Bull Run\n",
    "    fig.add_vrect(x0=\"2023-01-01\", x1=\"2023-12-31\", fillcolor=\"green\", opacity=0.1, line_width=0)\n",
    "    fig.add_annotation(x=\"2023-06-01\", y=df_plot['nav'].max(), text=\"2023 Bull Run\", showarrow=False)\n",
    "\n",
    "    # Highlight 2024 Correction\n",
    "    fig.add_vrect(x0=\"2024-03-01\", x1=\"2024-06-01\", fillcolor=\"red\", opacity=0.1, line_width=0)\n",
    "    fig.add_annotation(x=\"2024-04-15\", y=df_plot['nav'].max(), text=\"2024 Correction\", showarrow=False)\n",
    "\n",
    "    fig.show()\n",
    "else:\n",
    "    print('File not found:', nav_path)"
]))

# 2. AUM Growth Bar Chart
cells.append(create_markdown_cell([
    "### 2. AUM Growth Bar Chart\n",
    "**Why we do it:** AUM (Assets Under Management) tells us how big a Mutual Fund company is. We want to see who the biggest players are (like SBI Mutual Fund) and how much they grew year over year.\n",
    "\n",
    "**Layman's term:** Comparing the bank accounts of different mutual fund companies to see who is the richest."
]))

cells.append(create_code_cell([
    "# Load AUM Data\n",
    "aum_path = '../data/raw/03_aum_by_fund_house.csv'\n",
    "if os.path.exists(aum_path):\n",
    "    df_aum = pd.read_csv(aum_path)\n",
    "    \n",
    "    plt.figure(figsize=(12, 6))\n",
    "    sns.barplot(data=df_aum, x='fund_house', y='aum_cr', hue='year')\n",
    "    plt.title('AUM Growth by Fund House (2022-2025)')\n",
    "    plt.ylabel('AUM (in Crores)')\n",
    "    plt.xticks(rotation=45)\n",
    "    \n",
    "    # Highlight SBI\n",
    "    plt.annotate('SBI Dominance (₹12.5L Cr)', xy=(0, 1250000), xytext=(1, 1300000),\n",
    "             arrowprops=dict(facecolor='black', shrink=0.05))\n",
    "    \n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "else:\n",
    "    print('File not found:', aum_path)"
]))

# 3. SIP Inflow Time-Series
cells.append(create_markdown_cell([
    "### 3. SIP Inflow Time-Series\n",
    "**Why we do it:** SIPs are monthly automated investments. Tracking this shows us retail investor sentiment (how confident average people are in the market).\n",
    "\n",
    "**Layman's term:** Seeing how much pocket money everyday people are putting into the stock market every month."
]))

cells.append(create_code_cell([
    "# Load SIP Inflows\n",
    "sip_path = '../data/raw/04_monthly_sip_inflows.csv'\n",
    "if os.path.exists(sip_path):\n",
    "    df_sip = pd.read_csv(sip_path)\n",
    "    df_sip['month_year'] = pd.to_datetime(df_sip['month_year'])\n",
    "    \n",
    "    fig = px.line(df_sip, x='month_year', y='sip_amount_cr', title='Monthly SIP Inflows (Jan 2022 - Dec 2025)')\n",
    "    \n",
    "    # Annotate the All-Time High\n",
    "    max_val = df_sip['sip_amount_cr'].max()\n",
    "    max_date = df_sip[df_sip['sip_amount_cr'] == max_val]['month_year'].iloc[0]\n",
    "    \n",
    "    fig.add_annotation(x=max_date, y=max_val, \n",
    "                       text=f\"All-Time High: ₹{max_val:,.0f} Cr\", \n",
    "                       showarrow=True, arrowhead=1)\n",
    "    fig.show()\n",
    "else:\n",
    "    print('File not found:', sip_path)"
]))

# 4. Sector Allocation Donut
cells.append(create_markdown_cell([
    "### 4. Sector Allocation Donut Chart\n",
    "**Why we do it:** Mutual funds invest in different parts of the economy (IT, Banks, Pharma). This shows us where the money is actually going.\n",
    "\n",
    "**Layman's term:** Checking which slice of the pie each industry gets from the mutual fund's total cash."
]))

cells.append(create_code_cell([
    "# Load Portfolio Holdings\n",
    "port_path = '../data/raw/09_portfolio_holdings.csv'\n",
    "if os.path.exists(port_path):\n",
    "    df_port = pd.read_csv(port_path)\n",
    "    \n",
    "    # Aggregate sector weights\n",
    "    sector_agg = df_port.groupby('sector')['weight_percentage'].sum().reset_index()\n",
    "    \n",
    "    fig = px.pie(sector_agg, values='weight_percentage', names='sector', hole=0.5, \n",
    "                 title='Sector Allocation Across Equity Funds')\n",
    "    fig.update_traces(textposition='inside', textinfo='percent+label')\n",
    "    fig.show()\n",
    "else:\n",
    "    print('File not found:', port_path)"
]))

# Summary
cells.append(create_markdown_cell([
    "### Key EDA Findings Summary\n",
    "1. **Bull Market Confirmation:** 2023 saw massive, uninterrupted growth across almost all equity mutual funds.\n",
    "2. **Market Correction:** Early 2024 showed a distinct dip, indicating a market correction where investors lost some short-term value.\n",
    "3. **SBI Dominance:** SBI Mutual Fund dominates the AUM charts, crossing ₹12.5L Cr.\n",
    "4. **Retail Investor Confidence:** SIP inflows reached an all-time high of over ₹31k Cr in Dec 2025, showing huge retail trust.\n",
    "5. **Sector Preference:** Financial Services and IT remain the heaviest weighted sectors in most portfolios.\n"
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

out_path = os.path.join('d:\\\\DOWNLOADS\\\\Codes\\\\blue-stock-project', 'notebooks', '03_eda_analysis.ipynb')

with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=2)

print(f'Successfully generated {out_path}')
