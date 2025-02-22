from pywt import wavedec, upcoef
import plotly.graph_objects as go
import numpy as np


class common_functions():
    def __init__(self):
        pass

    def get_wt_coeff_inv(self,signal,wavelet,level,mode,take=None):
        take = len(signal) if take == None else take
        coeffs = wavedec(signal,wavelet=wavelet,level=level,mode=mode)
        coeffs_taggged = {}
        inv_coeffs_tagged = {}
        for i in range(0,level):
            if i == 0:
                coeffs_taggged.update({f'cA{level-i}':coeffs[i]})
                coeffs_taggged.update({f'cD{level-i}':coeffs[i+1]})
                inv_coeffs_tagged.update({f'cA{level-i}':upcoef('a',coeffs[i],wavelet,level,take)})
                inv_coeffs_tagged.update({f'cD{level-i}':upcoef('d',coeffs[i+1],wavelet,level,take)})

            else:
                coeffs_taggged.update({f'cD{level-i}':coeffs[i+1]})
                inv_coeffs_tagged.update({f'cD{level-i}':upcoef('d',coeffs[i+1],wavelet,level,take)})
        return coeffs_taggged,inv_coeffs_tagged
    

    def plot_inv_wv(self,inv_coeffs,date_signal,external_signals=None,output_path=None):
        all_vectors = external_signals
        all_vectors.update(inv_coeffs)
        fig = go.Figure()
        for tag,inv_coeff in all_vectors.items():
            #adding trace
            fig.add_trace(go.Scatter(x=date_signal
                                    ,y=inv_coeff
                                    ,mode='lines'
                                    ,name=tag))
        fig.update_layout(
            xaxis_title="Tiempo",
            yaxis_title="Valor",
            title='Grafica de inversa de Wavelet'
        )
        fig.show()
        if output_path != None:
            fig.write_html(output_path)

    def create_sequences(self,data, window_size, target_col):
        X, y = [], []
        for i in range(len(data) - window_size):
            X.append(data.iloc[i:i+window_size])  # Ventana de entrada
            y.append(data[target_col][i+window_size])    # Valor a predecir
        return np.array(X), np.array(y)


