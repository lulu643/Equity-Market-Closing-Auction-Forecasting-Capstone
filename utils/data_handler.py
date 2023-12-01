# extract all zipped files
import tarfile
import gzip
import os

folder_path = '//data/raw_data/compress_out_1m'
# folder_path = '/Users/sihanliu/Desktop/Volume_PCA/data/raw_data/compress_out_addl2'
out_path = '//data'

# Create a function to extract tar files while maintaining the structure
def extract_tar_files(in_path, output_path):
    for filename in os.listdir(in_path):
        if filename.endswith('.tar.gz'):
            tar_path = os.path.join(in_path, filename)
            with tarfile.open(tar_path, 'r') as tar:
                tar.extractall(path=output_path)  # Extract files to the "bar_out" folder
                print(f'Extracted: {tar_path}')

# Call the function to extract the tar files
extract_tar_files(folder_path, out_path)




