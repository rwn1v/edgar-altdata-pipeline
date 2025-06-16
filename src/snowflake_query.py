import snowflake.connector
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import os

# Load credentials
project_root = Path(__file__).resolve().parents[1]
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

# Load data
df = pd.read_csv("data/processed/risk_factors.csv", dtype=str).fillna("")

# Create table
columns = ', '.join(f'"{col}" STRING' for col in df.columns)
create_stmt = f'CREATE OR REPLACE TABLE risk_factors ({columns})'

cs = conn.cursor()
try:
    cs.execute(create_stmt)
    print("✅ Table created.")

    # Insert data using parameterized queries
    insert_stmt = f'INSERT INTO risk_factors VALUES ({", ".join(["%s"] * len(df.columns))})'
    cs.executemany(insert_stmt, df.values.tolist())
    print(f"✅ Uploaded {len(df)} rows.")
except Exception as e:
    print("❌ Error:", e)
finally:
    cs.close()
    conn.close()
