from postgres.psql import Database
import time
from date_work import DataWork
from orders.export import DataExportDay
from orders.reader import Reader
from changer import Changer


def start():
    db = Database()
    users = db.get_users()
    dt = DataWork().set_date()
    for user in users:
        data = DataExportDay(dt, user[0])
        data.delivery_statistic()
        data.productivity()
        time.sleep(5)


def work():
    db = Database()
    users = db.get_users()
    dt = DataWork().set_date()
    db.delete_metrics()
    for user in users:
        cls_df = Reader(user[0])
        cls_df.read_df()
        change = Changer(cls_df)
        rev, productivity, product, ord_hour = change.change_productivity()
        delivery, cert = change.change_delivery_statistic()
        db.add_metrics(dt, user[1], user[0], rev, productivity, product, ord_hour, delivery, cert)


if __name__ == '__main__':
    start()
    work()
