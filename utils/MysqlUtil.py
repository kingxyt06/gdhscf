import pymysql
from config.conf import ConfigReader

# host=ConfigReader().config['BASE']['qa']['mysql-url'],
# user=ConfigReader().config['BASE']['qa']['mysql-user'],
# password=ConfigReader().config['BASE']['qa']['mysql-pwd'],

class MySQLClient:
    def __init__(self, host,port, user, password):
        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            cursorclass=pymysql.cursors.DictCursor
        )
    def sql_cursor(self):
        cursor = self.connection.cursor()
        return cursor

    def select_database(self, database):
        self.connection.select_db(database)

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        self.connection.commit()
        return result

    def close(self):
        self.connection.close()
