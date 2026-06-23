import os
import pandas as pd

def profile_datasets(data_dir="data/bluestock_mf_datasets"):
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]

    if not csv_files:
        print(f"No files founf in {data_dir}")
        return
    
    print(f"Found {len(csv_files)} datasests. \n")
    for file in csv_files:
        file_path = os.path.join(data_dir, file)

        print(f"\n Profiling file: {file}")

        try:
            df = pd.read_csv(file_path)
            
            print(f"Shape : {df.shape[0]} rows. {df.shape[1]} columns")
            
            print(f"\n First 3 rows:")
            print(df.head(3))

            print("\n Column profiles and Data Types:")
            info_df = pd.DataFrame({
                'Data Type': df.dtypes,
                'Null Count': df.isnull().sum().sum(),
                "Null %": (df.isnull().sum() / len(df)* 100).round(2)
            })

            print(info_df)

            print("\n Anamolies detected:")
            anamolies = []

            duplicates = df.duplicated().sum()
            if duplicates > 0:
                anamolies.append(f"Found {duplicates} duplicate rows.")

            all_null_col= df.columns[df.isnull().all()].tolist()

            if all_null_col:
                anamolies.append(f"Colums completely empty: {all_null_col}")
            
            date_col = [col for col in df.columns if 'date' in col.lower()]

            for dc in date_col:
                if df[dc].dtype == 'object':
                    anamolies.append(f"Column '{dc}' is an object. Needs conversion to date/time.")

            
            if not anamolies:
                print("No anamlies found.")

            else:
                for anamoly in anamolies:
                    print(anamoly)

        except Exception as e:
            print("Error readile {file}: {e}")


if __name__ == "__main__":
    profile_datasets()


def validate_amfi(master_path="data/bluestock_mf_datasets/01_fund_master.csv", history_path="data/bluestock_mf_datasets/02_nav_history.csv"):
    print("\n Data Integrity and Code Validation")

    try:
        master_df = pd.read_csv(master_path)
        history_df = pd.read_csv(history_path)

        print("\n -Fund Master Structural Summary- \n")

        for col in ['fund_house', 'category', 'sub_category', 'risk_grade']:
            if col in master_df.columns:
                print(f"Unique {col.replace('_', ' ').title()}s: {master_df[col].nunique()}")

            master_code_col = 'amfi_code' if 'amfi_code' in master_df.columns else ('scheme_code' if 'scheme_code' in master_df.columns else None)
            history_code_col = 'amfi_code' if 'amfi_code' in history_df.columns else ('scheme_code' if 'scheme_code'in history_df.columns else None)
        
        if not master_code_col or not history_code_col:
            print("Could not locate AMFI/Scheme code columns dynamically.\n")
            return
        print(f" - Code Integrity Check ({master_code_col} to {history_code_col}) -")
        master_codes = set(master_df[master_code_col].dropna().unique())
        history_codes = set(history_df[history_code_col].dropna().unique())

        missing_in_history = master_codes - history_codes

        print(
            f"Unique codes in master {len(master_codes)}\n"
            f"Uniques codes in history {len(history_codes)}"
        )

        print("\n -- Data Quality Summary -- \n")
        if len(missing_in_history) == 0:
            print("intefrity Passed. Every AMFI code in fund_master matches a record in nav_history. \n")

        else:
            print(f"{len(missing_in_history)} codes in fund_master have NO corresponding historical records.")
            print(f"Sample missing codes: {list(missing_in_history)[:5]} ")
    
    except FileNotFoundError as e:
        print(f"Missing Reference file. Details : {e}")

if __name__ == "__main__":
  
    profile_datasets()
    validate_amfi()