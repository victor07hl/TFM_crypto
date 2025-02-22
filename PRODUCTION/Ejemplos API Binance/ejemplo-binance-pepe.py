#ejemplo-binance-pepe.py
import datetime
import os
import sys

# Añade el directorio padre al path de búsqueda de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BinanceUtil import BinanceUtil
from FileHelper import FileHelper

if __name__ == '__main__':
    # --- Obtener datos de PEPEUSDT y guardarlos ---
    symbol = "PEPEUSDT"
    interval = "1h"
    start_time = datetime.datetime(2023, 4, 17)  # PEPE creation date (approx.)
    end_time = datetime.datetime.now()

    try:
        # Obtener datos de Binance
        binance = BinanceUtil(symbol=symbol)
        df = binance.get_historical_data(
            interval=interval,
            start_time=start_time,
            end_time=end_time
        )

        # Guardar los datos (si se obtuvieron)
        if df is not None:
            file_helper = FileHelper()  # Instancia sin argumentos
            file_helper.save_csv(df, file_path="./data", file_name=f"datos_{symbol}.csv") #Pasamos argumentos
            print(f"{symbol} data downloaded and saved. First 5 rows:\n{df.head()}")
        else:
            print(f"Failed to retrieve {symbol} data.")

    except Exception as e:
        print(f"Error: {e}")