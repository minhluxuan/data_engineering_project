import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
df = pd.read_csv('.\data\processed\Olympic_Games_Summary.csv')

# Replace 'True' with 1 and 'False' with 0 in the 'isHeld' column
# df['isHeld'] = df['isHeld'].map({'True': 1, 'False': 0})

# Replace empty strings with NaN
df['start_date'] = df['start_date'].replace('', np.nan)
df['end_date'] = df['end_date'].replace('', np.nan)
# Save the modified DataFrame back to a CSV file
df.to_csv('.\data\processed\Olympic_Games_Summary.csv', index=False)
