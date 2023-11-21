from my_directories import *
import pandas as pd


class ReadDataTeammate:
    def __init__(self):
        self.all_cross_path = data_teammate_dir + '/all_intraday_df.parquet'
        self.all_imbalance_path = data_teammate_dir + '/all_imbalance_df.parquet'
        self.all_intraday_path = data_teammate_dir + '/all_intraday_df.parquet'

    def get_data(self, data_type):
        """
        :param data_type: (str) 'all_cross', 'all_imbalance', or 'all_intraday'
        :return: (dataframe) data
        """
        data_type_to_path = {
            'all_cross': self.all_cross_path,
            'all_imbalance': self.all_imbalance_path,
            'all_intraday': self.all_intraday_path
        }

        df = pd.read_parquet(data_type_to_path[data_type])
        return df


if __name__ == "__main__":
    my_obj = ReadDataTeammate()
    df = my_obj.get_data('all_cross')
    print(df.columns)
