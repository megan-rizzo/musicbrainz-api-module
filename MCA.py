import pandas as pd
import prince

# Load the dataset
df = pd.read_csv("Merged_DatasetV2.csv", dtype=str, low_memory=False)

# Drop irrelevant columns
df = df.drop(columns=['id', 'name'])

# Check for missing values and handle them
df = df.fillna("Unknown")  # Replace NaN with "Unknown" or another suitable value

print(df.head())

# Initialize MCA with 2 components
mca = prince.MCA(n_components=2, random_state=42)

# Sample the data to avoid memory issues
df_sample = df.sample(1000, random_state=42)  # Reduce dataset size if needed

# Fit and transform the data (one-hot encoding is handled automatically)
mca_result = mca.fit_transform(df_sample)

# Display the transformed data
print(mca_result.head())
