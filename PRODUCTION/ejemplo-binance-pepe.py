import datetime
from BinanceUtil import BinanceUtil  # Assuming you saved the class as binance_util.py

# --- Simple Example Usage ---
if __name__ == '__main__':
    # Parameters
    symbol = "PEPEUSDT"
    interval = "1h"  # Example: 1-hour candles
    start_time = datetime.datetime(2023, 4, 17)  # PEPEUSDT creation date
    end_time = datetime.datetime.now()  # Current date and time

    # Create a BinanceUtil instance
    binance = BinanceUtil(symbol=symbol)

    # Fetch historical data
    df = binance.get_historical_data(
        interval=interval,
        start_time=start_time,
        end_time=end_time
    )

    # Check if data was retrieved successfully
    if df is not None:
        # Save the data using default file name and directory
        binance.save_data(dir_path="./data")

        # Optionally, print the first few rows to verify
        print(df.head())
    else:
        print("Failed to retrieve historical data.")