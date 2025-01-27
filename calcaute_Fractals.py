import pandas as pd
import numpy as np
from services.historicalData import getHistoricaldata

# Load your data
data = pd.read_csv('data.csv')

def identify_fractals():

    data = getHistoricaldata("EURUSDm" , 100, "1d")
    high = data["bid"]
    low = data["ask"]
    period = 9

    type = "BUY"

    bullish_fractals = [np.nan] * len(high)
    bearish_fractals = [np.nan] * len(high)
    
    for i in range(period, len(high) - period):
        if (high[i] > max(high[i - period:i]) and high[i] > max(high[i + 1:i + period + 1])):
            bearish_fractals[i] = high[i]
        
        if (low[i] < min(low[i - period:i]) and low[i] < min(low[i + 1:i + period + 1])):
            bullish_fractals[i] = low[i]

    bullish_fractals_slice = bullish_fractals[-1]  
    bearish_fractals_slice  = bearish_fractals[-1]    
    print(bullish_fractals_slice)
    print(bearish_fractals_slice) 
    # print(bullish_fractals)
    # print(bearish_fractals)
    if type == "BUY":
        if np.isnan(bullish_fractals_slice):
            return False
        else:
            print("bullish" , bullish_fractals_slice)
            return True

    if type == "SELL":
        if np.isnan(bearish_fractals_slice ):
            
            return False
            
        else:
            print("bearish", bearish_fractals_slice)
            return True






