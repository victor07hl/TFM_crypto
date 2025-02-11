import pandas as pd
import os
from typing import Optional


class FileHelper:
    """
    Clase auxiliar para manejar la carga y guardado de archivos CSV.
    """

    def __init__(self):
        # El constructor ahora no toma argumentos.
        pass

    def load_csv(self, file_path: str, file_name: str) -> pd.DataFrame:
        """
        Carga un archivo CSV en un DataFrame de pandas, respetando los tipos de datos originales.

        Args:
            file_path (str): Ruta al directorio del archivo.
            file_name (str): Nombre del archivo.

        Returns:
            pd.DataFrame: El DataFrame cargado.

        Raises:
            FileNotFoundError: Si el archivo no existe.
        """
        full_path = os.path.join(file_path, file_name)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"El archivo no existe: {full_path}")

        # Carga el CSV, sin inferir tipos de datos automáticamente.
        df = pd.read_csv(full_path, dtype={
            'Open time': 'int64',
            'Close time': 'int64',
            'Open': 'float64',
            'High': 'float64',
            'Low': 'float64',
            'Close': 'float64',
            'Volume': 'float64',
            'Quote asset volume': 'float64',
            'Number of trades': 'Int64',
            'Taker buy base asset volume': 'float64',
            'Taker buy quote asset volume': 'float64',
            'Ignore': 'Int64',
            'Variation': 'float64'
        }, parse_dates=['Open time_date', 'Close time_date'])
        print(f"Datos cargados desde {full_path}")
        return df

    def save_csv(self, df: pd.DataFrame, file_path: str, file_name: Optional[str] = None, prefix: str = ""):
        """
        Guarda un DataFrame en un archivo CSV.

        Args:
            df (pd.DataFrame): DataFrame a guardar.
            file_path (str): Ruta al directorio donde se guardará el archivo.
            file_name (str, optional): Nombre del archivo. Si es None, se genera uno.
            prefix (str, optional):  Prefijo para el nombre del archivo (si se genera).

        Raises:
            ValueError: Si el df es None, o si file_name es None y no se puede construir.
        """
        if df is None:
            raise ValueError("No se puede guardar un DataFrame vacío.")

        if file_name is None:
            raise ValueError("Se debe proporcionar un nombre de archivo")
        else:
            full_output_path = os.path.join(file_path, file_name)


        if not os.path.exists(file_path):
            os.makedirs(file_path)

        df.to_csv(full_output_path, index=False)
        print(f"DataFrame guardado en {full_output_path}")

    