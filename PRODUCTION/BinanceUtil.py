import requests
import datetime
import time
import os
import pandas as pd
from IPython.display import clear_output, display
from typing import List, Optional

class BinanceUtil:
    """
    A utility class for fetching and processing historical K-line (candlestick) data from the Binance API.
    Provides a simplified interface for retrieving and saving cryptocurrency price data.
    """

    def __init__(self, symbol: str, base_url: str = "https://api.binance.com", request_sleep_time: float = 0.25) -> None:
        """
        Initializes the BinanceUtil class.

        Args:
            symbol (str): The trading symbol for the cryptocurrency (e.g., "PEPEUSDT", "BTCUSDT").
            base_url (str, optional): The base URL for the Binance API.  Defaults to the public Binance API endpoint.
            request_sleep_time (float, optional):  The time (in seconds) to wait between API requests to avoid rate limits. Defaults to 0.25 seconds.
        """
        self._base_url: str = base_url
        self._request_sleep_time: float = request_sleep_time
        self.symbol: str = symbol  # Public attribute: The trading symbol.
        self.data_frame: Optional[pd.DataFrame] = None # Public attribute: Stores the fetched and processed data.
        self._kline_column_names: List[str] = [  # Private:  Column names for the K-line data.
            "Open time", "Open", "High", "Low", "Close", "Volume",
            "Close time", "Quote asset volume", "Number of trades",
            "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
        ]


    def _fetch_klines(self, interval: str, start_time_ms: int, end_time_ms: int, request_limit: int = 500) -> List[List]:
        """
        (Private) Fetches K-line (candlestick) data from the Binance API. Handles pagination.

        Args:
            interval (str): The time interval for each candlestick (e.g., "1h", "1d", "4h").
            start_time_ms (int): The start time in milliseconds (Unix timestamp).
            end_time_ms (int): The end time in milliseconds (Unix timestamp).
            request_limit (int, optional): The maximum number of K-lines to retrieve per API request. Defaults to 500.

        Returns:
            list: A list of K-line data, where each element is a list representing a single candlestick.
                  Returns an empty list if an error occurs during the API request.
        """

        all_kline_data: List[List] = []
        num_fragments: int = 0
        total_records: int = 0

        while start_time_ms < end_time_ms:
            clear_output(wait=True)  # Clear output in interactive environments
            try:
                request_url: str = (f"{self._base_url}/api/v3/klines?symbol={self.symbol}&interval={interval}"
                               f"&startTime={start_time_ms}&endTime={end_time_ms}&limit={request_limit}")
                response: requests.Response = requests.get(request_url)
                response.raise_for_status()
                kline_data: List[List] = response.json()

                if kline_data:
                    num_fragments += 1
                    records_in_fragment: int = len(kline_data)
                    total_records += records_in_fragment
                    display(f"Fragment {num_fragments} obtained: {records_in_fragment} records. Total: {total_records}")
                    all_kline_data.extend(kline_data)
                    last_open_time: int = kline_data[-1][0]
                    start_time_ms = last_open_time + 1
                    time.sleep(self._request_sleep_time)
                else:
                    display(f"Empty fragment. Possibly reached the end of available data. Total: {total_records}")
                    break

            except requests.exceptions.RequestException as e:
                print(f"Error during API request: {e}")
                return []
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return []

        return all_kline_data


    def _process_klines(self, raw_kline_data: List[List]) -> pd.DataFrame:
        """
        (Private) Processes raw K-line data. Converts to a Pandas DataFrame, handles timestamps, and calculates price variation.

        Args:
            raw_kline_data (list): The raw K-line data from `_fetch_klines`.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing the processed data.  Also sets `self.data_frame`.
        """

        df: pd.DataFrame = pd.DataFrame(raw_kline_data, columns=self._kline_column_names)

        df['Open time_date'] = pd.to_datetime(df['Open time'], unit='ms').apply(lambda x: x.isoformat())
        df['Close time_date'] = pd.to_datetime(df['Close time'], unit='ms').apply(lambda x: x.isoformat())
        df['Variation'] = df['Close'].astype(float).diff()

        column_order: List[str] = [
            "Open time_date", "Close time_date", "Open time", "Close time", "Open",
            "High", "Low", "Close", "Variation", "Volume", "Quote asset volume",
            "Number of trades", "Taker buy base asset volume",
            "Taker buy quote asset volume", "Ignore"
        ]
        df = df[column_order]

        self.data_frame = df  # Store DataFrame as an instance attribute
        return df



    def save_data(self, dir_path: str, file_name: Optional[str] = None) -> Optional[str]:
        """
        Saves the fetched and processed K-line data (in `self.data_frame`) to a CSV file.

        Args:
            dir_path (str): The directory path where the file will be saved.
            file_name (str, optional): The name of the CSV file. Defaults to "datos_{symbol}.csv".

        Returns:
            Optional[str]: The full path to the saved file, or None if there was an error.
        """
        if self.data_frame is None:
            print("No data to save. Run get_historical_data() first.")
            return None

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if file_name is None:
            file_name: str = f"datos_{self.symbol}.csv"

        file_path: str = os.path.join(dir_path, file_name)

        try:
            self.data_frame.to_csv(file_path, index=False)
            print(f"Data saved to '{file_path}'")
            return file_path
        except Exception as e:
            print(f"Error saving data to CSV: {e}")
            return None



    def get_historical_data(self, interval: str, start_time: datetime.datetime, end_time: datetime.datetime, request_limit: int = 500) -> Optional[pd.DataFrame]:
        """
        Fetches, processes, and stores historical K-line data.

        Args:
            interval (str): The candlestick interval (e.g., "1h", "1d").
            start_time (datetime.datetime): The start date and time.
            end_time (datetime.datetime): The end date and time.
            request_limit (int, optional): Max K-lines per request. Defaults to 500.

        Returns:
            Optional[pd.DataFrame]: The processed DataFrame, also stored in `self.data_frame`. Returns None on error.
        """
        start_time_ms: int = int(start_time.timestamp() * 1000)
        end_time_ms: int = int(end_time.timestamp() * 1000)

        raw_kline_data: List[List] = self._fetch_klines(interval, start_time_ms, end_time_ms, request_limit)
        if not raw_kline_data:
            return None

        processed_df: pd.DataFrame = self._process_klines(raw_kline_data)
        return processed_df