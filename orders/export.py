import requests
import fake_useragent
from datetime import date
from postgres.psql import Database


class DataExportDay:

    def __init__(self, date_end: date, name: str):
        db = Database()
        data = db.get_data(name)
        self.name = name
        self.rest = data[0]
        self.uuid = data[2]
        self.date_end = date_end
        self.login = data[3]
        self.password = data[4]
        self.code = data[5]
        self.session = None
        self.user = None
        self.header = None
        self.auth()

    def auth(self):
        self.session = requests.Session()
        self.user = fake_useragent.UserAgent().random
        log_data = {
            'CountryCode': self.code,
            'login': self.login,
            'password': self.password
        }
        self.header = {
            'user-agent': self.user
        }
        log_link = f'https://auth.dodopizza.{self.code}/Authenticate/LogOn'
        self.session.post(log_link, data=log_data, headers=self.header)

    def save(self, orders_data):
        for order in orders_data:
            response = self.session.post(orders_data[order]['link'], data=orders_data[order]['data'],
                                         headers=self.header)
            with open(f'./orders/export/{order}_{self.name}.xlsx', 'wb') as file:
                file.write(response.content)
                file.close()
            self.session.close()

    def productivity(self):
        orders_data = {
            'productivity': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/Productivity/Export',
                'data': {
                    "unitId": self.rest,
                    "beginDate": self.date_end,
                    "endDate": self.date_end,
                    "Interval": "24"
                }
            }
        }
        self.save(orders_data)

    def delivery_statistic(self):
        orders_data = {
            'del_statistic': {
                'link': f'https://officemanager.dodopizza.{self.code}/Reports/DeliveryStatistic/Export',
                'data': {
                    "unitsIds": self.rest,
                    "beginDate": self.date_end,
                    "endDate": self.date_end
                }
            }
        }
        self.save(orders_data)
