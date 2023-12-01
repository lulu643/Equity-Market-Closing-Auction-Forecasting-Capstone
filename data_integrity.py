from config import *

import os
import pandas as pd

# Directory containing the stock data
main_directory = DataDir1min

# List of valid dates
valid_dates = ['20220103', '20220104', '20220105']  # Add your dates here

# Initialize an empty DataFrame
corruption_df = pd.DataFrame(columns=['symbol', 'date', 'corruption_type'])

# Function to check file corruption
def check_corruption(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            return 'Empty File'
        elif df.isnull().all().all():
            return 'All NaN'
        elif df.isnull().any().any():
            return 'Some NaN'
        else:
            return 'No Corruption'
    except Exception as e:
        return str(e)

# Iterate over each stock symbol directory
for symbol in os.listdir(main_directory):
    symbol_path = os.path.join(main_directory, symbol)
    if os.path.isdir(symbol_path):
        # Check each valid date
        for date in valid_dates:
            expected_file = f'bars.{symbol}.{date}'
            file_path = os.path.join(symbol_path, expected_file)
            if not os.path.isfile(file_path):
                corruption_df = corruption_df.append({'symbol': symbol, 'date': date, 'corruption_type': 'File Missing'}, ignore_index=True)
            else:
                corruption_type = check_corruption(file_path)
                if corruption_type != 'No Corruption':
                    corruption_df = corruption_df.append({'symbol': symbol, 'date': date, 'corruption_type': corruption_type}, ignore_index=True)

print(corruption_df)
