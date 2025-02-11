# BinanceUtil.py
import requests
import datetime
import time
import os
import pandas as pd
from IPython.display import clear_output, display
from typing import List, Optional


class BinanceUtil:
    """
    Clase para obtener y procesar datos históricos de K-lines (velas) de la API de Binance.
    NO se encarga de la gestión de archivos.
    """

    def __init__(self, symbol: str, base_url: str = "https://api.binance.com", request_sleep_time: float = 0.25) -> None:
        """
        Inicializa la clase BinanceUtil.

        Args:
            symbol (str): Símbolo de trading (ej: "PEPEUSDT", "BTCUSDT").
            base_url (str, optional):  URL base de la API de Binance.
            request_sleep_time (float, optional): Tiempo de espera entre requests.
        """
        self._base_url: str = base_url
        self._request_sleep_time: float = request_sleep_time
        self.symbol: str = symbol
        # Ahora solo se usa para almacenar temporalmente
        self.data_frame: Optional[pd.DataFrame] = None
        self._kline_column_names: List[str] = [
            "Open time", "Open", "High", "Low", "Close", "Volume",
            "Close time", "Quote asset volume", "Number of trades",
            "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"
        ]

    def _fetch_klines(self, interval: str, start_time_ms: int, end_time_ms: int, request_limit: int = 500) -> List[List]:
        # (Código del método _fetch_klines sin cambios - igual que antes)
        all_kline_data: List[List] = []
        num_fragments: int = 0
        total_records: int = 0

        while start_time_ms < end_time_ms:
            clear_output(wait=True)  # Clear output in interactive environments
            try:
                request_url: str = (f"{self._base_url}/api/v3/klines?symbol={self.symbol}&interval={interval}"
                                    f"&startTime={start_time_ms}&endTime={end_time_ms}&limit={request_limit}")
                response: requests.Response = requests.get(request_url)
                response.raise_for_status()  # Lanza excepción si hay error HTTP
                kline_data: List[List] = response.json()

                if kline_data:
                    num_fragments += 1
                    records_in_fragment: int = len(kline_data)
                    total_records += records_in_fragment
                    display(
                        f"Fragmento {num_fragments} obtenido: {records_in_fragment} registros. Total: {total_records}")
                    all_kline_data.extend(kline_data)
                    last_open_time: int = kline_data[-1][0]
                    start_time_ms = last_open_time + 1  # Incrementa para la siguiente solicitud
                    # Pausa para no exceder límites de la API
                    time.sleep(self._request_sleep_time)
                else:
                    display(
                        f"Fragmento vacío. Posiblemente se llegó al final de los datos. Total: {total_records}")
                    break  # Si no hay datos, sale del bucle

            except requests.exceptions.RequestException as e:
                print(f"Error durante la solicitud a la API: {e}")
                return []  # Retorna lista vacía en caso de error
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")
                return []

        return all_kline_data

    def _process_klines(self, raw_kline_data: List[List]) -> pd.DataFrame:
        """
        (Privado) Procesa los datos de K-lines, preservando los tipos de datos originales.

        Args:
            raw_kline_data (list): Datos brutos de K-lines.

        Returns:
            pd.DataFrame: DataFrame con los datos procesados.
        """
        df: pd.DataFrame = pd.DataFrame(
            raw_kline_data, columns=self._kline_column_names)

        # Convierte las columnas de tiempo a datetime64[ns]
        df['Open time_date'] = pd.to_datetime(df['Open time'], unit='ms')
        df['Close time_date'] = pd.to_datetime(df['Close time'], unit='ms')

        #  Convierte las columnas numéricas a sus tipos correctos, *manteniendo los tipos originales*.
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume',
                           'Taker buy base asset volume', 'Taker buy quote asset volume']
        for col in numeric_columns:
            # Convertir a numérico, 'coerce' convierte errores a NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['Number of trades'] = pd.to_numeric(
            df['Number of trades'], errors='coerce', downcast='integer')
        df['Ignore'] = pd.to_numeric(
            df['Ignore'], errors='coerce', downcast='integer')

        # Calcula la variación *después* de la conversión numérica.
        df['Variation'] = df['Close'].diff()

        # Reordena las columnas
        column_order: List[str] = [
            "Open time_date", "Close time_date", "Open time", "Close time", "Open",
            "High", "Low", "Close", "Variation", "Volume", "Quote asset volume",
            "Number of trades", "Taker buy base asset volume",
            "Taker buy quote asset volume", "Ignore"
        ]
        df = df[column_order]

        self.data_frame = df
        return df

    def get_historical_data(self, interval: str, start_time: datetime.datetime, end_time: datetime.datetime, request_limit: int = 500) -> Optional[pd.DataFrame]:
        """
        Obtiene, procesa y  retorna los datos históricos de K-lines.

        Args:
            interval (str): Intervalo de las velas (ej, "1h", "1d").
            start_time (datetime.datetime): Fecha y hora de inicio.
            end_time (datetime.datetime): Fecha y hora de fin.
            request_limit (int, optional): Máximo de K-lines por solicitud.

        Returns:
            Optional[pd.DataFrame]: DataFrame procesado, o None si hay error.
        """
        start_time_ms: int = int(start_time.timestamp() * 1000)
        end_time_ms: int = int(end_time.timestamp() * 1000)

        raw_kline_data: List[List] = self._fetch_klines(
            interval, start_time_ms, end_time_ms, request_limit)
        if not raw_kline_data:
            return None

        processed_df: pd.DataFrame = self._process_klines(raw_kline_data)
        return processed_df

    def get_dataframe(self) -> Optional[pd.DataFrame]:
        """Devuelve el dataframe, si existe."""
        return self.data_frame
