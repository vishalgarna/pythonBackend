import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backtest_function import evaluate_strategy
from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import pytz
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
    # return rates
    if rates is not None and len(rates) > 0:
        # return rates[:-1]
        # Create DataFrame out of the obtained data

        rates_frame = pd.DataFrame(rates)
        # Convert time in seconds into the datetime format in UTC
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s', utc=True)
        # Convert the time to IST
        rates_frame['time'] = rates_frame['time'].dt.tz_convert('Asia/Kolkata')
        
        # Remove the last row
        # newdata = rates_frame[:-1]
        # print(rates_frame)
        data = rates_frame.iloc[:-1]
        # print(data)
        return data   # Return the new DataFrame without the last row
    else:
        print('No rates retrieved:', mt5.last_error())

    # # Shutdown MT5 connection
    # mt5.shutdown()

# Usage example


# data = getHistoricaldata("EURUSDm" ,100, "4h")





def caculate_pnl_value (symbol , entry_price , close_price , type ):

    if type == "SELL":
        if "JPY" in symbol:
            price = entry_price - close_price
            return round( (price * 0.063478 ) * 100)
        
        elif "DXY" in symbol:
            price = entry_price - close_price
            return round( (price * 0.1000 ) * 100)

        secondprice = entry_price - close_price  
        # print (secondprice)
     
        return round((secondprice * 0.1000) * 10000)
    elif type == "BUY":
        if "JPY" in symbol:
            price = close_price - entry_price  
            return round( (price * 0.063478 ) * 100)
        
        elif "DXY" in symbol:
            price = close_price - entry_price  
            return round( (price * 0.1000 ) * 100)

        secondprice = close_price - entry_price    
        # print (secondprice)
     
        return round((secondprice * 0.1000) * 10000)
    

def calculate_SL_TP(close_price, symbol, trade_type ):
    if "JPY" in symbol:
        if trade_type == "BUY":
            sl = close_price - 0.600
            tp = close_price + 1.00
        elif trade_type == "SELL":
            sl = close_price + 0.600
            tp = close_price - 1.00
    else:
        if trade_type == "BUY":
            sl = close_price - 0.00600
            tp = close_price + 0.01500
        elif trade_type == "SELL":
            sl = close_price + 0.00600
            tp = close_price - 0.01000
        else:
            raise ValueError("Invalid trade type")

    return {"sl": sl, "tp": tp}
def evaluate_trade(historical_data, strategy , symbol):
    return evaluate_strategy(historicaldata=historical_data, strategy=strategy ,symbol= symbol)

# def backtest_results(strategy , symbol):
#     trades = []
#     position = None
#     order_details = strategy["orderDetails"]
#     timeframe = strategy["timeframe"]
#     # symbol = order_details["symbol"]
#     sl_hit = 0
#     tp_hit = 0
#     initalamount = 30
#     after_trade = 30
#     # position["after_trade"] = 30tradet_

#     historical_data = getHistoricaldata(symbol=symbol, timeframe=timeframe, totalnoperiod=10000)
#     # print(historical_data)
#     for i in range(len(historical_data)):
#             data = historical_data.iloc[:i + 1]
#             result = evaluate_trade(historical_data=data, strategy=strategy , symbol =symbol)

#             if result:
#                 if not position:
#                     entry_price = historical_data["last"].iloc[i]
#                     time = historical_data["time"].iloc[i]
#                     sl_tp = calculate_SL_TP(close_price=entry_price, symbol=symbol, trade_type=order_details["type"])
#                     position = {
#                         "type": order_details["type"],
#                         "entry_price": entry_price,
#                         "entry_time": time,
#                         "sl": sl_tp["sl"],
#                         "tp": sl_tp["tp"],
#                         "status": "open",
#                         "pnl" : 0
#                     }
#                     # trades.append(position)
#                 else:
#                     if position["type"] == "BUY":
#                         if historical_data["last"].iloc[i] <= position["sl"]:
#                             loss = caculate_pnl_value(symbol=symbol , entry_price= position["entry_price"] , close_price=position["sl"] , type= "BUY")
#                             position["exit_price"] = position["sl"]
#                             position["status"] = "sl_hit"
#                             position["pnl"] = loss
#                             position["exit_time"] = time
#                             sl_hit += 1
#                             trades.append(position)
#                             after_trade += loss
#                             position = None
#                         elif historical_data["last"].iloc[i] >= position["tp"]:
#                             profit = caculate_pnl_value(symbol=symbol , entry_price= position["entry_price"] , close_price=position["tp"] ,type= "BUY")
#                             position["exit_price"] = position["tp"]
#                             position["pnl"] = profit
#                             position["status"] = "tp_hit"
#                             position["exit_time"] = time
#                             tp_hit += 1
#                             trades.append(position)
#                             after_trade += profit
#                             position = None
#                     elif position["type"] == "SELL":
#                         if historical_data['last'].iloc[i] >= position["sl"]:
#                             loss = caculate_pnl_value(symbol=symbol , entry_price= position["entry_price"] , close_price=position["sl"] , type= "SELL")
#                             position["exit_price"] = position["sl"]
#                             position["pnl"] = loss
#                             position["status"] = "sl_hit"
#                             position["exit_time"] = time
#                             sl_hit += 1
#                             trades.append(position)
#                             after_trade += loss
#                             position = None
#                         elif historical_data['last'].iloc[i] <= position["tp"]:
#                             profit = caculate_pnl_value(symbol=symbol , entry_price= position["entry_price"] , close_price=position["tp"], type= "SELL")
#                             position["exit_price"] = position["tp"]
#                             position["pnl"] = profit
#                             position["status"] = "tp_hit"
#                             position["exit_time"] = time
#                             trades.append(position)
#                             after_trade += profit
#                             position = None

#     # print("SL hit count:", sl_hit, "TP hit count:", tp_hit)
#     # print(initalamount)
#     # print(after_trade)
#     totaltrades = len(trades)
#     data = {
#         "initalamount":initalamount,
#         "after_trade" : after_trade,
#         "sl_hit" : sl_hit,
#         "tp_hit": tp_hit, 
#            "totaltrades" : totaltrades   }
#     # print(data)
#     return data

def backtest_results(strategy, symbol):
    trades = []
    position = None
    order_details = strategy["orderDetails"]
    timeframe = strategy["timeframe"]
    sl_hit = 0
    tp_hit = 0
    initalamount = 30
    after_trade = 30

    historical_data = getHistoricaldata(symbol=symbol, timeframe=timeframe, totalnoperiod=10000)
    for i in range(len(historical_data)):
        data = historical_data.iloc[:i + 1]
        if(after_trade <=0):
             totaltrades = len(trades)
             data = {
                    "initialAmount": initalamount,
                    "afterTrade": after_trade,
                    "slHit": sl_hit,
                    "tpHit": tp_hit,
                    "totalTrades": totaltrades
                                                 }
             return data
           
        result = evaluate_trade(historical_data=data, strategy=strategy, symbol=symbol)
        # print(result)

        if result:
            if not position:
                entry_price = historical_data["last"].iloc[i]
                time = historical_data["time"].iloc[i]
                sl_tp = calculate_SL_TP(close_price=entry_price, symbol=symbol, trade_type=order_details["type"])
                position = {
                    "type": order_details["type"],
                    "entry_price": entry_price,
                    "entry_time": time,
                    "sl": sl_tp["sl"],
                    "tp": sl_tp["tp"],
                    "status": "open",
                    "pnl": 0
                }
            else:
                if position["type"] == "BUY":
                    if historical_data["last"].iloc[i] <= position["sl"]:
                        loss = caculate_pnl_value(symbol=symbol, entry_price=position["entry_price"], close_price=position["sl"], type="BUY")
                        position["exit_price"] = position["sl"]
                        position["status"] = "sl_hit"
                        position["pnl"] = loss
                        position["exit_time"] = time
                        sl_hit += 1
                        trades.append(position)
                        after_trade += loss
                        position = None
                    elif historical_data["last"].iloc[i] >= position["tp"]:
                        profit = caculate_pnl_value(symbol=symbol, entry_price=position["entry_price"], close_price=position["tp"], type="BUY")
                        position["exit_price"] = position["tp"]
                        position["pnl"] = profit
                        position["status"] = "tp_hit"
                        position["exit_time"] = time
                        tp_hit += 1
                        trades.append(position)
                        after_trade += profit
                        position = None
                elif position["type"] == "SELL":
                    if historical_data['last'].iloc[i] >= position["sl"]:
                        loss = caculate_pnl_value(symbol=symbol, entry_price=position["entry_price"], close_price=position["sl"], type="SELL")
                        position["exit_price"] = position["sl"]
                        position["pnl"] = loss
                        position["status"] = "sl_hit"
                        position["exit_time"] = time
                        sl_hit += 1
                        trades.append(position)
                        after_trade += loss
                        position = None
                    elif historical_data['last'].iloc[i] <= position["tp"]:
                        profit = caculate_pnl_value(symbol=symbol, entry_price=position["entry_price"], close_price=position["tp"], type="SELL")
                        position["exit_price"] = position["tp"]
                        position["pnl"] = profit
                        position["status"] = "tp_hit"
                        position["exit_time"] = time
                        tp_hit += 1
                        trades.append(position)
                        after_trade += profit
                        position = None

    totaltrades = len(trades)
    data = {
        "initialAmount": initalamount,
        "afterTrade": after_trade,
        "slHit": sl_hit,
        "tpHit": tp_hit,
        "totalTrades": totaltrades
    }
    # print("xvcb",data)
    return data






# price = caculate_pip_value(symbol="USDJPYm" , entry_price= 158.209 , close_price= 157.600 , lotsize= 100)

# EvaluteBacktestResult(strategy=strategy)
# print(price)