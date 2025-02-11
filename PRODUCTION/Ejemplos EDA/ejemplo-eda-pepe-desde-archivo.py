# ejemplo-eda-pepe-desde-archivo.py
import datetime
import os
import sys

# Añade el directorio padre al path de búsqueda de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from CryptoEDA import CryptoEDA
from FileHelper import FileHelper

if __name__ == '__main__':
    try:
        # 1. Cargar datos con FileHelper
        file_helper = FileHelper()  # Instancia sin argumentos
        pepe_df = file_helper.load_csv(file_path="./data", file_name="datos_PEPEUSDT_.csv") #Pasamos path y nombre.  Ruta relativa CORRECTA.


        # 2. Crear instancia de CryptoEDA y procesar
        eda = CryptoEDA(data=pepe_df)
        processed_df = eda.apply_eda()

        # 3. Mostrar resultados (opcional) o volver a guardar.
        print("Datos de PEPEUSDT procesados (primeras 5 filas):\n", processed_df.head())

        # O, volver a guardar (opcional - útil si quieres un archivo limpio separado):
        # CORREGIDO:  file_name, no output_file_name.  Y ruta relativa correcta.
        file_helper.save_csv(processed_df, file_path="./data/processed", file_name="processed_pepe_from_file.csv")


    except Exception as e:
        print(f"Error: {e}")