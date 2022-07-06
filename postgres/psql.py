from datetime import datetime

import psycopg2
from config.cfg import Settings


class Database:
    @property
    def connection(self):
        stg = Settings()
        return psycopg2.connect(
            database=stg.dbase,
            user=stg.user,
            password=stg.password,
            host=stg.host,
            port='5432'
        )

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def get_data(self, name: str):
        sql = '''
            SELECT restId, restName, restUuid, userLogs, userPass, countryCode 
            FROM orders 
            WHERE restName=%s 
            order by restId
        '''
        parameters = (name,)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_users(self):
        sql = '''
            SELECT restName, restId, restTime
            FROM orders
            WHERE status=%s 
            order by restId
        '''
        parameters = ('work',)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def add_metrics(self, dt: datetime, rest_id: int, name_rest: str, rev: float, prod: float, pr: float,
                    oh: float, dv: str, cert: int):
        sql = '''
            INSERT INTO metrics (date, rest_id, name_rest, revenue, 
                        productivity, orders_hour, product, delivery,
                        certificatess) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        parameters = (dt, rest_id, name_rest, rev, prod, pr, oh, dv, cert)
        self.execute(sql, parameters=parameters, commit=True)

    def delete_metrics(self):
        sql = '''
            DELETE FROM metrics
        '''
        self.execute(sql, commit=True)
