import pandas as pd
import utils
from config import *
import os
import numpy as np

# Retrieve the complete list of stocks for PCA analysis
all_stocks = pca_utils.get_stock_list()

# Create a copy of all stocks for modification during analysis
working_stock_list = all_stocks.copy()

# Initialize a dictionary to track stocks with data issues
corrupted_stocks = {
    "empty file": [],        # List stocks with empty files
    "file not exist": [],    # List stocks whose files do not exist
    "file all NaN": [],      # List stocks with files containing only NaN values
    "file some NaN": []      # List stocks with files containing some NaN values
}

# Set the start and end dates for the PCA analysis period
start_date, end_date = "20220103", "20220404"

# Generate a list of date strings within the specified range
dates = pca_utils.get_dates_strings(start_date, end_date)

# initialize an empty container to store volume surprise arrays
# key: stock, value: volume surprise (time_of_day, date)
volume_surprises_dict = {}

for stock in all_stocks:
    print(stock)
    totalBins = 481  # number of 1 minute bins in the dataset
    totalDates = len(dates)
    volume_array = np.zeros([totalBins, totalDates])

    try:  # Reading data
        for d, date in enumerate(dates):
            file_name = os.path.join(DataDir1min, stock, f"bars.{stock}.{date}")
            in_df = pd.read_csv(file_name, sep="\s+")
            volume_array[:, d] = in_df.loc[:, 'trade_volume']
    except ValueError as e:  # empty file
        if "could not broadcast input array from shape" in str(e):
            print(f"Error occurred for stock: {stock}")
            print("Error details:", e)
            working_stock_list.remove(stock)
            corrupted_stocks["empty file"].append(stock)
            continue  # jump to the next stock
        else:
            raise
    except FileNotFoundError as e:  # file not exist
        if "No such file or directory" in str(e):
            print(f"Error occurred for stock: {stock}")
            print("Error details:", e)
            working_stock_list.remove(stock)
            corrupted_stocks["file not exist"].append(stock)
            continue  # jump to the next stock
        else:
            raise

    volume_array = pca_utils.reshape_volume_array(volume_array, first_bin=31, last_bin=420, bin_width=30)
    # compute volume surprise
    volume_surprise = pca_utils.compute_volume_surprise(volume_array, rolling_window=20)
    # add volume surprise array to our volume_surprises_container
    print(volume_surprise)
    if np.all(np.isnan(volume_surprise)):  # file of all NaN
        print(f"{stock} has file of all NaN.")
        working_stock_list.remove(stock)
        corrupted_stocks["file all NaN"].append(stock)
    elif np.any(np.isnan(volume_surprise)):
        print(f"{stock} has file of some NaN.")
        working_stock_list.remove(stock)
        corrupted_stocks["file some NaN"].append(stock)
    else:
        volume_surprises_dict[stock] = volume_surprise

# reorganize volume surprise arrays of the form fix time slot, volume surprise (stock, date)
formatted_volume_surprises_dict = pca_utils.reorganize_volume_surprises(volume_surprises_dict, working_stock_list)
# perform pca for each volume_surprise array and print the results
print(f'PCA analysis was completed on data from {start_date} to {end_date}.')
pca_utils.perform_pca(formatted_volume_surprises_dict)

print('The number of total stocks is', len(all_stocks))
print('The number of uncorrupted stocks is', len(working_stock_list))
print('The number of corrupted stocks is', sum(len(lst) for lst in corrupted_stocks.values()))
