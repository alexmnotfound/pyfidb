import sys
sys.path.append(".")  # Add the parent directory to sys.path
import logging
from datetime import datetime
from helpers.db_manager import DatabaseManager
from helpers.binance_api import BinanceAPI
from helpers.data_processor import DataProcessor
from config import DB_CONFIG


def main():
    # Configure logging
    loggingLevel = logging.DEBUG

    logging.basicConfig(
        level=loggingLevel,  # Adjust as needed (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger(__name__)
    logger.info("--- Script started ---")

    # Init DB connection
    logger.info("--- Checking for DB connection ---")
    db_manager = DatabaseManager(DB_CONFIG['host'], DB_CONFIG['user'], DB_CONFIG['passwd'], DB_CONFIG['database'])
    connection = db_manager.connect()

    # Only run when connection is reached
    if connection:
        # Define your symbols and intervals
        symbols = ['BTCUSDT', 'ETHUSDT']
        # intervals = ['1w', '1d', '4h', '1h', '15m']
        intervals = ['1w', '1d']
        date_from = '2021-01-01'
        date_to = '2021-06-30'

        for symbol in symbols:
            for interval in intervals:
                table_name = f'{symbol}_{interval}'
                db_manager.create_table(connection, table_name)

                # Fetch data from Binance for the given range
                binance_data = BinanceAPI().fetch_data_for_range(symbol, interval, date_from, date_to)
                logging.info(f'------- DEBUG DAATA {binance_data}')

                if not binance_data.empty:
                    # Fetch existing data from the database
                    existing_dates = set(db_manager.fetch_data_for_range(connection, table_name, date_from, date_to))

                    # Get dates from Binance data
                    binance_dates = set(binance_data.index.strftime('%Y-%m-%d'))  # Format as string for comparison

                    # Find missing data by comparing dates
                    missing_dates = binance_dates.difference(existing_dates)

                    # Insert missing data
                    for missing_date_str in missing_dates:
                        missing_date = datetime.strptime(missing_date_str, '%Y-%m-%d').date()
                        missing_data = binance_data.loc[binance_data.index.date == missing_date]

                        if not missing_data.empty:
                            processed_data = DataProcessor.process_data(missing_data)
                            db_manager.insert_data(connection, table_name, processed_data)
                else:
                    logger.warning(
                        f"No data found for {symbol} in interval {interval} between {date_from} and {date_to}")

    else:
        logger.error("Failed to connect to the database.")


if __name__ == "__main__":
    main()
