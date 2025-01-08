import pandas as pd
import talib as tb

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.historicalData import getHistoricaldata

# Sample closing prices
#Convert to DataFrame
def checkkCoressOverMacd(strategies, data):
    # print(data)
    symbol = strategies["orderDetails"]["symbol"]
    timeframe = strategies["timeframe"]
    type = strategies["orderDetails"]["type"]
    # data = getHistoricaldata(symbol=symbol, totalnoperiod=100, timeframe=timeframe)
    
    # Calculate MACD using talib
    if data is None or data.size == 0:
        print('data is empty')
        return False
    
    macd, signal, hist = tb.MACD(data['last'], fastperiod=12, slowperiod=26, signalperiod=9)
    # Extract and print the latest MACD and Signal values
    newmacd = macd.iloc[-1]
    newsinal = signal.iloc[-1]
    
    # Check for crossover
    if type == "BUY":
        if newmacd > newsinal:
            return True
    elif type == "SELL":
        if newmacd < newsinal:
            return True
    
    return False

        
class LogicalOperator:
    def __init__(self, name):
        self.name = name

    def evaluate(self, conditions):
        print(f"Evaluating Logical Operator: {self.name} with Conditions: {conditions}")  # Debug print
        if self.name == 'AND':
            return all(conditions)
        elif self.name == 'OR':
            return any(conditions)
        else:
            raise ValueError(f"Unknown logical operator: {self.name}")






class Condition:
    def __init__(self, name):
        self.name = name

    def evaluate(self, values):
        if self.name == 'isGreaterThan':
            return values[0] > values[1]
        elif self.name == 'isLessThan':
            return values[0] < values[1]
        else:
            raise ValueError(f"Unknown condition: {self.name}")

import pandas as pd
import talib

# Indicator functions
def calculate_sma(historical_data, time_period):
    closing_prices = historical_data['last']
    return talib.SMA(closing_prices, timeperiod=time_period)

def calculate_ema(historical_data, time_period):
    closing_prices = historical_data['last']
    return talib.EMA(closing_prices, timeperiod=time_period)

def calculate_rsi(historical_data, time_period):
    closing_prices = historical_data['last']
    return talib.RSI(closing_prices, timeperiod=time_period)

def calculate_macd(historical_data):
    closing_prices = historical_data['last']
    macd, macd_signal, _ = talib.MACD(closing_prices)
    return macd, macd_signal

# Initialize indicators based on name
def calculate_indicator(name, historical_data, parameters=None):
    if name == 'SMA':
        return calculate_sma(historical_data, parameters['time period'])
    elif name == 'EMA':
        return calculate_ema(historical_data, parameters['time period'])
    elif name == 'RSI':
        return calculate_rsi(historical_data, parameters['time period'])
    elif name == 'MACD':
        return calculate_macd(historical_data)
    else:
        raise ValueError(f"Unknown indicator: {name}")


import pandas as pd  # Ensure Pandas is imported

def evaluate_strategy(strategy):
    print('hello from evaluate')
    print(strategy)
    indicator_values = {}
    conditions = []
    logical_ops = []
    condition_results = []

    entryCondition = strategy["entryRuleModel"]

    data = getHistoricaldata(symbol="GBPUSDm" , timeframe= "1m", totalnoperiod= 1000)
    historical_data  = pd.DataFrame(data)
    # Calculate all indicators first
    for component in entryCondition:
        if component['type'] == 'indicator':
            indicator = component['name']
            if indicator == "MACD":
                check = checkkCoressOverMacd(strategies=strategy)
                condition_results.append(check)
            value = calculate_indicator(component['name'], historical_data, component['parameters'])
            indicator_key = f"{component['name']}_{component['parameters'].get('time period', '')}"
            if value is not None:
                if isinstance(value, tuple):  # Handle multiple values (e.g., MACD)
                    indicator_values[f"{indicator_key}_value"] = value[0].iloc[-1]
                    indicator_values[f"{indicator_key}_signal"] = value[1].iloc[-1]
                else:
                    indicator_values[indicator_key] = value.iloc[-1]

    print(indicator_values)  # Debug print to see indicator values

    # Store conditions and logical operators
    i = 0
    while i < len(entryCondition):
        component = entryCondition[i]
        if component['type'] == 'condition':
            prev_indicator_key = f"{entryCondition[i-1]['name']}_{entryCondition[i-1]['parameters'].get('time period', '')}"
            next_indicator_key = f"{entryCondition[i+1]['name']}_{entryCondition[i+1]['parameters'].get('time period', '')}"
            conditions.append((component['name'], indicator_values[prev_indicator_key], indicator_values[next_indicator_key]))
        elif component['type'] == 'logicalOperator':
            logical_ops.append(component['name'])
        i += 1

    # Evaluate all conditions
    for cond in conditions:
        condition = Condition(cond[0])
        values = [cond[1], cond[2]]
        if not any(pd.isna(values)):
            result = condition.evaluate(values)
            condition_results.append(result)
        else:
            print(f"Skipping Condition due to NaN Values: {values}")  # Debug print
            condition_results.append(False)

    print("Individual Condition Results:", condition_results)  # Debug print

    # Combine conditions using logical operators
    if logical_ops:
        conditions_met = condition_results[0]
        for j, logical_op in enumerate(logical_ops):
            # Check if j+1 is within bounds of condition_results
            if j + 1 < len(condition_results):
                logical_operator = LogicalOperator(logical_op)
                conditions_met = logical_operator.evaluate([conditions_met, condition_results[j+1]])
            else:
                print(f"Skipping logical operator {logical_op} due to insufficient condition results.")  # Debug print
                break
    else:
        conditions_met = condition_results[0]

    print(conditions_met)  # Final result print

    return conditions_met


strategy = {
    # "_id": ObjectId("67760af72202081b5f68c2f2"),
    # "userId": ObjectId("674f044539c250120a20854e"),
    "strategyName": "new Strategy",
    "timeframe": "1m",
    "description": "This is testing",
    "deployed": True,
    "entryRuleModel": [
        {
            "type": "indicator",
            "name": "SMA",
            "parameters": {
                "time period": 50
            }
        },
        {
            "type": "condition",
            "name": "isGreaterThan"
        },
        {
            "type": "indicator",
            "name": "SMA",
            "parameters": {
                "time period": 200
            }
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
    ],
    "exitRuleModel": [
        {
            "indicatorId": "ccea0bcee2",
            "condition": "",
            "value": "a171f27903",
            "action": "SELL",
            "_id": ("67760af72202081b5f68c2f3")
        }
    ],
    "orderDetails": {
        "type": "BUY",
        "symbol": "GBPUSDm",
        "volume": 2
    },
    # "createdAt": datetime.datetime(2025, 1, 2, 3, 41, 44, 38000),
    # "updatedAt": datetime.datetime(2025, 1, 2, 3, 41, 44, 38000),
    "__v": 0
}




# # restult = evaluate_strategy(strategy=strategy)

# # print(restult)


# import pandas as pd
# import talib as tb

# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from services.historicalData import getHistoricaldata

# # Sample closing prices
# #Convert to DataFrame

# def checkkCoressOverMacd(strategies , data ):
#         symbol = strategies["orderDetails"]["symbol"]
#         timeframe = strategies["timeframe"]
#         type = strategies["orderDetails"]["type"]
#         # data = getHistoricaldata(symbol=symbol, totalnoperiod=100 , timeframe=timeframe) 
#         # Calculate MACD using talib
#         if data is None or data.size == 0:
#           print('data is empty')
#           return
#         macd, signal, hist = tb.MACD(data['last'], fastperiod=12, slowperiod=26, signalperiod=9)
#         # Extract and print the latest MACD and Signal values
#         newmacd = macd[-1]
#         newsinal = signal[-1]

#         print(newmacd)
#         print(newsinal)
        
#         # Check for crossover

#         if(type == "BUY"):
#           if newmacd > newsinal:
#             return True

#         if(type == "SELL"):
#            if (newmacd < newsinal):
#             return True   

#         else:
#            return False
        



        
# class LogicalOperator:
#     def __init__(self, name):
#         self.name = name

#     def evaluate(self, conditions):
#         print(f"Evaluating Logical Operator: {self.name} with Conditions: {conditions}")  # Debug print
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

# import pandas as pd
# import talib

# # Indicator functions
# def calculate_sma(historical_data, time_period):
#     closing_prices = historical_data['last']
#     return talib.SMA(closing_prices, timeperiod=time_period)

# def calculate_ema(historical_data, time_period):
#     closing_prices = historical_data['last']
#     return talib.EMA(closing_prices, timeperiod=time_period)

# def calculate_rsi(historical_data, time_period):
#     closing_prices = historical_data['last']
#     return talib.RSI(closing_prices, timeperiod=time_period)

# def calculate_macd(historical_data):
#     closing_prices = historical_data['last']
#     macd, macd_signal, _ = talib.MACD(closing_prices)
#     return macd, macd_signal

# # Initialize indicators based on name
# def calculate_indicator(name, historical_data, parameters=None):
#     if name == 'SMA':
#         return calculate_sma(historical_data, parameters['time period'])
#     elif name == 'EMA':
#         return calculate_ema(historical_data, parameters['time period'])
#     elif name == 'RSI':
#         return calculate_rsi(historical_data, parameters['time period'])
#     elif name == 'MACD':
#         return calculate_macd(historical_data)
#     else:
#         raise ValueError(f"Unknown indicator: {name}")


# import pandas as pd  # Ensure Pandas is imported

# def evaluate_strategy(strategy):
#     print('hello from evaluate')
#     indicator_values = {}
#     conditions = []
#     logical_ops = []
#     condition_results = []

#     entryCondition = strategy["entryRuleModel"]
#     symbol = strategy["orderDetails"]["symbol"]
#     timeframe = strategy["timeframe"]



#     data = getHistoricaldata(symbol=symbol, timeframe= timeframe, totalnoperiod= 1000)
#     historical_data  = pd.DataFrame(data)
#     # Calculate all indicators first
#     for component in entryCondition:
#         if component['type'] == 'indicator':
#             indicator = component['name']
#             if indicator == "MACD":
#                 check = checkkCoressOverMacd(strategies=strategy)
#                 condition_results.append(check)
#             value = calculate_indicator(component['name'], historical_data, component['parameters'])
#             indicator_key = f"{component['name']}_{component['parameters'].get('time period', '')}"
#             if value is not None:
#                 if isinstance(value, tuple):  # Handle multiple values (e.g., MACD)
#                     indicator_values[f"{indicator_key}_value"] = value[0].iloc[-1]
#                     indicator_values[f"{indicator_key}_signal"] = value[1].iloc[-1]
#                 else:
#                     indicator_values[indicator_key] = value.iloc[-1]

#     print(indicator_values)  # Debug print to see indicator values

#     # Store conditions and logical operators
#     i = 0
#     while i < len(entryCondition):
#         component = entryCondition[i]
#         if component['type'] == 'condition':
#             prev_indicator_key = f"{entryCondition[i-1]['name']}_{entryCondition[i-1]['parameters'].get('time period', '')}"
#             next_indicator_key = f"{entryCondition[i+1]['name']}_{entryCondition[i+1]['parameters'].get('time period', '')}"
#             conditions.append((component['name'], indicator_values[prev_indicator_key], indicator_values[next_indicator_key]))
#         elif component['type'] == 'logicalOperator':
#             logical_ops.append(component['name'])
#         i += 1

#     # Evaluate all conditions
#     for cond in conditions:
#         condition = Condition(cond[0])
#         values = [cond[1], cond[2]]
#         if not any(pd.isna(values)):
#             result = condition.evaluate(values)
#             condition_results.append(result)
#         else:
#             print(f"Skipping Condition due to NaN Values: {values}")  # Debug print
#             condition_results.append(False)

#     print("Individual Condition Results:", condition_results)  # Debug print

#     # Combine conditions using logical operators
#     if logical_ops:
#         conditions_met = condition_results[0]
#         for j, logical_op in enumerate(logical_ops):
#             # Check if j+1 is within bounds of condition_results
#             if j + 1 < len(condition_results):
#                 logical_operator = LogicalOperator(logical_op)
#                 conditions_met = logical_operator.evaluate([conditions_met, condition_results[j+1]])
#             else:
#                 print(f"Skipping logical operator {logical_op} due to insufficient condition results.")  # Debug print
#                 break
#     else:
#         conditions_met = condition_results[0]

#     print(conditions_met)  # Final result print

#     return conditions_met


# strategy = {
#     # "_id": ObjectId("67760af72202081b5f68c2f2"),
#     # "userId": ObjectId("674f044539c250120a20854e"),
#     "strategyName": "new Strategy",
#     "timeframe": "1m",
#     "description": "This is testing",
#     "deployed": True,
#     "entryRuleModel": [
#         {
#             "type": "indicator",
#             "name": "SMA",
#             "parameters": {
#                 "time period": 50
#             }
#         },
#         {
#             "type": "condition",
#             "name": "isGreaterThan"
#         },
#         {
#             "type": "indicator",
#             "name": "SMA",
#             "parameters": {
#                 "time period": 200
#             }
#         },
#         {
#             "type": "logicalOperator",
#             "name": "AND"
#         },
#         {
#             "type": "indicator",
#             "name": "MACD",
#             "parameters": {
#                 "fast period": 12,
#                 "slow period": 26,
#                 "signal period": 9
#             }
#         }
#     ],
#     "exitRuleModel": [
#         {
#             "indicatorId": "ccea0bcee2",
#             "condition": "",
#             "value": "a171f27903",
#             "action": "SELL",
#             "_id": ("67760af72202081b5f68c2f3")
#         }
#     ],
#     "orderDetails": {
#         "type": "BUY",
#         "symbol": "GBPUSDm",
#         "volume": 2
#     },
#     # "createdAt": datetime.datetime(2025, 1, 2, 3, 41, 44, 38000),
#     # "updatedAt": datetime.datetime(2025, 1, 2, 3, 41, 44, 38000),
#     "__v": 0
# }


# # strategy = {
# #  'timeframe': '1h',
# #    'deployed': True,
# #      'orderDetails': {'symbol': 'DXYm', 'type': 'BUY'}, '__v': 0}

# # result = checkkCoressOverMacd(strategies= strategy)

# # print(result)


# # restult = evaluate_strategy(strategy=strategy)

# # print(restult)