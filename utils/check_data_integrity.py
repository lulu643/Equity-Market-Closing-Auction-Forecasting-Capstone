import os
import pandas as pd


def create_file_size_spreadsheet(root_directory, output_file):
    folders = []
    dates = []
    file_sizes = []

    # Iterate through the directories and files
    for folder, subfolders, files in os.walk(root_directory):
        for file in files:
            file_path = os.path.join(folder, file)
            folder_name = os.path.basename(folder)
            file_name = file
            file_size = os.path.getsize(file_path)

            # Append the information to the respective lists
            folders.append(folder_name)
            dates.append(file_name[-8:])
            file_sizes.append(file_size / 1024)

    # Create a DataFrame from the collected information
    data = {
        'Symbol': folders,
        'Date': dates,
        'Filesize': file_sizes
    }

    df = pd.DataFrame(data)
    df = df.sort_values(by=['Symbol', 'Date'])

    df.to_excel(output_file, index=False)


if __name__ == '__main__':
    from MyDirectories import data_dir_1min
    output_file = '/Users/sihanliu/Desktop/capstone_pycharm/utils/file_size_spreadsheet.xlsx'
    create_file_size_spreadsheet(data_dir_1min, output_file)

    # WORK LOG 20231114
    # Comment: One way to see if a file is corrupted is to check its file size
    # But there is not a standard threshold for all files
    # Need to decide whether a file is corrupted based on individual symbol file size distribution

    # Else, we could just work on the volume array
    # if there is more than half 0/NaN, we drop the ticker
    # I think this is the best way

    # Else, use cyy's file, drop all rows with trade_volume=NaN
    # But it seems that sometimes, it is corrupted and shown as 0 in all rows
    # sometimes, it is corrupted, has a lot of 0 and a few values
    # Besides, I have tried, cyy's file is too big for my machine
    # I cannot almost do nothing(operations)
    # I can only try that on Colab
    # or ask him to do it

    # One more thing, the tickers in folder with imbalance/cross data
    # does not match exact the folder with 1min continuous trading data

    # Else, I don't think it is a good idea to use the old data
    # because it only has around 260 stocks
    # and, Hora said that they are randomly picked by Russell 3000
    # It is very likely that there are representative enough
    # But, yes, we could try it

    # One more, we should do PCA on close auction data
    # and, need to do the tests to show whether it works in the final linear regression
