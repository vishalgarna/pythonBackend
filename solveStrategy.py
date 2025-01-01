import pandas as pd
import talib

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

class LogicalOperator:
    def __init__(self, name):
        self.name = name

    def evaluate(self, conditions):
        if self.name == 'AND':
            return all(conditions)
        elif self.name == 'OR':
            return any(conditions)
        else:
            raise ValueError(f"Unknown logical operator: {self.name}")

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

def calculate_indicator(name, historical_data, parameters=None):
    if name == 'SMA':
        return pd.Series(calculate_sma(historical_data, parameters['time period']), index=historical_data.index)
    elif name == 'EMA':
        return pd.Series(calculate_ema(historical_data, parameters['time period']), index=historical_data.index)
    elif name == 'RSI':
        return pd.Series(calculate_rsi(historical_data, parameters['time period']), index=historical_data.index)
    elif name == 'MACD':
        macd, macd_signal = calculate_macd(historical_data)
        return (pd.Series(macd, index=historical_data.index), pd.Series(macd_signal, index=historical_data.index))
    else:
        raise ValueError(f"Unknown indicator: {name}")

def generate_indicator_key(component, count):
    parameters_str = '_'.join([f"{key}_{value}" for key, value in sorted(component['parameters'].items())])
    return f"{component['name']}_{parameters_str}_{count}"

def evaluate_strategy(historical_data, strategy):
    indicator_values = {}
    indicator_keys = {}
    indicator_counter = {}
    trades = []
    conditions = []
    logical_ops = []

    for component in strategy:
        if component['type'] == 'indicator':
            value = calculate_indicator(component['name'], historical_data, component['parameters'])
            if component['name'] not in indicator_counter:
                indicator_counter[component['name']] = 0
            indicator_key_base = generate_indicator_key(component, indicator_counter[component['name']])
            
            # Debug print to show generated key
            print(f"Generated Key for Indicator: {indicator_key_base}")
            
            if component['name'] not in indicator_keys:
                indicator_keys[component['name']] = []
            indicator_keys[component['name']].append(indicator_key_base)
            
            indicator_counter[component['name']] += 1

            if value is not None:
                if isinstance(value, tuple):
                    indicator_values[f"{indicator_key_base}_value"] = value[0].iloc[-1]
                    indicator_values[f"{indicator_key_base}_signal"] = value[1].iloc[-1]
                else:
                    indicator_values[indicator_key_base] = value.iloc[-1]

    print("Indicator Values:", indicator_values)  # Debug print to show all indicator values

    i = 0
    while i < len(strategy):
        component = strategy[i]
        if component['type'] == 'condition':
            prev_indicator_key = indicator_keys[strategy[i-1]['name']][-1]
            next_indicator_key = indicator_keys[strategy[i+1]['name']][-1]
            
            # Debug print to show keys used in condition
            print(f"Condition Keys: {prev_indicator_key}, {next_indicator_key}")

            conditions.append((component['name'], indicator_values[prev_indicator_key], indicator_values[next_indicator_key]))
        elif component['type'] == 'logicalOperator':
            logical_ops.append(component['name'])
        i += 1

    condition_results = []
    for cond in conditions:
        condition = Condition(cond[0])
        values = [cond[1], cond[2]]
        if not any(pd.isna(values)):
            result = condition.evaluate(values)
            condition_results.append(result)
        else:
            condition_results.append(False)

    if logical_ops:
        conditions_met = condition_results[0]
        for j, logical_op in enumerate(logical_ops):
            logical_operator = LogicalOperator(logical_op)
            conditions_met = logical_operator.evaluate([conditions_met, condition_results[j+1]])
    else:
        conditions_met = condition_results[0]

    if conditions_met:
        print(conditions_met)
        trades.append(('Buy', historical_data['last'].iloc[-1]))

    return trades

def backtest(historical_data, strategy):
    trades = evaluate_strategy(historical_data, strategy)
    net_profit = 0
    buy_price = None

    for trade in trades:
        if trade[0] == 'Buy':
            if buy_price is None:
                buy_price = trade[1]
        elif trade[0] == 'Sell':
            if buy_price is not None:
                net_profit += trade[1] - buy_price
                buy_price = None

    results = {
        'Net Profit': net_profit,
        'Number of Trades': len(trades),
        'Win/Loss Ratio': net_profit / len(trades) if len(trades) > 0 else 0
    }

    return results

def fetch_historical_data(symbol):
    return pd.DataFrame([
        {"last": 100}, {"last": 105}, {"last": 110}, {"last": 115},
        {"last": 120}, {"last": 125}, {"last": 130}, {"last": 135},
        {"last": 140}, {"last": 145}, {"last": 150}, {"last": 155},
        {"last": 160}, {"last": 165}, {"last": 170}, {"last": 175},
        {"last": 180}, {"last": 185}, {"last": 190}, {"last": 195},
        {"last": 200}, {"last": 205}, {"last": 210}, {"last": 215},
        {"last": 220}, {"last": 225}, {"last": 230}, {"last": 235},
        {"last": 240}, {"last": 245}, {"last": 250}
    ])

strategy = [
    {"type": "indicator", "name": "SMA", "parameters": {"time period": 20}},
    {"type": "condition", "name": "isGreaterThan"},
    {"type": "indicator", "name": "SMA", "parameters": {"time period": 5}},
    {"type": "logicalOperator", "name": "OR"},
    {"type": "indicator", "name": "SMA", "parameters": {"time period": 25}},
    {"type": "condition", "name": "isGreaterThan"},
    {"type": "indicator", "name": "SMA", "parameters": {"time period": 10}},
    {"type": "logicalOperator", "name": "AND"},
    {"type": "indicator", "name": "SMA", "parameters": {"time period": 20}},
    {"type": "condition", "name": "isLessThan"},
    {"type": "indicator", "name": "SMA", "parameters": {"time period": 5}},
    {"type": "action", "name": "Buy"}
]

historical_data = fetch_historical_data('symbol')

results = backtest(historical_data, strategy)
print("Backtest Results:", results)
