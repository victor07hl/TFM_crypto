# example_doge.py
import datetime
from BinanceUtil import BinanceUtil

if __name__ == '__main__':
    symbol = "DOGEUSDT"
    interval = "1d"  # Daily candles
    interval = "1h"  # Hourly candles
    start_time = datetime.datetime(2015, 1, 1)  # DOGE stabilization year
    end_time = datetime.datetime.now()

    binance_doge = BinanceUtil(symbol=symbol)
    df_doge = binance_doge.get_historical_data(interval, start_time, end_time)

    if df_doge is not None:
        binance_doge.save_data(dir_path="./data")  # Save with default name in ./data
        print(f"DOGE data downloaded and saved. First 5 rows:\n{df_doge.head()}")
    else:
        print("Failed to retrieve DOGE data.")