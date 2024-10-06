import pandas as pd


class GroupListService:
    def __init__(self,
                 path_to_csv: str,
                 sep=';'):
        self.data = pd.read_csv(filepath_or_buffer=path_to_csv,
                                sep=sep)

    def get_list_of_group(self,
                          column_name: str):
        series = self.data[column_name]
        return list(series[~series.isnull()])
