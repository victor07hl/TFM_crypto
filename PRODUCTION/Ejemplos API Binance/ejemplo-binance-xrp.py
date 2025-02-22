#ejemplo-binance-xrp.py
import datetime
import os
import sys

# Añade el directorio padre al path de búsqueda de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BinanceUtil import BinanceUtil
from FileHelper import FileHelper

if __name__ == '__main__':
    symbol = "XRPUSDT"
    interval = "1h"
    start_time = datetime.datetime(2014, 1, 1)  # XRP stabilization year
    end_time = datetime.datetime.now()

    try:
        binance_xrp = BinanceUtil(symbol=symbol)
        df_xrp = binance_xrp.get_historical_data(interval, start_time, end_time)

        if df_xrp is not None:
            file_helper = FileHelper()  # Instancia sin argumentos
            file_helper.save_csv(df_xrp, file_path="./data", file_name=f"datos_{symbol}.csv")#Pasamos argumentos
            print(f"XRP data downloaded and saved.  First 5 rows:\n{df_xrp.head()}")
        else:
            print("Failed to retrieve XRP data.")

    except Exception as e:
         print(f"An error occurred: {e}")