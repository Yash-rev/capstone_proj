import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine, text

DB_PATH = "bluestock_mf.db"
ENGINE_URL = f"sqlite:///{DB_PATH}"

def initialize_database():
    print("🔨 Building fresh database architecture maps...")
    with open("sql/schema.sql", "r") as f:
        sql_script = f.read()
        
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(sql_script)
    conn.close()
    print("✅ Schema architecture loaded successfully.")

def populate_date_dimension():
    """Generates dates to populate dim_date for foreign key validation."""
    engine = create_engine(ENGINE_URL)
    date_series = pd.date_range(start="2010-01-01", end="2027-12-31")
    dim_date_df = pd.DataFrame({
        "date_id": date_series.strftime('%Y-%m-%d'),
        "calendar_year": date_series.year,
        "calendar_month": date_series.month,
        "month_name": date_series.strftime('%B'),
        "day_of_week": date_series.strftime('%A'),
        "is_weekend": date_series.weekday.map(lambda x: 1 if x >= 5 else 0)
    })
    dim_date_df.to_sql("dim_date", con=engine, if_exists='replace', index=False)
    print("✅ Populated global Date Dimension table.")

def load_processed_csv_to_db(csv_path, table_name):
    engine = create_engine(ENGINE_URL)
    df = pd.read_csv(csv_path)
    
    # ---------------------------------------------------------
    # Schema Alignment: Filter and map columns before loading
    # ---------------------------------------------------------
    if table_name == "fact_performance":
        rename_map = {
            'return_1yr_pct': 'returns_1y',
            'return_3yr_pct': 'returns_3y',
            'return_5yr_pct': 'returns_5y',
            'expense_ratio_pct': 'expense_ratio'
        }
        df = df.rename(columns=rename_map)
        allowed_cols = ['amfi_code', 'returns_1y', 'returns_3y', 'returns_5y', 'expense_ratio']
        df = df[[col for col in allowed_cols if col in df.columns]]
        
    elif table_name == "dim_fund":
        # Rename risk column to match the schema
        if 'risk_category' in df.columns:
            df = df.rename(columns={'risk_category': 'risk_grade'})
            
        # Keep ONLY the columns defined in schema.sql for dim_fund
        allowed_cols = ['amfi_code', 'scheme_name', 'fund_house', 'category', 'sub_category', 'risk_grade']
        df = df[[col for col in allowed_cols if col in df.columns]]
            
    # Standard Date formatting logic for SQLite
    for col in df.columns:
        if 'date' in col.lower() and df[col].dtype == 'datetime64[ns]':
            df[col] = df[col].dt.strftime('%Y-%m-%d')
            
    # Load into the database
    df.to_sql(table_name, con=engine, if_exists='append', index=False)
    
    # Verification and row audit check
    with engine.connect() as conn:
        db_count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).fetchone()[0]
        
    print(f"📌 Table '{table_name:<18}': CSV Rows ({len(df):<6}) vs Database Rows ({db_count:<6})")
    assert len(df) == db_count, f"❌ Validation failure: Row counts don't match for {table_name}!"
def main():
    initialize_database()
    populate_date_dimension()
    
    # Processing pipeline execution map
    mappings = {
        "data/processed/fund_master_cleaned.csv": "dim_fund",
        "data/processed/nav_history_cleaned.csv": "fact_nav",
        "data/processed/investor_transactions_cleaned.csv": "fact_transactions",
        "data/processed/scheme_performance_cleaned.csv": "fact_performance"
    }
    
    for path, table in mappings.items():
        if os.path.exists(path):
            load_processed_csv_to_db(path, table)
        else:
            print(f"⚠️ Data skip notification: File {path} not found.")
            
    print("\n🎉 Database loading sequence complete!")

if __name__ == "__main__":
    main()