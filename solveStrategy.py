import os, sys
import pandas as pd
import talib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from demo import evaluate_strategy
from services.indicatorsFunction import checkkCoressOverMacd
from services.historicalData import getHistoricaldata
from datetime import datetime
from openpyxl import load_workbook


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


def fetch_historical_data(symbol, timeframe, totalnoperiod=10000):
    data = getHistoricaldata(symbol=symbol, timeframe=timeframe, totalnoperiod=totalnoperiod)
    df = pd.DataFrame(data)
    
    df['high'] = df[['bid', 'ask', 'last']].max(axis=1)
    df['low'] = df[['bid', 'ask', 'last']].min(axis=1)
    
    df['open'] = df['last'].iloc[0]
    df['close'] = df['last'].iloc[-1]
    
    return df

def evaluate_trade(historical_data, strategy):
    return evaluate_strategy(historical_data=historical_data, strategy=strategy)

def backtest_results(strategy):
    trades = []
    position = None
    order_details = strategy["orderDetails"]
    timeframe = strategy["timeframe"]
    symbol = order_details["symbol"]
    sl_hit = 0
    tp_hit = 0
    strategycount = []
    lot_size = 0.01
    initalamount = 30
    after_trade = 30
    # position["after_trade"] = 30tradet_



    historical_data = fetch_historical_data(symbol, timeframe)

    for i in range(len(historical_data)):
        if(after_trade <= 0):
            break
        data = historical_data.iloc[:i + 1]
        result = evaluate_trade(historical_data=data, strategy=strategy)

        if result:
            strategycount.append(result)

            if not position:
                entry_price = historical_data["last"].iloc[i]
                time = datetime.fromtimestamp(historical_data["time"].iloc[i]).strftime("%Y-%m-%d %H-%M-%S")
                sl_tp = calculate_SL_TP(close_price=entry_price, symbol=symbol, trade_type=order_details["type"])
                position = {
                    "type": order_details["type"],
                    "entry_price": entry_price,
                    "entry_time": time,
                    "sl": sl_tp["sl"],
                    "tp": sl_tp["tp"],
                    "status": "open",
                    "pnl" : 0
                }
                # trades.append(position)
            else:
                if position["type"] == "BUY":
                    if historical_data["last"].iloc[i] <= position["sl"]:
                        loss = caculate_pnl_value(symbol=symbol , entry_price= position["entry_price"] , close_price=position["sl"] , type= "BUY")
                        position["exit_price"] = position["sl"]
                        position["status"] = "sl_hit"
                        position["pnl"] = loss
                        position["exit_time"] = datetime.fromtimestamp(historical_data["time"].iloc[i]).strftime("%Y-%m-%d %H-%M-%S")
                        sl_hit += 1
                        trades.append(position)
                        after_trade += loss
                        position = None
                    elif historical_data["last"].iloc[i] >= position["tp"]:
                        profit = caculate_pnl_value(symbol=symbol , entry_price= position["entry_price"] , close_price=position["tp"] ,type= "BUY")
                        position["exit_price"] = position["tp"]
                        position["pnl"] = profit
                        position["status"] = "tp_hit"
                        position["exit_time"] = datetime.fromtimestamp(historical_data["time"].iloc[i]).strftime("%Y-%m-%d %H-%M-%S")
                        tp_hit += 1
                        trades.append(position)
                        after_trade += profit
                        position = None
                elif position["type"] == "SELL":
                    if historical_data['last'].iloc[i] >= position["sl"]:
                        loss = caculate_pnl_value(symbol=symbol , entry_price= position["entry_price"] , close_price=position["sl"] , type= "SELL")
                        position["exit_price"] = position["sl"]
                        position["pnl"] = loss
                        position["status"] = "sl_hit"
                        position["exit_time"] = datetime.fromtimestamp(historical_data["time"].iloc[i]).strftime("%Y-%m-%d %H-%M-%S")
                        sl_hit += 1
                        trades.append(position)
                        after_trade += loss
                        position = None
                    elif historical_data['last'].iloc[i] <= position["tp"]:
                        profit = caculate_pnl_value(symbol=symbol , entry_price= position["entry_price"] , close_price=position["tp"], type= "SELL")
                        position["exit_price"] = position["tp"]
                        position["pnl"] = profit
                        position["status"] = "tp_hit"
                        position["exit_time"] = datetime.fromtimestamp(historical_data["time"].iloc[i]).strftime("%Y-%m-%d %H-%M-%S")
                        tp_hit += 1
                        trades.append(position)
                        after_trade += profit
                        position = None

    print("SL hit count:", sl_hit, "TP hit count:", tp_hit)
    print(initalamount)
    print(after_trade)
    return trades

# Example Strategy
strategy = {
    "timeframe": "4h",
    "orderDetails": {
        "symbol": "EURUSDm",
        "type": "SELL",
        "stop_loss_pct": 1.0,
        "take_profit_pct": 2.0
    },
    "entryRuleModel": [
        #   {
        #     "type": "indicator",
        #     "name": "close",
        #     "parameters": {"time period": 200}
        # },

            {
            "type": "indicator",
            "name": "SMA",
            "parameters": {"time period": 50}
        },
       
        {
            "type": "condition",
            "name": "isGreaterThan"
        },

    

           {
            "type": "indicator",
            "name": "close",
            "parameters": {"time period": 200}
        },
      
        {
            "type": "logicalOperator",
            "name": "AND"
        },
        {
            "type": "indicator",
            "name": "MACD",
            "parameters": {
                "fast period": 12,
                "slow period": 26,
                "signal period": 9
            }
        }
        #     {
        #     "type": "logicalOperator",
        #     "name": "AND"
        # },

        # {
        #     "type": "indicator",
        #     "name": "AND"
        # },


    ]
}

# Run backtest
results = backtest_results(strategy=strategy)
print("Backtest Results:", len(results))
data = pd.DataFrame(results)
print(data)


# price = caculate_pip_value(symbol="USDJPYm" , entry_price= 158.209 , close_price= 157.600 , lotsize= 100)

# print(price)