# ejemplo-eda-pepe-desde-dataframe.py
import datetime
import os
import sys

# Añade el directorio padre al path de búsqueda de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from BinanceUtil import BinanceUtil
from CryptoEDA import CryptoEDA
from FileHelper import FileHelper  # Importa FileHelper

if __name__ == '__main__':
    try:
        # 1. Obtener datos con BinanceUtil
        binance = BinanceUtil(symbol="PEPEUSDT")
        raw_df = binance.get_historical_data(
            interval="1h",
            start_time=datetime.datetime(2023, 10, 26),
            end_time=datetime.datetime(2023, 10, 27)
        )

        # 2. Verificar que se obtuvieron datos
        if raw_df is not None:
            # 3. Crear instancia de CryptoEDA y procesar
            eda = CryptoEDA(data=raw_df)
            processed_df = eda.apply_eda()

            # 4. Mostrar o guardar los datos procesados.
            print("Datos de PEPEUSDT procesados (primeras 5 filas):\n", processed_df.head())

            # O guardar:  Usar FileHelper.
            file_helper = FileHelper() # Instancia sin argumentos
            file_helper.save_csv(processed_df, file_path="./data/processed", file_name="processed_pepe_from_binance.csv") #Pasamos path y nombre

        else:
            print("No se obtuvieron datos de PEPEUSDT.")

    except Exception as e:
        print(f"Error: {e}")