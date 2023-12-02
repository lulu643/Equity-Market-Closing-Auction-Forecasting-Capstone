import pandas as pd
# pd.set_option('display.max_columns', None)
import gzip

filepath = "/Users/sihanliu/Desktop/Volume_PCA/data/out_1m/TFC/bars.TFC.20221227"
gz_file_path1 = "//data/out_addl2/FE/imbalance.FE.nasdaq.20220124.gz"
gz_file_path2 = "//data/out_addl2/FE/cross.FE.20220124.gz"

#############
# For normal file
df = pd.read_csv(filepath, sep="\s+")
print(df.iloc[100:120])

#############
# For gz imbalance file
# with gzip.open(gz_file_path1, 'rb') as gz_file:
#     compressed_data = gz_file.read()
#     decompressed_text = compressed_data.decode("utf-8")
#     print(decompressed_text)
#     print(decompressed_text.split(",")[-2])

#############
# For gz cross file
# with gzip.open(gz_file_path2, 'rb') as gz_file:
#     compressed_data = gz_file.read()
#     decompressed_text = compressed_data.decode("utf-8")
#     print(decompressed_text)


