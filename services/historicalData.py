from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import pytz
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import appconfig

# mt5.initialize()
# if not mt5.initialize():
#  print('Beta Tumhare Mt5 Initialize nhai hua ', mt5.last_error())

# account = 182507753
# password = "Vishalgarna@1"
# server = "Exness-MT5Trial6"

# if not mt5.login(login=account, password=password, server=server):
#  print('Ye Kya Kardiy credential Wrong de diya ', mt5.last_error())
#  quit()

Alltimframes = {
    "1m" : mt5.TIMEFRAME_M1,
    "5m" : mt5.TIMEFRAME_M5,
    "15m" : mt5.TIMEFRAME_M15,
    "30m" : mt5.TIMEFRAME_M30,
    "1h" : mt5.TIMEFRAME_H1,
    "2h" : mt5.TIMEFRAME_H2,
    "4h" : mt5.TIMEFRAME_H4,
    "1d" : mt5.TIMEFRAME_D1,
    

    
    
}

# Initialize MetaTrader 5
def getHistoricaldata(symbol, totalnoperiod , timeframe):

    time = Alltimframes[timeframe] 
    # Set time zone to UTC
    timezone = pytz.timezone("Etc/UTC")

    # Create 'datetime' object in UTC time zone
    utc_from = datetime.now()

    # Get rates starting from current time in UTC time zone
    rates = mt5.copy_rates_from(symbol, time, utc_from, totalnoperiod)
 
    # # Check if rates are retrieved
    if rates is not None and len(rates) > 0:
        return rates[:-1]
        # Create DataFrame out of the obtained data

    #     rates_frame = pd.DataFrame(rates)
    #     # Convert time in seconds into the datetime format in UTC
    #     rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s', utc=True)
    #     # Convert the time to IST
    #     rates_frame['time'] = rates_frame['time'].dt.tz_convert('Asia/Kolkata')
        
    #     # Remove the last row
    #     newdata = rates_frame[:-1]
    #     return newdata  # Return the new DataFrame without the last row
    # else:
    #     print('No rates retrieved:', mt5.last_error())

    # # Shutdown MT5 connection
    # mt5.shutdown()

# Usage example


# data = getHistoricaldata("EURUSDm" ,100, "1m")

# print(data)
