from orders.reader import Reader
from datetime import timedelta


class Changer:

    def __init__(self, obj: Reader) -> None:
        self.obj = obj

    def change_productivity(self):
        df = self.obj.df_prod

        try:
            revenue = int(df.iloc[0]['Выручка'])
        except IndexError:
            revenue = 0
        except KeyError:
            revenue = 0

        try:
            productivity = int(df.iloc[0]['Выручка на человека в час'])
        except IndexError:
            productivity = 0
        except KeyError:
            productivity = 0

        try:
            order_per_hour = df.iloc[0]['Кол-во заказов на курьера в час']
        except IndexError:
            order_per_hour = 0
        except KeyError:
            order_per_hour = 0

        try:
            product_on_hour = df.iloc[0]['Продуктов на человека в час']
        except IndexError:
            product_on_hour = 0
        except KeyError:
            product_on_hour = 0

        return int(revenue), int(productivity), float(product_on_hour), float(order_per_hour)

    def change_delivery_statistic(self):
        df = self.obj.df_del

        try:
            avg_del = df.iloc[0]['Среднее время доставки*']
        except IndexError:
            avg_del = timedelta(0)
        except KeyError:
            avg_del = timedelta(0)

        try:
            cert = df.iloc[0]['Количество просроченных заказов']
        except IndexError:
            cert = 0
        except KeyError:
            cert = 0

        return avg_del, int(cert)
