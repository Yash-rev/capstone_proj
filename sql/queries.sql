-- Query 1: Top 5 Funds by AUM
SELECT amfi_code, SUM(amount_inr) AS total_aum 
FROM fact_transactions 
WHERE transaction_type IN ('SIP', 'LUMPSUM')
GROUP BY amfi_code 
ORDER BY total_aum DESC 
LIMIT 5;

-- Query 2: Rolling Average NAV Per Month 
SELECT amfi_code, strftime('%Y-%m', date) AS transaction_month, AVG(nav) AS avg_nav
FROM fact_nav
GROUP BY amfi_code, transaction_month;

-- Query 3:  Expense Ratio < 1%
SELECT f.amfi_code, f.scheme_name, p.expense_ratio 
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.expense_ratio < 1.0;

-- Query 4: Transaction by state
SELECT state, COUNT(*) AS volume_count, SUM(amount_inr) AS gross_state_capital
FROM fact_transactions
GROUP BY state
ORDER BY gross_state_capital DESC;

-- Query 5: SIP YoY Growth
SELECT strftime('%Y', transaction_date) AS tracking_year, COUNT(*) AS active_sip_count, SUM(amount_inr) AS annual_sip_capital
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY tracking_year;

-- Query 6: Identification of Funds holding High Risk Categories
SELECT amfi_code, scheme_name, risk_grade 
FROM dim_fund 
WHERE risk_grade IN ('High', 'Very High');

-- Query 7: Total Liquid Capital Outflow via Redemption Events
SELECT amfi_code, SUM(amount_inr) AS total_withdrawn_capital
FROM fact_transactions
WHERE transaction_type = 'REDEMPTION'
GROUP BY amfi_code;

-- Query 8: Monthly Aggregate Analysis of All Transaction Capital
SELECT strftime('%Y-%m', transaction_date) AS month_idx, SUM(amount_inr) AS monthly_turnover
FROM fact_transactions
GROUP BY month_idx;

-- Query 9: Funds with the Best 3-Year Return Horizons
SELECT f.scheme_name, p.returns_3y
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.returns_3y DESC
LIMIT 5;

-- Query 10: Ratio of Capital Inflow (SIP + Lumpsum) vs Outflow (Redemption)
SELECT 
    SUM(CASE WHEN transaction_type IN ('SIP', 'LUMPSUM') THEN amount_inr ELSE 0 END) AS gross_inflow,
    SUM(CASE WHEN transaction_type = 'REDEMPTION' THEN amount_inr ELSE 0 END) AS gross_outflow
FROM fact_transactions;