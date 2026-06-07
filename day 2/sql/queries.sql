-- Day 2: 10 Analytical SQL Queries
-- ==================================
-- These queries showcase the power of the database we just built.

-- 1. Top 5 funds by AUM (Assets Under Management)
SELECT scheme_name, fund_house, aum_crore 
FROM fact_performance 
ORDER BY aum_crore DESC 
LIMIT 5;

-- 2. Average NAV per month for a specific fund (e.g., AMFI 119551)
-- Notice how we join the fact table with our dim_date table!
SELECT d.year, d.month, f.amfi_code, AVG(f.nav) as avg_nav
FROM fact_nav f
JOIN dim_date d ON DATE(f.date) = DATE(d.date)
WHERE f.amfi_code = 119551
GROUP BY d.year, d.month
ORDER BY d.year DESC, d.month DESC
LIMIT 12;

-- 3. Total Transaction Amount by State
SELECT state, SUM(amount_inr) as total_invested
FROM fact_transactions
WHERE transaction_type IN ('SIP', 'Lumpsum')
GROUP BY state
ORDER BY total_invested DESC;

-- 4. Funds with an Expense Ratio < 1% (Cheap funds!)
SELECT scheme_name, expense_ratio_pct, category 
FROM dim_fund 
WHERE expense_ratio_pct < 1.0 
ORDER BY expense_ratio_pct ASC;

-- 5. SIP vs Lumpsum investment totals
SELECT transaction_type, COUNT(*) as transaction_count, SUM(amount_inr) as total_volume
FROM fact_transactions
GROUP BY transaction_type;

-- 6. Male vs Female SIP distribution (Who invests more via SIP?)
SELECT gender, SUM(amount_inr) as total_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY gender;

-- 7. Highest Sharpe Ratio Funds (Best risk-adjusted returns)
SELECT scheme_name, category, sharpe_ratio 
FROM fact_performance
WHERE sharpe_ratio IS NOT NULL
ORDER BY sharpe_ratio DESC
LIMIT 10;

-- 8. Most preferred payment mode
SELECT payment_mode, COUNT(*) as frequency
FROM fact_transactions
GROUP BY payment_mode
ORDER BY frequency DESC;

-- 9. Number of active mutual funds managed by each fund house
SELECT fund_house, COUNT(amfi_code) as number_of_funds
FROM dim_fund
GROUP BY fund_house
ORDER BY number_of_funds DESC;

-- 10. Total redemptions (money pulled out) by age group
SELECT age_group, SUM(amount_inr) as total_redemptions
FROM fact_transactions
WHERE transaction_type = 'Redemption'
GROUP BY age_group
ORDER BY total_redemptions DESC;
