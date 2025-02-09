# example_xrp.py
import datetime
from BinanceUtil import BinanceUtil

if __name__ == '__main__':
    symbol = "XRPUSDT"
    interval = "1h"  
    start_time = datetime.datetime(2014, 1, 1)  # XRP stabilization year
    end_time = datetime.datetime.now()

    binance_xrp = BinanceUtil(symbol=symbol)
    df_xrp = binance_xrp.get_historical_data(interval, start_time, end_time)

    if df_xrp is not None:
        binance_xrp.save_data(dir_path="./data")  # Save with default name in ./data
        print(f"XRP data downloaded and saved.  First 5 rows:\n{df_xrp.head()}")
    else:
        print("Failed to retrieve XRP data.")