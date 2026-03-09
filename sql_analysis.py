import sqlite3
import pandas as pd
import re

# 1. Load the RAW data
try:
    df = pd.read_csv('naukri_business_analyst_data.csv')
except FileNotFoundError:
    print("Error: Could not find 'naukri_business_analyst_data.csv'.")
    exit()

# 2. CLEANING LOGIC (Turning text into numbers for Power BI)
def get_min_exp(exp_str):
    nums = re.findall(r'\d+', str(exp_str))
    return int(nums[0]) if nums else 0

def get_days_ago(posted_str):
    s = str(posted_str).lower()
    if 'just now' in s or 'today' in s: return 0
    nums = re.findall(r'\d+', s)
    if 'week' in s: return int(nums[0]) * 7 if nums else 7
    return int(nums[0]) if nums else 1

df['Min_Experience'] = df['Experience'].apply(get_min_exp)
df['Days_Ago'] = df['Posted_Date'].apply(get_days_ago)

# 3. SAVE THE CLEANED CSV (Use this for Power BI)
df.to_csv('cleaned_naukri_data.csv', index=False)
print("Step 1: 'cleaned_naukri_data.csv' created successfully!")

# 4. Update the SQL Database
conn = sqlite3.connect('job_market.db')
df.to_sql('Jobs', conn, if_exists='replace', index=False)
conn.close()
print("Step 2: 'job_market.db' updated successfully!")