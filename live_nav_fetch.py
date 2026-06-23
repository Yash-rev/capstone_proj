import os
import time
import requests
import pandas as pd

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 5 Key schemes provided + HDFC Top 100 Direct
TARGET_SCHEMES = {
    "hdfc_top_100_direct": 125497,
    "sbi_bluechip": 119551,
    "icici_bluechip": 120503,
    "nippon_large_cap": 118632,
    "axis_bluechip": 119092,
    "kotak_bluechip": 120841
}

def fetch_and_save_nav(scheme_name, scheme_code):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"live data for {scheme_name} (Code: {scheme_code})")
    
    try:
        response = requests.get(url, timeout=15)
        
        
        if response.status_code == 200:
            json_data = response.json()
            
           
            nav_list = json_data.get("data", [])
            
            if not nav_list:
                print(f"No data returned for code {scheme_code}")
                return
                
          
            df = pd.DataFrame(nav_list)
            
            
            df["scheme_code"] = scheme_code
            df["scheme_name"] = json_data.get("meta", {}).get("scheme_name", scheme_name)
            
          
            df = df[["scheme_code", "scheme_name", "date", "nav"]]
          
            file_name = f"{scheme_name}_raw.csv"
            save_path = os.path.join(OUTPUT_DIR, file_name)
            
          
            df.to_csv(save_path, index=False)
            print(f"saved {len(df)} records to {save_path}")
            
        else:
            print(f"failed for {scheme_name} with status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {str(e)}")

def main():
    for name, code in TARGET_SCHEMES.items():
        fetch_and_save_nav(name, code)
        time.sleep(1)

if __name__ == "__main__":
    main()