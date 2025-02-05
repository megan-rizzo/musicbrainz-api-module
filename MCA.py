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

# Get coordinates of categories (how each category contributes to components)
category_coordinates = mca.column_coordinates(df_sample)

# Display which categories load heavily
print(category_coordinates)

# Save MCA result and sample data
df_sample.to_csv("MCA_sampled_data.csv", index=False)
mca_result.to_csv("MCA_results.csv", index=False)
