import mysql.connector
import logging
from mysql.connector import errorcode


class DatabaseManager:
    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.logger = logging.getLogger(__name__)  # Create a logger for this class

    def connect(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                database=self.database
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.logger.error("Invalid user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.logger.error("Database does not exist")
            else:
                self.logger.debug(err)
            return None

    def create_table(self, connection, table_name):
        self.logger.debug(f"--- Checking table {table_name}")

        cursor = connection.cursor()
        query = (f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
                 f"            Date DATETIME PRIMARY KEY,\n"
                 f"            Open DOUBLE,\n"
                 f"            High DOUBLE,\n"
                 f"            Low DOUBLE,\n"
                 f"            Close DOUBLE,\n"
                 f"            Volume DOUBLE\n"
                 f"        )")
        try:
            cursor.execute(query)
            connection.commit()
            self.logger.info(f"--- Process Success ---")
        except mysql.connector.Error as err:
            self.logger.error(f"Failed creating table {table_name}: {err}")
        finally:
            cursor.close()

    def fetch_data_for_range(self, connection, table_name, date_from, date_to):
        cursor = connection.cursor()
        query = f"SELECT Date FROM {table_name} WHERE Date BETWEEN %s AND %s"
        try:
            cursor.execute(query, (date_from, date_to))
            # This will format each date object to a string in 'YYYY-MM-DD' format for comparison
            return [row[0].strftime('%Y-%m-%d') for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            self.logger.error(f"Failed to fetch data for range: {err}")
            return []
        finally:
            cursor.close()

    def insert_data(self, connection, table_name, data):
        self.logger.info(f"--- Inserting Data into table {table_name}")
        self.logger.debug(f"Data to be inserted: {data}")

        cursor = connection.cursor()
        query = f"INSERT INTO {table_name} (Date, Open, High, Low, Close, Volume) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cursor.executemany(query, data)
            connection.commit()
            self.logger.info(f"--- Process Success ---")
        except mysql.connector.Error as err:
            self.logger.error(f"Failed to insert data into {table_name}: {err}")
        finally:
            cursor.close()
            self.logger.debug(f"--- Closing cursor")
