# CryptoEDA.py
import pandas as pd
import numpy as np
from typing import Optional

class CryptoEDA:
    """
    Clase para realizar Análisis Exploratorio de Datos (EDA) en datos de criptomonedas.
    Recibe un DataFrame y lo procesa.

    Args:
        data (pd.DataFrame): DataFrame de pandas con los datos.

    Attributes:
        df (pd.DataFrame): DataFrame que contiene los datos.

    """

    def __init__(self, data: pd.DataFrame):
        if not isinstance(data, pd.DataFrame):
            raise TypeError("`data` debe ser un DataFrame de pandas.")
        self.df = data.copy()  # Siempre trabaja sobre una copia

    def _create_cyclic_features(self, column_name: str, period: int, prefix: str) -> None:
        """
        Crea variables cíclicas (seno y coseno) a partir de una columna de tiempo.

        Args:
            column_name (str): Nombre de la columna de tipo datetime.  String, NO la columna.
            period (int): Periodo de la característica cíclica (ej: 24 para horas, 7 para días).
            prefix (str): Prefijo para los nombres de las nuevas columnas.
        """
        # Usa directamente el nombre de la columna (string)
        self.df[f"{prefix}_sin"] = np.sin(2 * np.pi * self.df[column_name] / period)
        self.df[f"{prefix}_cos"] = np.cos(2 * np.pi * self.df[column_name] / period)

    def _preprocess_data(self) -> None:
        """
        Realiza el preprocesamiento del DataFrame. Método privado.
        """

        # Conversión a datetime
        self.df["Open time_date"] = pd.to_datetime(self.df["Open time_date"])
        self.df["Close time_date"] = pd.to_datetime(self.df["Close time_date"])

        # Elimina la primera fila
        self.df = self.df.iloc[1:]

        # Filtra filas y elimina columnas
        # CORRECCIÓN:  Mantener filas donde Ignore == 0 (o equivalentemente, eliminar donde Ignore != 0)
        self.df.describe()
        
        self.df = self.df[self.df["Ignore"] == 0]  # Mantener las filas correctas
        self.df = self.df.drop(
            columns=["Ignore", "Close time", "Open time", "Variation"]
        )


        # Reinicia el índice
        self.df = self.df.reset_index(drop=True)

        # Extrae hora, día de la semana y mes en nuevas columnas.  ¡IMPORTANTE!
        self.df["hour"] = self.df["Close time_date"].dt.hour
        self.df["weekday"] = self.df["Close time_date"].dt.weekday
        self.df["month"] = self.df["Close time_date"].dt.month

        # Crea variables cíclicas (usando el nuevo método, y pasando STRINGS)
        self._create_cyclic_features("hour", 24, "hour")
        self._create_cyclic_features("weekday", 7, "weekday")
        self._create_cyclic_features("month", 12, "month")


        self.df = self.df.drop(columns=["Open time_date", "Close time_date"])

        # Crea la variable objetivo
        self.df["Target"] = self.df["Close"].shift(-1)
        self.df.dropna(inplace=True)  #Elimina los nulos resultantes de Target

    def apply_eda(self) -> pd.DataFrame:
        """
        Aplica el proceso completo de EDA.

        Returns:
            pd.DataFrame: El DataFrame procesado.
        """
        self._preprocess_data()
        return self.df

    def get_dataframe(self) -> pd.DataFrame:
        """
        Devuelve el DataFrame (procesado o sin procesar, según el estado actual).

        Returns:
            pd.DataFrame: El DataFrame interno.
        """
        return self.df