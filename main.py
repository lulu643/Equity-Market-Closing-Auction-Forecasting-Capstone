import pandas as pd
from pca_utils import *
from utils.group_by_cross_volume import *
from MyDirectories import *

# specify stocks and dates used in PCA analysis
# stocks = top_cross_volume_stocks(data_dir_imbalance, None)  # None means use all stocks
all_stocks = get_stock_list(data_dir_1min)  # list of all stocks
stocks = all_stocks.copy()  # uncorrupted stocks, will be modified later
corrupted_stocks = {"empty file": [], "file not exist": [],
                    "file all NaN": [], "file some NaN": []}  # initialize to store corrupted stocks

start_date, end_date = "20220103", "20220404"
dates = get_dates_strings(data_dir_1min + '/AAPL', start_date, end_date)

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
            file_name = os.path.join(data_dir_1min, stock, f"bars.{stock}.{date}")
            in_df = pd.read_csv(file_name, sep="\s+")
            volume_array[:, d] = in_df.loc[:, 'trade_volume']
    except ValueError as e:  # empty file
        if "could not broadcast input array from shape" in str(e):
            print(f"Error occurred for stock: {stock}")
            print("Error details:", e)
            stocks.remove(stock)
            corrupted_stocks["empty file"].append(stock)
            continue  # jump to the next stock
        else:
            raise
    except FileNotFoundError as e:  # file not exist
        if "No such file or directory" in str(e):
            print(f"Error occurred for stock: {stock}")
            print("Error details:", e)
            stocks.remove(stock)
            corrupted_stocks["file not exist"].append(stock)
            continue  # jump to the next stock
        else:
            raise

    volume_array = reshape_volume_array(volume_array, first_bin=31, last_bin=420, bin_width=30)
    # print(volume_array)
    # compute volume surprise
    volume_surprise = compute_volume_surprise(volume_array, rolling_window=20)
    # add volume surprise array to our volume_surprises_container
    if np.all(np.isnan(volume_surprise)):  # file of all NaN
        print(f"{stock} has file of all NaN.")
        stocks.remove(stock)
        corrupted_stocks["file all NaN"].append(stock)
    elif np.any(np.isnan(volume_surprise)):
        print(f"{stock} has file of some NaN.")
        stocks.remove(stock)
        corrupted_stocks["file some NaN"].append(stock)
    else:
        volume_surprises_dict[stock] = volume_surprise

# reorganize volume surprise arrays of the form fix time slot, volume surprise (stock, date)
formatted_volume_surprises_dict = reorganize_volume_surprises(volume_surprises_dict, stocks)
# perform pca for each volume_surprise array and print the results
print(f'PCA analysis was completed on data from {start_date} to {end_date}.')
perform_pca(formatted_volume_surprises_dict)

print('The number of total stocks is', len(all_stocks))
print('The number of uncorrupted stocks is', len(stocks))
print('The number of corrupted stocks is', sum(len(lst) for lst in corrupted_stocks.values()))
