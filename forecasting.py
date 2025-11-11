import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Desactiva advertencias de Prophet (opcional)
import logging
logging.getLogger('prophet').setLevel(logging.ERROR)
logging.getLogger('cmdstanpy').setLevel(logging.ERROR)

def hacer_forecast(ticker, dias_a_predecir=365, anios_historial=4):
    """
    Descarga datos de una cripto y genera un forecast con Prophet.
    """
    print(f"\n--- Procesando: {ticker} ---")
    
    # 1. OBTENER DATOS
    end_date = pd.Timestamp.today()
    start_date = end_date - pd.DateOffset(years=anios_historial)
    
    try:
        # auto_adjust=True es el default y nos da la columna 'Close' ajustada
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.empty:
            print(f"No se encontraron datos para {ticker}.")
            return
            
        # 2. PREPARAR DATOS PARA PROPHET (SECCIÓN MODIFICADA)
        # 
        # En lugar de copiar y usar 'rename', creamos un
        # DataFrame nuevo y limpio con los nombres de columna 
        # que Prophet espera ('ds' y 'y').
        # Esto evita los bugs de 'rename' en Python 3.13.
        #
        data_prophet = pd.DataFrame({
            'ds': pd.to_datetime(data.index), # Usamos el índice de fecha
            'y': data['Close']                # Usamos la columna 'Close'
        })

        # Esta línea ahora SÍ debería funcionar
        data_prophet = data_prophet.dropna(subset=['y'])
        
        # 3. CREAR Y ENTRENAR EL MODELO
        model = Prophet(daily_seasonality=False, weekly_seasonality=True, yearly_seasonality=True)
        
        model.fit(data_prophet)
        
        # 4. REALIZAR LA PREDICCIÓN
        future = model.make_future_dataframe(periods=dias_a_predecir)
        forecast = model.predict(future)
        
        # 5. MOSTRAR RESULTADOS
        print(f"Predicción para {ticker} en {dias_a_predecir} días:")
        print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(1))
        
        # Graficar el forecast
        fig = model.plot(forecast)
        plt.title(f'Forecast de {ticker} (Próximos {dias_a_predecir} días)')
        plt.xlabel('Fecha')
        plt.ylabel('Precio (USD)')
        plt.show(block=True) 

    except Exception as e:
        print(f"Error inesperado procesando {ticker}: {type(e).__name__} - {e}")
        import traceback
        traceback.print_exc() # Imprime el error detallado

# --- EJECUCIÓN PRINCIPAL ---
lista_de_criptos = [
    'BTC-USD',
    'ETH-USD',
    'SOL-USD',
    'XRP-USD'
]

for cripto_ticker in lista_de_criptos:
    hacer_forecast(cripto_ticker, dias_a_predecir=90) 

print("\n--- Análisis completado ---")