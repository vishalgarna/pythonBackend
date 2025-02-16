# # import pandas as pd
# # import talib 
# # import sys
# # import os
# # import logging

# # # Configure logging
# # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# # # Add current directory to sys.path
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # from services.historicalData import getHistoricaldata

# # def checkkCoressOverMacd(strategy):
# #     try:
# #         symbol = strategy["orderDetails"]["symbol"]
# #         timeframe = strategy["timeframe"]
# #         type = strategy["orderDetails"]["type"]
# #         data = getHistoricaldata(symbol=symbol, totalnoperiod=100, timeframe=timeframe)

# #         if data is None or data.size == 0:
# #             logging.warning('Data is empty')
# #             return False

# #         macd, signal, hist = talib.MACD(data['last'], fastperiod=12, slowperiod=26, signalperiod=9)
# #         newmacd = macd.iloc[-1]
# #         newsinal = signal.iloc[-1]

# #         print(newmacd)
# #         print(newsinal)

# #         if type == "BUY":
# #             return newmacd > newsinal
# #         elif type == "SELL":
# #             return newmacd < newsinal
# #         return False
# #     except Exception as e:
# #         logging.error(f"Error in checkkCoressOverMacd: {e}")
# #         return False

# # class LogicalOperator:
# #     def __init__(self, name):
# #         self.name = name

# #     def evaluate(self, conditions):
# #         logging.debug(f"Evaluating Logical Operator: {self.name} with Conditions: {conditions}")
# #         if self.name == 'AND':
# #             return all(conditions)
# #         elif self.name == 'OR':
# #             return any(conditions)
# #         else:
# #             raise ValueError(f"Unknown logical operator: {self.name}")

# # class Condition:
# #     def __init__(self, name):
# #         self.name = name

# #     def evaluate(self, values):
# #         if self.name == 'isGreaterThan':
# #             return values[0] > values[1]
# #         elif self.name == 'isLessThan':
# #             return values[0] < values[1]
# #         else:
# #             raise ValueError(f"Unknown condition: {self.name}")

# # # Indicator functions
# # def calculate_sma(historical_data, time_period):
# #     return talib.SMA(historical_data['last'], timeperiod=time_period)

# # def calculate_ema(historical_data, time_period):
# #     return talib.EMA(historical_data['last'], timeperiod=time_period)

# # def calculate_rsi(historical_data, time_period):
# #     return talib.RSI(historical_data['last'], timeperiod=time_period)

# # def calculate_macd(historical_data):
# #     return talib.MACD(historical_data['last'])

# # # Initialize indicators based on name
# # def calculate_indicator(name, credentials, parameters=None):
# #     try:
# #         historical_data = getHistoricaldata(symbol=credentials["symbol"], totalnoperiod=500, timeframe=credentials["timeframe"])
# #         print(historical_data)
# #         if name == 'SMA':
# #             return calculate_sma(historical_data, parameters['time period'])
# #         elif name == 'EMA':
# #             return calculate_ema(historical_data, parameters['time period'])
# #         elif name == 'RSI':
# #             return calculate_rsi(historical_data, parameters['time period'])
# #         elif name == 'close':
# #             return historical_data["last"]
# #     except Exception as e:
# #         logging.error(f"Error in calculate_indicator: {e}")
# #         return None

# # def evaluate_strategy(strategy):
# #     try:
# #         symbol = strategy["orderDetails"]["symbol"]
# #         timeframe = strategy["timeframe"]
# #         type = strategy["orderDetails"]["type"]
# #         Credentials = {"symbol": symbol, "timeframe": timeframe, "type": type}

# #         entryCondition = strategy["entryRuleModel"]
# #         indicator_values = {}
# #         conditions = []
# #         logical_ops = []
# #         condition_results = []

# #         for component in entryCondition:
# #             if component['type'] == 'indicator':
# #                 if component['name'] == "MACD":
# #                     check = checkkCoressOverMacd(strategy=strategy)
# #                     condition_results.append(check)
# #                 value = calculate_indicator(component['name'], Credentials, component['parameters'])
# #                 indicator_key = f"{component['name']}_{component['parameters'].get('time period', '')}"
# #                 if value is not None:
# #                     if isinstance(value, tuple):  # Handle multiple values (e.g., MACD)
# #                         indicator_values[f"{indicator_key}_value"] = value[0].iloc[-1]
# #                         indicator_values[f"{indicator_key}_signal"] = value[1].iloc[-1]
# #                     else:
# #                         indicator_values[indicator_key] = value.iloc[-1]
# #         print(indicator_values)
# #         i = 0
# #         while i < len(entryCondition):
# #             component = entryCondition[i]
# #             if component['type'] == 'condition':
# #                 prev_indicator_key = f"{entryCondition[i-1]['name']}_{entryCondition[i-1]['parameters'].get('time period', '')}"
# #                 next_indicator_key = f"{entryCondition[i+1]['name']}_{entryCondition[i+1]['parameters'].get('time period', '')}"
# #                 conditions.append((component['name'], indicator_values[prev_indicator_key], indicator_values[next_indicator_key]))
# #             elif component['type'] == 'logicalOperator':
# #                 logical_ops.append(component['name'])
# #             i += 1

# #         for cond in conditions:
# #             condition = Condition(cond[0])
# #             values = [cond[1], cond[2]]
# #             if not any(pd.isna(values)):
# #                 result = condition.evaluate(values)
# #                 condition_results.append(result)
# #             else:
# #                 logging.warning(f"Skipping Condition due to NaN Values: {values}")
# #                 condition_results.append(False)

# #         if logical_ops:
# #             conditions_met = condition_results[0]
# #             for j, logical_op in enumerate(logical_ops):
# #                 if j + 1 < len(condition_results):
# #                     logical_operator = LogicalOperator(logical_op)
# #                     conditions_met = logical_operator.evaluate([conditions_met, condition_results[j+1]])
# #                 else:
# #                     logging.warning(f"Skipping logical operator {logical_op} due to insufficient condition results.")
# #                     break
# #         else:
# #             conditions_met = condition_results[0]

# #         logging.info(f"Final condition met: {conditions_met}")
# #         return conditions_met
# #     except Exception as e:
# #         logging.error(f"Error in evaluate_strategy: {e}")
# #         return False

# # # # Sample usage (example)
# # if __name__ == "__main__":
# #     strategy = {
# #         "orderDetails": {
# #             "symbol": "USDCHFm",
# #             "type": "SELL"
# #         },
# #         "timeframe": "4h",
# #         "entryRuleModel": [
# #             {"type": "indicator", "name": "close", "parameters": {"time period": 50}},
# #             {"type": "condition", "name": "isLessThan"},
# #             {"type": "indicator", "name": "SMA", "parameters": {"time period": 50}},
# #             # {"type": "logicalOperator", "name": "AND"},
# #             # {"type": "indicator", "name": "MACD" ,"parameters": {"time period": 50}},
# #         ]
# #     }
# #     result = evaluate_strategy(strategy)
# #     print(result)



# from services.historicalData import getHistoricaldata
# import pandas as pd
# import talib 
# import sys
# import os
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# # Add current directory to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# # Configure logging


# def checkkCoressOverMacd(strategy, symbol):
#     try:
#         # symbol = strategy["orderDetails"]["symbol"]
#         timeframe = strategy["timeframe"]
#         type = strategy["orderDetails"]["type"]
#         data = getHistoricaldata(symbol=symbol, totalnoperiod=100, timeframe=timeframe)
#         print(data)

#         if data is None or data.size == 0:
#             logging.warning('Data is empty')
#             return False

#         macd, signal, hist = talib.MACD(data['last'], fastperiod=12, slowperiod=26, signalperiod=9)
#         newmacd = macd.iloc[-1]
#         newsinal = signal.iloc[-1]

#         # print(newmacd)
#         # print(newsinal)

#         if type == "BUY":
#             return newmacd > newsinal
#         elif type == "SELL":
#             return newmacd < newsinal
#         return False
#     except Exception as e:
#         logging.error(f"Error in checkkCoressOverMacd: {e}")
#         return False

# class LogicalOperator:
#     def __init__(self, name):
#         self.name = name

#     def evaluate(self, conditions):
#         logging.debug(f"Evaluating Logical Operator: {self.name} with Conditions: {conditions}")
#         if self.name == 'AND':
#             return all(conditions)
#         elif self.name == 'OR':
#             return any(conditions)
#         else:
#             raise ValueError(f"Unknown logical operator: {self.name}")

# class Condition:
#     def __init__(self, name):
#         self.name = name

#     def evaluate(self, values):
#         if self.name == 'isGreaterThan':
#             return values[0] > values[1]
#         elif self.name == 'isLessThan':
#             return values[0] < values[1]
#         else:
#             raise ValueError(f"Unknown condition: {self.name}")

# # Indicator functions
# def calculate_sma(historical_data, time_period):
#     return talib.SMA(historical_data['last'], timeperiod=time_period)

# def calculate_ema(historical_data, time_period):
#     return talib.EMA(historical_data['last'], timeperiod=time_period)

# def calculate_rsi(historical_data, time_period):
#     return talib.RSI(historical_data['last'], timeperiod=time_period)

# def calculate_macd(historical_data):
#     return talib.MACD(historical_data['last'])

# # Initialize indicators based on name
# def calculate_indicator(name, credentials, parameters=None):
#     try:
#         historical_data = getHistoricaldata(symbol=credentials["symbol"], totalnoperiod=500, timeframe=credentials["timeframe"])
#         # print(historical_data)
#         if name == 'SMA':
#             return calculate_sma(historical_data, parameters['time period'])
#         elif name == 'EMA':
#             return calculate_ema(historical_data, parameters['time period'])
#         elif name == 'RSI':
#             return calculate_rsi(historical_data, parameters['time period'])
#         elif name == 'close':
#             return historical_data["last"]
#     except Exception as e:
#         logging.error(f"Error in calculate_indicator: {e}")
#         return None

# def evaluate_strategy(strategy, symbol):
#     try:
#         # symbol = strategy["orderDetails"]["symbol"]
#         timeframe = strategy["timeframe"]
#         type = strategy["orderDetails"]["type"]
#         Credentials = {"symbol": symbol, "timeframe": timeframe, "type": type}

#         entryCondition = strategy["entryRuleModel"]
#         indicator_values = {}
#         conditions = []
#         logical_ops = []
#         condition_results = []

#         for component in entryCondition:
#             if component['type'] == 'indicator':
#                 if component['name'] == "MACD":
#                     check = checkkCoressOverMacd(strategy=strategy , symbol =symbol)
#                     condition_results.append(check)
#                 value = calculate_indicator(component['name'], Credentials, component['parameters'])
#                 indicator_key = f"{component['name']}_{component['parameters'].get('time period', '')}"
#                 if value is not None:
#                     if isinstance(value, tuple):  # Handle multiple values (e.g., MACD)
#                         indicator_values[f"{indicator_key}_value"] = value[0].iloc[-1]
#                         indicator_values[f"{indicator_key}_signal"] = value[1].iloc[-1]
#                     else:
#                         indicator_values[indicator_key] = value.iloc[-1]
#         # print(indicator_values)
#         i = 0
#         while i < len(entryCondition):
#             component = entryCondition[i]
#             if component['type'] == 'condition':
#                 prev_indicator_key = f"{entryCondition[i-1]['name']}_{entryCondition[i-1]['parameters'].get('time period', '')}"
#                 next_indicator_key = f"{entryCondition[i+1]['name']}_{entryCondition[i+1]['parameters'].get('time period', '')}"
#                 conditions.append((component['name'], indicator_values[prev_indicator_key], indicator_values[next_indicator_key]))
#             elif component['type'] == 'logicalOperator':
#                 logical_ops.append(component['name'])
#             i += 1

#         for cond in conditions:
#             condition = Condition(cond[0])
#             values = [cond[1], cond[2]]
#             if not any(pd.isna(values)):
#                 result = condition.evaluate(values)
#                 condition_results.append(result)
#             else:
#                 logging.warning(f"Skipping Condition due to NaN Values: {values}")
#                 condition_results.append(False)

#         if logical_ops:
#             conditions_met = condition_results[0]
#             for j, logical_op in enumerate(logical_ops):
#                 if j + 1 < len(condition_results):
#                     logical_operator = LogicalOperator(logical_op)
#                     conditions_met = logical_operator.evaluate([conditions_met, condition_results[j+1]])
#                 else:
#                     logging.warning(f"Skipping logical operator {logical_op} due to insufficient condition results.")
#                     break
#         else:
#             conditions_met = condition_results[0]

#         logging.info(f"Final condition met: {conditions_met}")
#         return conditions_met
#     except Exception as e:
#         logging.error(f"Error in evaluate_strategy: {e}")
#         return False


import logging
from  historicalData import getHistoricaldata
import talib
import numpy as np
from notifications_serivces import send_notification
import threading

def find_Momentum_indicator(name, Credentials):
    if name == "MACD":
        return checkkCoressOverMacd(Credentials)
    if name == "william_fractal":
        return identify_fractals(Credentials)
    else:
        return

    

def checkkCoressOverMacd(Credentials):
    try:
        symbol = Credentials["symbol"]
        timeframe = Credentials["timeframe"]
        type = Credentials["type"]
        data = getHistoricaldata(symbol=symbol, totalnoperiod=100, timeframe=timeframe)
        if data is None or data.size == 0:
            logging.warning('Data is empty')
            return False

        macd, signal, hist = talib.MACD(data['last'], fastperiod=12, slowperiod=26, signalperiod=9)
        newmacd = macd.iloc[-1]
        newsinal = signal.iloc[-1]

        print(newmacd)
        print(newsinal)

        if type == "BUY":
            return newmacd > newsinal
        elif type == "SELL":
            return newmacd < newsinal
        return False
    except Exception as e:
        logging.error(f"Error in checkkCoressOverMacd: {e}")
        return False

def identify_fractals(Credentials):
    symbol = Credentials["symbol"]
    timeframe = Credentials["timeframe"]
    type = Credentials["type"]
    data = getHistoricaldata(symbol=symbol, totalnoperiod=100, timeframe=timeframe)
    
    high = data["bid"]
    low = data["ask"]
    period = 9

    bullish_fractals = [np.nan] * len(high)
    bearish_fractals = [np.nan] * len(high)
    
    for i in range(period, len(high) - period):
        if high[i] > max(high[i - period:i]) and high[i] > max(high[i + 1:i + period + 1]):
            bearish_fractals[i] = high[i]
        
        if low[i] < min(low[i - period:i]) and low[i] < min(low[i + 1:i + period + 1]):
            bullish_fractals[i] = low[i]

    bullish_fractals_slice = bullish_fractals[-1]
    bearish_fractals_slice = bearish_fractals[-1]
    
    print(bullish_fractals_slice)
    print(bearish_fractals_slice)
    
    result = False

    if type == "BUY":
        if not np.isnan(bullish_fractals_slice):
            result = True
            threading.Thread(target=send_notification, args=("Attention Vishal", f"bullishFractal aaya hai iss symbol ka {symbol}")).start()
    elif type == "SELL":
        if not np.isnan(bearish_fractals_slice):
            result = True
            threading.Thread(target=send_notification, args=("Attention Vishal", f"bearishFractal aaya hai iss symbol ka {symbol}")).start()

    return result
