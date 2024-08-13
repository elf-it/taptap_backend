import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def helper(s):
    s = str(s)
    return "'" + str(s) + "'"

def helper2(k, v):
    string = ""
    for l in range(len(k)):
        string += k[l] + "=" + "'" + str(v[l]) + "',"
    string = string[:len(string) - 1]
    return string

class Connection:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                database=os.getenv("DB_NAME")
            )
            #return connection
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
            return False
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            
    def insert(self, table: str, keys: list, values: list):
        if len(keys) == len(values):
            try:
                cursor = self.connection.cursor()
                insert_query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table, ', '.join(keys), ', '.join(map(helper, values)))
                cursor.execute(insert_query)
                self.connection.commit()
                cursor.close()
            except (Exception, Error) as error:
                print("Ошибка insert PostgreSQL", error)
        else:
            print("Не совпадает количество ключей и данных")
            
    def update(self, table: str, keys: list, values: list, id: int):
        if len(keys) == len(values):
            try:
                cursor = self.connection.cursor()
                insert_query = "UPDATE {0} set {1} WHERE id = {2};".format(table, helper2(keys, values), str(id))
                cursor.execute(insert_query)
                self.connection.commit()
                cursor.close()
            except (Exception, Error) as error:
                print("Ошибка update PostgreSQL", error)
        else:
            print("Не совпадает количество ключей и данных")

    def updateFromStr(self, s: str):
        try:
            cursor = self.connection.cursor()
            cursor.execute(s)
            self.connection.commit()
            cursor.close()
        except (Exception, Error) as error:
            print("Ошибка update PostgreSQL", error)

    def delete(self, table: str, id: int):
        try:
            cursor = self.connection.cursor()
            insert_query = "DELETE FROM {0} WHERE id={1};".format(table, str(id))
            cursor.execute(insert_query)
            self.connection.commit()
            cursor.close()
        except (Exception, Error) as error:
            print("Ошибка delete PostgreSQL", error)
            
    def select(self, table: str, where_key: str = "", where_value: str = "", key: list = "*"):
        try:
            cursor = self.connection.cursor()
            if where_key != "":
                cursor.execute("SELECT {3} FROM {0} WHERE {1} = '{2}';".format(table, where_key, where_value, ", ".join(map(str, key))))
                return cursor.fetchall()
            else:
                cursor.execute("SELECT {1} FROM {0};".format(table, ", ".join(map(str, key))))
                return cursor.fetchall()
            cursor.close()
        except (Exception, Error) as error:
            print("Ошибка select PostgreSQL", error)

    # where_key_value = "key=value, key=value ..."
    def selectWhereList(self, table: str, where_key_value: str = "", key: list = "*"):
        try:
            cursor = self.connection.cursor()
            if where_key_value != "":
                cursor.execute("SELECT {2} FROM {0} WHERE {1};".format(table, where_key_value, ", ".join(map(str, key))))
                return cursor.fetchall()
            else:
                cursor.execute("SELECT {1} FROM {0};".format(table, ", ".join(map(str, key))))
                return cursor.fetchall()
            cursor.close()
        except (Exception, Error) as error:
            print("Ошибка select PostgreSQL", error)