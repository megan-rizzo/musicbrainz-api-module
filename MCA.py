import pandas as pd

# Load the dataset
df = pd.read_csv("Merged_DatasetV2.csv")

# Drop irrelevant columns
df = df.drop(columns=['id', 'name'])

# Check for missing values and handle them
df = df.fillna("Unknown")  # Replace NaN with "Unknown" or another suitable value

print(df.head())


