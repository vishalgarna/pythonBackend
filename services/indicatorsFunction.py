import pandas as pd
import talib as tb
from services.historicalData import getHistoricaldata
# Sample closing prices
#Convert to DataFrame

def checkkCoressOverMacd(strategies):
        symbol = strategies["orderDetails"]["symbol"]
        timeframe = strategies["timeframe"]
        type = strategies["orderDetails"]["type"]
        data = getHistoricaldata(symbol=symbol, totalnoperiod=100 , timeframe=timeframe)
        # Calculate MACD using talib
        macd, signal, hist = tb.MACD(data['last'], fastperiod=12, slowperiod=26, signalperiod=9)
        # Extract and print the latest MACD and Signal values
        newmacd = macd[-1]
        newsinal = signal[-1]
        
        # Check for crossover

        if(type == "BUY"):
          if newmacd > newsinal:
            return True

        if(type == "SELL"):
           if (newmacd < newsinal):
            return True   

        else:
           return False
