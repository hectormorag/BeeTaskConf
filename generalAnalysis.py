import pandas as pd

# Load the file
df = pd.read_parquet("Hive_A_2024-07-20T03_00_00Z--2024-07-20T09_00_00Z.parquet")

# Count unique bee IDs
num_unique_bees = df["bee_id"].nunique()

print(f"Number of unique bee IDs: {num_unique_bees}")
