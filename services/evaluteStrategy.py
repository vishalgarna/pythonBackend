import talib as tb
import os, sys
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.historicalData import getHistoricaldata
from services.placeOrderServices import placedOrder
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



TalibIndicatorsFunctions = {
    "SMA": tb.SMA,
    "RSI": tb.RSI,
    "ADX": tb.ADX,
    "HMA": tb.WMA  # Note: HMA is not a built-in TA-Lib function, using WMA as a placeholder
}

ComparisonFunction = {
    'isEqual': lambda x, y: x == y,
    'isNotEqual': lambda x, y: x != y,
    'isGreaterThan': lambda x, y: x > y,
    'isLessThan': lambda x, y: x < y,
    'isGreaterThanEqual': lambda x, y: x >= y,
    'isLessThanEqual': lambda x, y: x <= y,
}

def get_latest_value(result, indicator_id, symbol_data):
    return result.get(indicator_id) 

def get_compare_value(result, value, symbol_data):
    return result.get(value) 

def evaluate_rule(rule, indicators_result, symbol_data):
    try:
        indicator_id = rule["indicatorId"]
        condition = rule["condition"]
        value = rule["value"]

        latest_value = get_latest_value(indicators_result, indicator_id, symbol_data)
        compare_value = get_compare_value(indicators_result, value, symbol_data)

        new_value = latest_value[-1] if isinstance(latest_value, list) else latest_value[-1]
        second_value = compare_value[-1] if isinstance(compare_value, list) else compare_value[-1]

        print(f"Evaluating rule with new_value: {new_value}, second_value: {second_value}, condition: {condition}")

        comparison_function = ComparisonFunction.get(condition)

        if not comparison_function:
            logging.error(f"Invalid comparison condition: {condition}")
            return False

        return comparison_function(new_value, second_value)
    except Exception as e:
        logging.error(f"Error evaluating rule: {e}")
        return False

def evaluate_indicators(indicators, close):
    acc = {}
    
    for indicator in indicators:
        indicator_id = indicator["indicatorId"]
        indicator_type = indicator["type"]
        parameters = indicator["parameters"]

        indicator_func = TalibIndicatorsFunctions.get(indicator_type)

        if indicator_func is None:
            logging.error(f"Invalid indicator type: {indicator_type}")
            continue

        # Log parameters for debugging
        logging.info(f"Evaluating indicator {indicator_id} with parameters: {parameters}")

        if indicator_type == "close":
            acc["close"] = close
        else:
            try:
                # Unpack the parameters dynamically
                acc[indicator_id] = indicator_func(close, **parameters)  # Unpack parameters as keyword arguments
            except TypeError as te:
                logging.error(f"Error while evaluating {indicator_id}: {te}")

    return acc

def evaluate_strategy(strategy):
    indicators = strategy["indicators"]
    entry_rule_model = strategy["entryRuleModel"]
    order_details = strategy["orderDetails"]
    symbol = strategy["orderDetails"]["symbol"]
    timeframe = strategy["timeframe"]

    symbol_data = getHistoricaldata(symbol , 100, timeframe)
    close = symbol_data["last"]

    indicator_result = evaluate_indicators(indicators, close)
    rule_result = evaluate_rule(entry_rule_model[0], indicator_result, close)

    if rule_result:
        logging.info(f"Strategy met for symbol: {symbol}, executing order details: {order_details}")
        if placedOrder(orderDetails= order_details):
            return True
        else:
            return False 
    else:
        logging.info(f"Strategy not met for symbol: {symbol}")
        return False

