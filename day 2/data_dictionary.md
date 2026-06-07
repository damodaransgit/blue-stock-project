# Blue Stock Project: Data Dictionary
> Your definitive guide to understanding what the data means.

## 1. `dim_fund` (Fund Master)
The central directory of all mutual funds.
*   **amfi_code** (Integer) - **[PRIMARY KEY]** The unique barcode ID assigned by AMFI.
*   **fund_house** (Text) - The company managing the money (e.g., SBI, HDFC).
*   **scheme_name** (Text) - The full legal name of the mutual fund.
*   **category** (Text) - Broad classification (Equity, Debt, Liquid).
*   **expense_ratio_pct** (Float) - The percentage fee the fund charges you per year.
*   **fund_manager** (Text) - The person in charge of picking the stocks/bonds.

## 2. `fact_nav` (NAV History)
The daily price tracking for the funds.
*   **amfi_code** (Integer) - **[FOREIGN KEY]** Links to `dim_fund`.
*   **date** (Date) - The exact date the price was recorded.
*   **nav** (Float) - Net Asset Value. The price of one single unit of the mutual fund on that date.

## 3. `fact_transactions` (Investor Transactions)
A record of people buying or selling the funds.
*   **investor_id** (Text) - An anonymous, unique ID for the customer.
*   **transaction_date** (Date) - When the purchase/sale happened.
*   **amfi_code** (Integer) - **[FOREIGN KEY]** Which fund they bought/sold.
*   **transaction_type** (Text) - Whether it was a `SIP` (monthly), `Lumpsum` (one-time big purchase), or `Redemption` (selling).
*   **amount_inr** (Float) - How much money was moved, in Indian Rupees.
*   **kyc_status** (Text) - Whether the investor's identity is `Verified` or `Pending`.

## 4. `fact_performance`
Yearly performance and risk statistics.
*   **return_1yr_pct** (Float) - The percentage the fund grew (or shrank) in the last 1 year.
*   **sharpe_ratio** (Float) - A measure of how much risk the manager took to get those returns. Higher is better!
*   **max_drawdown_pct** (Float) - The maximum percentage the fund dropped from its highest peak. Measures downside risk.
*   **aum_crore** (Float) - Assets Under Management. The total amount of money sitting inside this specific fund, in Crores.
