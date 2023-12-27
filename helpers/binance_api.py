import logging
import requests
import pandas as pd
from datetime import datetime


class BinanceAPI:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.base_url = 'https://api.binance.com/api/v3/klines'

    def fetch_data_for_range(self, symbol, interval, date_from, date_to):
        start_time = self.date_to_ms(date_from)
        end_time = self.date_to_ms(date_to)
        return self.historic_data(symbol, interval, start_time, end_time)

    def historic_data(self, symbol, interval='1d', start_time=None, end_time=None, limit=1000):
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': end_time,
            'limit': limit
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()

        # Handle potential errors in response
        if not isinstance(data, list):
            self.logger.error(f"Error fetching data: {data.get('msg', 'Unknown error')}")
            return pd.DataFrame()

        cols = ['openTime', 'Open', 'High', 'Low', 'Close', 'Volume',
                'cTime', 'qVolume', 'trades', 'takerBase', 'takerQuote', 'Ignore']
        df = pd.DataFrame(data, columns=cols)
        df['Date'] = pd.to_datetime(df['openTime'], unit='ms')
        df.set_index('Date', inplace=True)
        df.drop(columns =['openTime'], axis=1, inplace=True)

        return df.drop(cols[6:], axis=1)

    def date_to_ms(self, date_str):
        """Converts a date string to milliseconds since epoch."""
        dt_obj = datetime.strptime(date_str, '%Y-%m-%d')
        millisec = int(dt_obj.timestamp() * 1000)
        return millisec

    def historic_data_full(self, symbol, interval, date_from, date_to):
        """Fetches full historical data for a given symbol and interval within the date range."""
        start_time = self.date_to_ms(date_from)
        end_time = self.date_to_ms(date_to)

        # Create an empty DataFrame to hold all fetched data
        all_data = pd.DataFrame()

        while True:
            df = self.historic_data(symbol, interval, start_time, end_time)

            if df.empty:
                break

            all_data = pd.concat([all_data, df])

            # Binance's end time is exclusive, so we start from the next interval
            start_time = int(df['Date'].iloc[-1].timestamp() * 1000) + 1

            # If we've reached the end of our time range, stop fetching
            if start_time > end_time:
                break

        all_data.set_index('Date', inplace=True)
        return all_data
