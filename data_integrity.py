import os
import pandas as pd
from config import data_dir_1min
from utils import get_valid_dates


def is_valid_file(file_path, verbose=True):
    """
    Validates data file at 'file_path' to ensure it exists, is not empty, and the 'trade_volume'
    column in rows 31 to 420 has no NaN values. If 'verbose' is True, prints out the failure reason.
    """
    def log(message):
        if verbose:
            print(message)

    if not os.path.isfile(file_path):
        log(f"File check failed: {file_path} does not exist.")
        return False

    try:
        in_df = pd.read_csv(file_path, sep="\s+")

        if in_df.empty:
            log(f"File check failed for {file_path}: The file is empty.")
            return False

        trade_volume = in_df.loc[31:420, 'trade_volume']
        if trade_volume.isna().any():
            log(f"File check failed for {file_path}: 'trade_volume' contains NaN values.")
            return False

        return True

    except Exception as e:
        log(f"Error processing file: {file_path}, Error: {e}")
        return False


def run_data_integrity_checks(main_directory, valid_dates, verbose=True):
    """
    Runs data integrity checks for all stock symbols in the main directory based on valid dates.
    If 'verbose' is True, prints out information about corrupted files.
    """
    corrupted_symbols = set()
    for stock_symbol in os.listdir(main_directory):
        symbol_path = os.path.join(main_directory, stock_symbol)
        if os.path.isdir(symbol_path):
            for date in valid_dates:
                file_path = os.path.join(symbol_path, f'bars.{stock_symbol}.{date}')
                if not is_valid_file(file_path, verbose):
                    corrupted_symbols.add(stock_symbol)
                    break
    return corrupted_symbols


if __name__ == "__main__":
    valid_dates = get_valid_dates("20220913", "20221230")

    corrupted_symbols = run_data_integrity_checks(data_dir_1min, valid_dates, verbose=True)
    print(f"Number of corrupted symbols: {len(corrupted_symbols)}")
