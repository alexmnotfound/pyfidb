import mysql.connector
import logging
from mysql.connector import errorcode


class DatabaseManager:
    def __init__(self, db_config):
        self.host = db_config['host']
        self.user = db_config['user']
        self.passwd = db_config['passwd']
        self.database = db_config['database']
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
            self.logger.debug(f"--- Process Success ---")
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
        self.logger.debug(f"--- Inserting Data into table {table_name}")
        self.logger.debug(f"Data to be inserted: {data}")

        cursor = connection.cursor()
        query = f"INSERT INTO {table_name} (Date, Open, High, Low, Close, Volume) VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cursor.executemany(query, data)
            connection.commit()
            self.logger.debug(f"--- Process Success ---")
        except mysql.connector.Error as err:
            self.logger.error(f"Failed to insert data into {table_name}: {err}")
        finally:
            cursor.close()
            self.logger.debug(f"--- Closing cursor")

    def fetch_tables_with_keyword(self, connection, keyword):
        """Fetches names of all tables in the database that contain the given keyword."""
        self.logger.debug(f"Fetching all table names containing '{keyword}' from the database.")

        cursor = connection.cursor()
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = %s AND table_name LIKE %s"
        like_pattern = f"%{keyword}%"
        try:
            cursor.execute(query, (self.database, like_pattern))
            # Fetch all table names that include the keyword
            table_names = [row[0] for row in cursor.fetchall()]
            return table_names
        except mysql.connector.Error as err:
            self.logger.error(f"Failed to fetch table names: {err}")
            return []
        finally:
            cursor.close()
            self.logger.debug("--- Closing cursor ---")

    def get_table_date_range(self, connection, table_name):
        """Fetches the earliest and latest date in the given table."""
        self.logger.debug(f"Fetching date range for table {table_name}")

        cursor = connection.cursor()
        query = f"SELECT MIN(Date), MAX(Date) FROM {table_name}"
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            return result  # Returns a tuple (earliest_date, latest_date)
        except mysql.connector.Error as err:
            self.logger.error(f"Failed to fetch date range for table {table_name}: {err}")
            return None, None
        finally:
            cursor.close()
