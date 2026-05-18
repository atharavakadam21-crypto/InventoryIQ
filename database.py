import sqlite3
import pandas as pd

# Connect database

conn = sqlite3.connect("inventory.db")

# Load CSV

df = pd.read_csv("retail_store_inventory.csv")

# Store into database

df.to_sql(
    "inventory",
    conn,
    if_exists="replace",
    index=False
)

print("Database created successfully!")