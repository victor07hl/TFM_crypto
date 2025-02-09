import requests
import time
import pandas as pd 

class data():
    def __init__(self,base_url="https://api.binance.com"):
        self.base_url = base_url

    # Function to fetch data in chunks
    def fetch_binance_data(self,symbol, interval, startTime, endTime, sleep_time):
        all_data = []
        numFragmentos = 0
        total_records = 0
        while startTime < endTime:
            try:
                url = f"{self.base_url}/api/v3/klines?symbol={symbol}&interval={interval}&startTime={startTime}&endTime={endTime}&limit={limit}"
                response = requests.get(url)
                response.raise_for_status() # Lanza una excepción si hay un error HTTP (código de estado != 200)
                data = response.json()
                if data:
                    numFragmentos += 1
                    records_in_fragment = len(data)
                    total_records += records_in_fragment
                    print(f"Fragmento {numFragmentos} obtenido: {records_in_fragment} registros. Total: {total_records}")
                    all_data.extend(data)
                    # Usar el tiempo de apertura para evitar superposiciones
                    last_open_time = data[-1][0]
                    startTime = last_open_time + 1
                    time.sleep(sleep_time) #Añadimos un tiempo de espera para evitar sobrecargar la API
                else:
                    print(f"Fragmento vacío.  Posiblemente se ha llegado al final de los datos.Total: {total_records}")
                    break
            except requests.exceptions.RequestException as e:
                print(f"Error al obtener datos: {e}")
                break  # Detener si hay un error de red
            except Exception as e: #Capturar cualquier otra excepción inesperada
                print(f"Ocurrió un error inesperado: {e}")
                break

        return all_data
    
    def save_data(self,data:pd.DataFrame,path:str):
        print('Saving data ...')
        data.to_csv(path_or_buf=path,index=False)
        print('Data Saved')

    def pull_save_data(self,symbol, interval, startTime, endTime, sleep_time,path):
        df = self.fetch_binance_data(symbol,interval,startTime,endTime,sleep_time)
        self.save_data(df,path)

    def load_data(self,path:str,header=0):
        df = pd.read_csv(path,header=header)
        return df 