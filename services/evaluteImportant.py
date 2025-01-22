import os
import sys
from bson.objectid import ObjectId
import logging

# Add current directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import services.indicatorsFunction as it  
import services.placeOrderServices as pt  
from backtest_results import backtest_results


# Initialize MongoDB connection


def evaluteImportant(document):
    print("vdfb")
#     try:
        # orderDetails = document["orderDetails"]
        # # Check MACD crossover
        # if it.checkkCoressOverMacd(document):
        #     if pt.placedOrder(orderDetails=orderDetails):
        #         id = document["_id"]
        #         importantmodel_collection.update_one({"_id": ObjectId(id)}, {"$set": {"deployed": False}})
        #         logging.info(f"Order placed and document {id} updated.")
    # except Exception as e:
    #     logging.error(f"Error in evaluateImportant: {e}")


def EvaluteStrategy(strategy):
    print("helloji")
    orderDetails = strategy["orderDetails"]
    pairList = orderDetails["symbol"]
    # print(pairList)

    try:
        for symbol in pairList:
            result = it.evaluate_strategy(strategy= strategy , symbol=symbol)
            if result:
                if pt.placedOrder(orderDetails=orderDetails, symbol=symbol):
                    id = strategy["_id"]
                    # strategiesmodel_collection.update_one({"_id": ObjectId(id)}, {"$set": {"deployed": False}})
                    # logging.info(f"Strategy executed and document {id} updated.")
                
    except Exception as e:
        logging.error(f"Error in evaluateStrategy: {e}")            
               



import concurrent.futures
import pandas as pd

def EvaluteBacktestResult(strategy):
    orderDetails = strategy["orderDetails"]
    pairList = orderDetails["symbol"]
    resultBacktesPairs = {}

    def process_symbol(symbol):
        try:
            return symbol, backtest_results(strategy=strategy, symbol=symbol)
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            return symbol, None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_symbol, symbol): symbol for symbol in pairList}
        for future in concurrent.futures.as_completed(futures):
            symbol, result = future.result()
            resultBacktesPairs[symbol] = result
    # print(resultBacktesPairs)
    return resultBacktesPairs




# Example usage
strategy = {
  "timeframe": "4h",
  "orderDetails": {
    "symbol": [
      "USDJPYm",
    #   "USDCHFm"
    ],
    "type": "SELL",
    "stop_loss_pct": 1.0,
    "take_profit_pct": 2.0
  },
  "entryRuleModel": [
    {
      "type": "indicator",
      "name": "MACD",
      "parameters": {
        "fast period": 12,
        "slow period": 26,
        "signal period": 9
      }
    }
  ]
}

# data = EvaluteBacktestResult(strategy = strategy)
# print(data)