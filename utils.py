import numpy as np
from sklearn.decomposition import PCA
from config import *
import os


def get_stock_list(folder_path=DataDir1min):
    """
    Extract a list of unique stock names from the dataset
    """
    stocks = []
    for item in os.listdir(folder_path):
        full_path = os.path.join(folder_path, item)
        if os.path.isdir(full_path):
            stocks.append(item)
    return sorted(stocks)


def get_dates_strings(start_date, end_date, folder_path=DataDir1min+'/AAPL'):
    matching_dates = []

    for filename in os.listdir(folder_path):
            date_str = filename[-8:]
            if start_date <= date_str <= end_date:
                matching_dates.append(date_str)
    return sorted(matching_dates)


def reshape_volume_array(volume_array, first_bin, last_bin, bin_width):
    """
    Select proper time range, bucket into bin_width, transform to cumulative volume

    first_bin = 31  # timestamp 09:31:00 (09:30:00-09:31:00)
    last_bin = 420  # timestamp 16:00:00 (15:59:00-16:00:00)
    bin_width = 30  # bucket data into bin_width bins
    """
    # select proper time range
    volume_array = volume_array[first_bin:last_bin + 1, :]

    # change bin_width
    totalDates = volume_array.shape[1]
    nSlots = int((last_bin - first_bin + 1) / bin_width)
    reshaped_volume_array = np.zeros([nSlots, totalDates])  # initialize an empty array to store reshaped volume array
    for t in range(nSlots):
        i = t * bin_width
        j = i + bin_width
        reshaped_volume_array[t, :] = np.sum(volume_array[i:j, :], axis=0)

    # transform to cumulative volume
    cum_volume_array = np.cumsum(reshaped_volume_array, axis=0)
    return cum_volume_array


def compute_volume_surprise(volume_array, rolling_window=20):
    """
    Fix stock, from its volume_array (time_of_day, date), compute volume surprise (time_of_day, date)
    """
    nSlots = volume_array.shape[0]
    nDates = volume_array.shape[1] - rolling_window  # nDates where we have a volume surprise

    # initialize an empty array to contain volume surprise
    volume_surpise = np.zeros([nSlots, nDates])
    # fill in each column
    for i in range(nDates):
        # compute previous rolling_window average
        volume_average = np.mean(volume_array[:, i:i + rolling_window], axis=1)
        # volume surprise = volume on day i / its previous rolling_window average - 1
        volume_surpise[:, i] = volume_array[:, i + rolling_window] / volume_average - 1
    return volume_surpise


def reorganize_volume_surprises(volume_surprises_container, stocks):
    """
    @params
    volume_surprises_container: key: stock, value: volume_surprise (time_of_day, date)

    @return
    volume_surprises_container_keyTime: key: time_of_day, value: volume_surprise (stock, date)
    """
    an_arbitrary_key = list(volume_surprises_container.keys())[0]
    nSlots = volume_surprises_container[an_arbitrary_key].shape[0]
    totalStocks = len(volume_surprises_container)
    nDates = volume_surprises_container[an_arbitrary_key].shape[1]
    # initialize an empty array to store the results
    volume_surprises_container_keyTime = {key: np.zeros([totalStocks, nDates]) for key in range(nSlots)}
    # take out each volume_surprise array in original container
    for i in range(totalStocks):
        stock = stocks[i]
        volume_surprise = volume_surprises_container.get(stock)
        # for each fixed stock volume surprise array
        for slot in range(nSlots):
            # take our each row of the volume surprise array, put it into different arrays
            volume_surprises_container_keyTime.get(slot)[i, :] = volume_surprise[slot, :]
    return volume_surprises_container_keyTime


def perform_pca(volume_surprises_container_keyTime):
    """
    @params
    volume_surprises_container_keyTime: key: time_of_day, value: volume_surprise (stock, date)
    """
    print('Variances explained by the first few principle component are:')
    for slot, volume_surprise_array in volume_surprises_container_keyTime.items():
        pca = PCA(n_components=5)
        pca.fit(volume_surprise_array)  # X array-like of shape (n_samples, n_features)
        print(f'30 mins bucket number {slot}: \t', pca.explained_variance_ratio_)
#         first_component = pca.components_[0]
#         plt.scatter(range(volume_surprise_array.shape[1]), first_component)
#         plt.title(str(slot) + ' first component')
#         plt.show()
