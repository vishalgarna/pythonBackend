import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv("data.csv")
prices = data['last']

# Fit ARIMA model
model = ARIMA(prices, order=(5,1,0))
model_fit = model.fit()

# Forecast
forecast = model_fit.get_forecast(steps=10)
forecast_values = forecast.predicted_mean
conf_int = forecast.conf_int()

# Plot results
plt.figure(figsize=(12,6))
plt.plot(prices, label='Historical Prices')
plt.plot(np.arange(len(prices), len(prices) + 10), forecast_values, label='Forecasted Prices', color='red')
plt.fill_between(np.arange(len(prices), len(prices) + 10), conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='pink', alpha=0.3)
plt.title('Stock Price Forecasting Using ARIMA')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()
