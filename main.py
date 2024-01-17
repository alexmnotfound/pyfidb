import sys
sys.path.append(".")  # Add the parent directory to sys.path
import logging
import json
from datetime import datetime
from helpers.db_manager import DatabaseManager
from helpers.binance_api import BinanceAPI
from helpers.data_processor import DataProcessor
from config import DB_CONFIG


def main():
    try:
        # Configure logging
        loggingLevel = logging.ERROR

        logging.basicConfig(
            level=loggingLevel,  # Adjust as needed (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        logger = logging.getLogger(__name__)
        logger.debug("--- Script started ---")

        print(f" ----------------- -----------------")
        print(f"     DATABASE MANAGER By PsyDuck    ")
        print(f" ----------------- -----------------")

        # Init DB connection
        logger.debug("--- Checking for DB connection ---")
        db_manager = DatabaseManager(DB_CONFIG)
        connection = db_manager.connect()

        # Only run when connection is reached
        if not connection:
            logger.error("Failed to connect to the database.")
            raise Exception("ERROR: Please check the DB Connection")

        logger.debug("--- Successfully Connected Database ---")
        input("\nPress any key to continue... ")

        # Define User input
        valid_options = ["1", "2", "0", "Download", "Check", "Exit"]
        user_input = get_user_input(valid_options)

        # Do process according to input
        if user_input == "1" or user_input == "Download":
            download_OHLC(db_manager, connection, logger)
        elif user_input == "2" or user_input == "Check":
            check_database(db_manager, connection, logger)
        else:
            print("Nothing to do here, see you later :)\n")
        sys.exit(0)

    except Exception as e:
        print(e)
        sys.exit(1)


def get_user_input(valid_options):
    while True:
        user_input = input("\n\nPlease choose what you wanna do:\n"
                           " 1 - Download OHLC to DB,\n"
                           " 2 - Check OHLC from Ticker,\n"
                           " 0 - Exit\n"
                           "You > ").strip().lower()

        if user_input in valid_options:
            return user_input
        else:
            print("\nYou selected an invalid option, please try again.")


def download_OHLC(db_manager, connection, logger):
    print(f" ----------------- -----------------\n")
    print(f"Okay, let's download some information ;)\n")

    print(" Here are the default values from the config. \n"
          " In case you want something different, please modify it.")
    while True:
        # Read download_params from the JSON file
        with open('download_params.json', 'r') as file:
            download_params = json.load(file)

        symbols = download_params['symbols']
        intervals = download_params['intervals']
        date_from = download_params['date_from']
        date_to = download_params['date_to']
        print(f"\n Symbols to download: {symbols} \n"
              f" Intervals to download: {intervals} \n"
              f" Date from {date_from} to {date_to} \n")

        user_input = input("Press any key to reload OHLC or ENTER to continue using this data.\n"
                           "You > ").strip().lower()
        if user_input == "":
            break

    for symbol in symbols:
        for interval in intervals:
            # Fetch data from Binance for the given range
            print(f"Fetching data for {symbol} from {date_from} to {date_to} with timeframe {interval}")
            binance_data = BinanceAPI().fetch_data_for_range(symbol, interval, date_from, date_to)
            logger.debug(f'------- DEBUG FETCHED DATA ------- \n{binance_data.head(5)}\n...\n{binance_data.tail(5)}\n')

            # Only do things if there is info from Binance
            if not binance_data.empty:
                # Check for table or create it if necessary
                table_name = f'{symbol}_{interval}'
                db_manager.create_table(connection, table_name)

                # Fetch existing data from the database
                existing_dates = set(
                    db_manager.fetch_data_for_range(connection, table_name, date_from, date_to))

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


def check_database(db_manager, connection, logger):
    print(f"\n ----------------- -----------------\n")
    print(f"Okay, let's check if everything is in order here...\n")
    print(f"I'll check for all the existing tables unless you tell me to look for a specific ticker\n")

    while True:
        symbol = input(" Please enter your symbol, or ENTER to check all tables, or EXIT to exit the script: \n"
                       "You > ").strip().upper()
        if symbol == "EXIT":
            print(f"\nExiting script...\n")
            sys.exit(1)
        elif symbol != "":
            print(f"\nLooking for {symbol} in database...")
        table_names = db_manager.fetch_tables_with_keyword(connection, symbol)

        if len(table_names) > 0:
            print(f"\n ----------------- -----------------\n")
            print("Tables found:\n")
            for table in table_names:
                earliest_date, latest_date = db_manager.get_table_date_range(connection, table)
                if earliest_date and latest_date:
                    print(f" - '{table}': From Date: {earliest_date}, To Date: {latest_date}")
                else:
                    print(f" - '{table}': No date data available.")
        else:
            print(f"\nNo tables found containing '{symbol}'" if symbol else "\nNo tables found.")
        print("\n")


if __name__ == "__main__":
    main()
