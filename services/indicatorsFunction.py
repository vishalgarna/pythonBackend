import pandas as pd
import talib 
from services.historicalData import getHistoricaldata
from services.placeOrderServices import placedOrder
# Sample closing prices
#Convert to DataFrame





def checkkCoressOverMacd(strategies):
        symbol = strategies["orderDetails"]["symbol"]
        timeframe = strategies["timeframe"]
        type = strategies["orderDetails"]["type"]
        data = getHistoricaldata(symbol=symbol, totalnoperiod=100 , timeframe=timeframe)
        # Calculate MACD using talib
        macd, signal, hist = talib.MACD(data['last'], fastperiod=12, slowperiod=26, signalperiod=9)
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


class MomentumIndictor:
    
    def __init__(self , name):
        self.name = name

    def evaluteMomnetum(self , strategy):
        
        if self.name == "MACD":
            
            return checkkCoressOverMacd(strategies=strategy)
        
                
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
        

def calculate_indicator(name, historical_data,time_period) :
    if name == 'SMA':
        return talib.SMA(historical_data, timeperiod=time_period)
    elif name == 'EMA':
        return talib.EMA(historical_data, timeperiod=time_period)
    elif name == 'RSI':
          return talib.EMA(historical_data, timeperiod=time_period)

    else:
        raise ValueError(f"Unknown indicator: {name}")


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

    def evaluate(name, values):
        print(f"Evaluating Condition: {name} with Values: {values}")  # Debug print
        if name == 'isGreaterThan':
            return values[0] > values[1] if not any(pd.isna(values)) else False
        elif name == 'isLessThan':
            return values[0] < values[1] if not any(pd.isna(values)) else False
        else:
            raise ValueError(f"Unknown condition: {name}")
        


def evaluate_strategy(historical_data, strategy):
    indicator_values = {}
    trades = []
    conditions = []
    logical_ops = []

    # Calculate all indicators first
    for component in strategy:
        if component['type'] == 'indicator':
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
    while i < len(strategy):
        component = strategy[i]
        if component['type'] == 'condition':
            prev_indicator_key = f"{strategy[i-1]['name']}_{strategy[i-1]['parameters'].get('time period', '')}"
            next_indicator_key = f"{strategy[i+1]['name']}_{strategy[i+1]['parameters'].get('time period', '')}"
            conditions.append((component['name'], indicator_values[prev_indicator_key], indicator_values[next_indicator_key]))
        elif component['type'] == 'logicalOperator':
            logical_ops.append(component['name'])
        i += 1

    # Evaluate all conditions
    condition_results = []
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
            logical_operator = LogicalOperator(logical_op)
            conditions_met = logical_operator.evaluate([conditions_met, condition_results[j+1]])
    else:
        conditions_met = condition_results[0]

    print("Conditions Met:", conditions_met)  # Debug print

    # Execute actions based on the conditions

    return "condtion met"

