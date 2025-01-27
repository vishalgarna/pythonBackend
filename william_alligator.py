import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load your data
data = pd.read_csv('data.csv')

def calculate_sma(data, period):
    return data['last'].rolling(window=period, min_periods=period).mean()

# print(data["last"])
jaw = calculate_sma(data, 13)
teeth = calculate_sma(data, 8)
lips = calculate_sma(data, 5)

plt.figure(figsize=(14, 7))
plt.plot(data['time'], jaw, label='Jaw (Blue Line)')
plt.plot(data['time'], teeth, label='Teeth (Red Line)')
plt.plot(data['time'], lips, label='Lips (Green Line)')
plt.plot(data["time"] , data["last"])
plt.title('William Alligator Indicator')
plt.xlabel('time')
plt.ylabel('Price')
plt.legend()
plt.show()
