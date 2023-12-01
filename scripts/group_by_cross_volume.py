import os
import gzip


def extract_stock_liquidity_proxy(folder_path):
    """
    :param folder_path: (str) data folder path
    :return: (dict) key: stock_symbol value: paired volume in close auction on 20220111
    """
    stock_liquidity_dict = {}
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.startswith("imbalance") and filename.endswith("20220111.gz"):
                gz_file_path = os.path.join(root, filename)
                with gzip.open(gz_file_path, 'rb') as gz_file:
                    compressed_data = gz_file.read()
                    decompressed_text = compressed_data.decode("utf-8")
                    liquidity_proxy = decompressed_text.split(",")[-2]
                    stock_symbol = filename.split(".")[1]
                    try:
                        liquidity_proxy = int(liquidity_proxy)
                        stock_liquidity_dict[stock_symbol] = liquidity_proxy
                    except Exception as e:
                        pass
                        # print(f"An exception of type {type(e).__name__} occurred for stock symbol {stock_symbol}")
    return stock_liquidity_dict


def top_cross_volume_stocks(imbalance_data_path, n_top_stocks):
    stock_liquidity_dict = extract_stock_liquidity_proxy(imbalance_data_path)
    if n_top_stocks is None:
        return stock_liquidity_dict.keys()
    # import matplotlib.pyplot as plt
    # plt.hist(list(stock_liquidity_dict.values()), bins=20, edgecolor='black')
    # plt.xlabel('Values')
    # plt.ylabel('Frequency')
    # plt.title('Histogram of Dictionary Values')
    # plt.show()
    top_keys = [stock_symbol for stock_symbol, liquidity_proxy in
                sorted(stock_liquidity_dict.items(), key=lambda item: item[1], reverse=True)[:n_top_stocks]]
    return top_keys




