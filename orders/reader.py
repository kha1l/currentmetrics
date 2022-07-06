import pandas as pd


class ReadFile:

    def __init__(self, name_rest: str):
        self.name = name_rest

    def open_file(self, order: str, rows: int):
        try:
            df = pd.read_excel(f'./orders/export/{order}_{self.name}.xlsx', skiprows=rows)
        except ValueError:
            df = pd.DataFrame()
        return df


class Reader(ReadFile):

    df_prod = None
    df_del = None

    def read_df(self):
        self.df_prod = self.open_file('productivity', 4)
        self.df_del = self.open_file('del_statistic', 5)
