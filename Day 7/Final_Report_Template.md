# Mutual Fund Analytics - Final Project Report

## Executive Summary
This report summarizes the findings of the 7-day Bluestock Mutual Fund Analytics Capstone Project. The goal was to build an end-to-end data pipeline processing 10 public datasets from AMFI and compute advanced financial performance metrics for 40 Mutual Fund schemes.

## 1. System Architecture (ETL)
*   **Extract:** Data was ingested from raw AMFI CSV files and the `mfapi.in` REST API.
*   **Transform:** Data was cleaned using Python (`pandas`), handling missing values and anomalies in NAV history.
*   **Load:** The cleaned data was loaded into a structured `bluestock_mf.db` SQLite database using a 5-table Star Schema.
*   **Analyse:** Exploratory Data Analysis (EDA) and performance analytics were performed in Jupyter Notebooks.
*   **Visualise:** A dynamic dashboard was built using Streamlit to present the findings to stakeholders.

## 2. Key Exploratory Data Analysis (EDA) Findings
1.  **Bull Market Rally:** Our NAV trend analysis confirmed a massive, uninterrupted bull run throughout 2023 across all equity mutual funds.
2.  **AUM Dominance:** SBI Mutual Fund dominates the market, crossing ₹12.5L Cr in Assets Under Management by 2025.
3.  **Retail Sentiment Peak:** SIP inflows reached an all-time high of ₹31,002 Cr in December 2025, showing historically high retail investor confidence.
4.  **Sector Concentration:** The Financial Services and IT sectors remain the heaviest weighted sectors in most equity fund portfolios.

## 3. Fund Performance & Risk Analytics
Using mathematical modeling, we ranked the 40 mutual funds based on Risk-Adjusted Returns.
*   **CAGR:** We calculated the 1yr, 3yr, and 5yr Compound Annual Growth Rates.
*   **Sharpe Ratio:** We identified funds that generated the highest return per unit of risk taken.
*   **Value at Risk (VaR):** We calculated the 95% VaR to understand the worst-case scenario losses for investors during market corrections.

## 4. Recommendations
Based on our recommender algorithm (Day 6), investors should choose funds based on their risk appetite:
*   **High Risk:** Focus on Small Cap funds which exhibit higher volatility but have generated significant Alpha.
*   **Low Risk:** Focus on Liquid or Debt funds that have a high Sharpe Ratio and low VaR.

## 5. Limitations & Future Scope
*   **Limitations:** The dataset focuses on the top 40 schemes. The real market has over 1,900 schemes.
*   **Future Scope:** Implementing a Machine Learning model (Random Forest) to predict future NAV prices based on historical benchmark trends.
