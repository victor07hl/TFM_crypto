#ejemplo-binance-doge.py
import datetime
import os
import sys

# Añade el directorio padre al path de búsqueda de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BinanceUtil import BinanceUtil
from FileHelper import FileHelper

if __name__ == '__main__':
    symbol = "DOGEUSDT"
    interval = "1h"  # Hourly candles
    start_time = datetime.datetime(2015, 1, 1)  # DOGE stabilization year
    end_time = datetime.datetime.now()

    try:
        binance_doge = BinanceUtil(symbol=symbol)
        df_doge = binance_doge.get_historical_data(interval, start_time, end_time)

        if df_doge is not None:
            file_helper = FileHelper() # Instancia sin argumentos
            file_helper.save_csv(df_doge, file_path="./data", file_name=f"datos_{symbol}.csv") #Pasamos argumentos
            print(f"DOGE data downloaded and saved. First 5 rows:\n{df_doge.head()}")
        else:
            print("Failed to retrieve DOGE data.")
    except Exception as e:
        print(f"An error occurred: {e}")