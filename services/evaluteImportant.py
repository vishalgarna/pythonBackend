# import os
# import sys
# from bson.objectid import ObjectId
import logging
import concurrent.futures
# from pymongo import MongoClient
# import certifi
from evaluteStrategy import evaluate_strategy
# from services.placeOrderServices import placedOrder 
# from backtest_results import backtest_results
from notifications_serivces import send_notification
# from config.dbconfig import MongoConnection

# Get the collection
# mongo_conn = MongoConnection()
# strategiesmodel_collection = mongo_conn.get_collection("strategies")

def EvaluteStrategy(strategy):
    print("helloji")
    orderDetails = strategy["orderDetails"]
    pairList = orderDetails["symbol"]
    # print(pairList)

    try:
        for symbol in pairList:
            result = evaluate_strategy(strategy=strategy, symbol=symbol)
            if result:
                # if placedOrder(orderDetails=orderDetails, symbol=symbol):
                    # id = strategy["_id"]
                    # strategiesmodel_collection.update_one({"_id": ObjectId(id)}, {"$set": {"deployed": False}})
                    # logging.info(f"Strategy executed and document {id} updated.")

                    # notification send 
                send_notification("Attention", f"Vishal, order placed for {symbol}. Please check important details.")
                
    except Exception as e:
        logging.error(f"Error in evaluateStrategy: {e}")

# def EvaluteBacktestResult(strategy):
#     orderDetails = strategy["orderDetails"]
#     pairList = orderDetails["symbol"]
#     resultBacktesPairs = {}
#     investedAmount = 1000

#     print("ENter in this ")

#     def process_symbol(symbol):
#         try:
#             return symbol, backtest_results(strategy=strategy, symbol=symbol, investedAmount=investedAmount)
#         except Exception as e:
#             print(f"Error processing {symbol}: {e}")
#             return symbol, None

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         futures = {executor.submit(process_symbol, symbol): symbol for symbol in pairList}
#         for future in concurrent.futures.as_completed(futures):
#             symbol, result = future.result()
#             resultBacktesPairs[symbol] = result
#             afterTrade = result["afterTrade"]
#     # print(resultBacktesPairs)
    
#     data = {
#         "resultBacktesPairs": resultBacktesPairs,
#         "afterTrade": afterTrade,
#         "investedAmount": investedAmount
#     }
#     # print(data)
#     return data

# Example usage
strategy = {
    "timeframe": "1d",
    "orderDetails": {
        "symbol": ["USDCHFm"],
        "type": "SELL",
        "stop_loss_pct": 1.0,
        "take_profit_pct": 2.0
    },
    "entryRuleModel": [

        {
            "type": "indicator",
            "name": "MACD",
            "parameters": {"period": 12}
        },

        {
            "type": "logicalOperator",
            "name": "AND",
            "parameters": {"period": 12}
        },
        {
            "type": "indicator",
            "name": "close",
            "parameters": {"time period": 12}
        },
        {
            "type": "condition",
            "name": "isLessThan",
        },
         {
            "type": "indicator",
            "name": "SMA",
            "parameters": {"time period": 9}
        },

    ]
}

data = EvaluteStrategy(strategy=strategy)
print(data)
