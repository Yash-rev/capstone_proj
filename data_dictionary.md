# Bluestock Mutual Fund Project - Data Dictionary

## 1. Dimension Tables


### Table: `dim_fund`
Stores the descriptive catalog of all mutual fund schemes available in the ecosystem.

| Column Name | Data Type | Key | Business Definition |
| :--- | :--- | :--- | :--- |
| `amfi_code` | INTEGER | Primary Key | Unique 6-digit identification code assigned by AMFI. |
| `scheme_name` | TEXT | None | Full registered legal name of the mutual fund scheme. |
| `fund_house` | TEXT | None | The Asset Management Company (AMC) managing the fund (e.g., SBI Mutual Fund). |
| `category` | TEXT | None | Broad asset class (e.g., Equity, Debt, Hybrid). |
| `sub_category` | TEXT | None | Specific investment strategy grouping (e.g., Large Cap, Small Cap, Gilt). |
| `risk_grade` | TEXT | None | Volatility classification metric (e.g., Low, Moderate, High, Very High). |

### Table: `dim_date`
A standard calendar dimension table used for time-series aggregation and holiday filtering.

| Column Name | Data Type | Key | Business Definition |
| :--- | :--- | :--- | :--- |
| `date_id` | TEXT | Primary Key | Formatted date string in `YYYY-MM-DD` standard layout. |
| `calendar_year` | INTEGER | None | The 4-digit calendar year (e.g., 2024). |
| `calendar_month` | INTEGER | None | The numeric month of the year (1-12). |
| `month_name` | TEXT | None | The full text name of the month (e.g., January). |
| `day_of_week` | TEXT | None | The full text name of the day (e.g., Monday). |
| `is_weekend` | INTEGER | None | Boolean flag (`1` for Saturday/Sunday, `0` for Weekdays). |

---

## 2. Fact Tables


### Table: `fact_nav`
Stores the daily historical Net Asset Value (NAV) pricing data for the mutual funds.

| Column Name | Data Type | Key | Business Definition |
| :--- | :--- | :--- | :--- |
| `nav_id` | INTEGER | Primary Key | Auto-incrementing internal surrogate key. |
| `amfi_code` | INTEGER | Foreign Key | Links to `dim_fund.amfi_code`. |
| `date` | TEXT | Foreign Key | The trading date, linking to `dim_date.date_id`. |
| `nav` | REAL | None | The closing Net Asset Value per unit for the specified date. |

### Table: `fact_transactions`
Logs all individual investor activity, including investments and withdrawals.

| Column Name | Data Type | Key | Business Definition |
| :--- | :--- | :--- | :--- |
| `transaction_id` | TEXT | Primary Key | Unique alphanumeric identifier for the individual transaction. |
| `amfi_code` | INTEGER | Foreign Key | Links to `dim_fund.amfi_code`. |
| `investor_id` | TEXT | None | Unique alphanumeric identifier for the retail investor. |
| `transaction_type` | TEXT | None | Standardized category of the action (`SIP`, `LUMPSUM`, `REDEMPTION`). |
| `amount_inr` | REAL | None | The gross monetary value of the transaction in Indian Rupees. |
| `transaction_date` | TEXT | Foreign Key | Date the transaction was executed, linking to `dim_date.date_id`. |
| `state` | TEXT | None | Primary geographic state of the investor. |
| `city` | TEXT | None | Primary geographic city of the investor. |
| `city_tier` | TEXT | None | Classification of the city (e.g., T30 for Top 30, B30 for Beyond 30). |
| `age_group` | TEXT | None | Categorical age bracket of the investor. |
| `gender` | TEXT | None | Declared gender of the investor. |
| `annual_income_lakh` | REAL | None | Investor's self-reported annual income in Lakhs (INR). |
| `payment_mode` | TEXT | None | Method of transaction funding (e.g., UPI, Net Banking, Mandate). |
| `kyc_status` | TEXT | None | Compliance verification state (`VERIFIED`, `PENDING`, `FAILED`). |

### Table: `fact_performance`
Stores trailing return percentages and operational expense ratios for the funds.

| Column Name | Data Type | Key | Business Definition |
| :--- | :--- | :--- | :--- |
| `performance_id` | INTEGER | Primary Key | Auto-incrementing internal surrogate key. |
| `amfi_code` | INTEGER | Foreign Key | Links to `dim_fund.amfi_code`. |
| `returns_1y` | REAL | None | Trailing 1-year compounded annualized growth rate percentage. |
| `returns_3y` | REAL | None | Trailing 3-year compounded annualized growth rate percentage. |
| `returns_5y` | REAL | None | Trailing 5-year compounded annualized growth rate percentage. |
| `expense_ratio` | REAL | None | Annual operational management fee charged by the AMC (capped 0.1 - 2.5). |