import os , sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__) , '..')))

from services.indicatorsFunction import checkkCoressOverMacd
from services.historicalData import getHistoricaldata
import MetaTrader5 as mt5



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
from services.placeOrderServices import placedOrder

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
    elif name == 'close':
        # symbol = parameters["symbol"]
        # timeframe = parameters["timeframe"]
        # data  = getHistoricaldata(symbol=symbol , totalnoperiod= 5 , timeframe=timeframe )
        data = historical_data["last"]
        return data
    else:
        return
        

# Condition evaluation
def evaluate_condition(name, values):
    # print(f"Evaluating Condition: {name} with Values: {values}")  # Debug print
    if name == 'isGreaterThan':
        return values[0] > values[1] if not any(pd.isna(values)) else False
    elif name == 'isLessThan':
        return values[0] < values[1] if not any(pd.isna(values)) else False
    else:
        raise ValueError(f"Unknown condition: {name}")

# Logical operation
class LogicalOperator:
    def __init__(self, name):
        self.name = name

    def evaluate(self, conditions):
        # print(f"Evaluating Logical Operator: {self.name} with Conditions: {conditions}")  # Debug print
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
        return evaluate_condition(self.name, values)
    



def evaluate_strategy(strategy , historical_data):
    # print('hello from evaluate')
    # print(strategy)
    indicator_values = {}
    conditions = []
    logical_ops = []
    condition_results = []

    entryCondition = strategy["entryRuleModel"]

    # data = getHistoricaldata(symbol="GBPUSDm" , timeframe= "1m", totalnoperiod= 1000)
    # historical_data  = pd.DataFrame(data)
    # Calculate all indicators first
    for component in entryCondition:
        if component['type'] == 'indicator':
            indicator = component['name']
            if indicator == "MACD":
                check = checkkCoressOverMacd(strategies=strategy , data= historical_data)
                # print(check)
                condition_results.append(check)
            value = calculate_indicator(component['name'], historical_data, component['parameters'])
            indicator_key = f"{component['name']}_{component['parameters'].get('time period', '')}"
            if value is not None:
                if isinstance(value, tuple):  # Handle multiple values (e.g., MACD)
                    indicator_values[f"{indicator_key}_value"] = value[0].iloc[-1]
                    indicator_values[f"{indicator_key}_signal"] = value[1].iloc[-1]
                else:
                    indicator_values[indicator_key] = value.iloc[-1]

    # print(indicator_values)  # Debug print to see indicator values

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

    # print("Individual Condition Results:", condition_results)  # Debug print

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

    # print(conditions_met)  # Final result print

    return conditions_met

