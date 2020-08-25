from flask import Flask
import mysql.connector
from decouple import config
from data.DataLayer import DataLayer


class SQLiteDataLayer(DataLayer):
    def __init__(self):
        super().__init__()
        self.__connect()

    def __connect(self):
        try:
            self.__sqlDb = mysql.connector.connect(
                host="127.0.0.1",
                user=config('MYSQL_USER'),
                password=config('PASSWORD'),
                database='roofarm'
            )
        except Exception as e:
            print(e)

    def close(self):
        self.__sqliteDb.close()

    def add_address(self, lat, long):
        cursor = self.__sqliteDb.cursor()
        try:
            self.__sqliteDb.start_transaction()
            sql = 'INSERT INTO addresses (lat, long) VALUES (%s, %s)'
            values = (lat, long,)
            cursor.execute(sql, values)
            self.__sqliteDb.commit()
            count = cursor.rowcount
            return ("Inserted successfully " + count)
        except Exception as e:
            return e
        finally:
            cursor.close()

    def get_result(self, result, address_id):
        cursor = self.__sqliteDb.cursor()
        try:
            sql = 'INSERT INTO results (res, id_address) VALUES (%s, %s)'
            values = (result, address_id)
            cursor.execute(sql, values)
            return "Inserted successfully " + cursor.rowcount
        finally:
            cursor.close()

    def add_email(self, email, lat, long):
        cursor = self.__sqliteDb.cursor()
        try:
            users_address = None
            sql_address = 'SELECT idaddresses FROM addresses ' \
                          'WHERE lat=%s, long=%s'
            values = (lat, long)
            cursor.execute(sql_address, values)
            self.__sqliteDb.commit()
            for (id_address) in cursor:
                users_address = id_address
            sql_email = 'INSERT INTO users (email, id_user_address) VALUES (%s, %s)'
            values = (email, users_address)
            cursor.execute(sql_email, values)
            self.__sqliteDb.commit()
            count = cursor.rowcount
            return ("Inserted successfully " + count)
        except Exception as e:
            return e
        finally:
            cursor.close()
