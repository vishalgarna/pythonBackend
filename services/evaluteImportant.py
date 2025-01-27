import os
import sys
from bson.objectid import ObjectId
import logging
import concurrent.futures

# Add current directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.evaluteStrategy   import evaluate_strategy
from placeOrderServices import placedOrder 
from backtest_results import backtest_results
from notifications_serivces import send_notification
from config.dbconfig import MongoConnection

strategiesmodel_collection = MongoConnection("strategies")

def EvaluteStrategy(strategy):
    print("helloji")
    orderDetails = strategy["orderDetails"]
    pairList = orderDetails["symbol"]
    # print(pairList)

    try:
        for symbol in pairList:
            result = evaluate_strategy(strategy= strategy , symbol=symbol)
            if result:
                if placedOrder(orderDetails=orderDetails, symbol=symbol):
                    id = strategy["_id"]
                    strategiesmodel_collection.update_one({"_id": ObjectId(id)}, {"$set": {"deployed": False}})
                    logging.info(f"Strategy executed and document {id} updated.")

                    # notification send 
                send_notification("Attention" , "vishal orderPlacing hua iss Symbol ka {symbol} Ek baar Tum Check kar lo kuch important thinks")
                

                
    except Exception as e:
        logging.error(f"Error in evaluateStrategy: {e}")            
               
def EvaluteBacktestResult(strategy):
    orderDetails = strategy["orderDetails"]
    pairList = orderDetails["symbol"]
    resultBacktesPairs = {}
    investedAmount = 1000

    print("ENter in this ")

    def process_symbol(symbol):
        try:
            return symbol, backtest_results(strategy=strategy, symbol=symbol , investedAmount = investedAmount)
        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            return symbol, None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_symbol, symbol): symbol for symbol in pairList}
        for future in concurrent.futures.as_completed(futures):
            symbol, result = future.result()
            resultBacktesPairs[symbol] = result
            afterTrade= result["afterTrade"]
    # print(resultBacktesPairs)
    
    data = {
        "resultBacktesPairs" : resultBacktesPairs,
        "afterTrade" : afterTrade,
        "investedAmount" : investedAmount
    }
    # print(data)
    return data




# Example usage
strategy = {
  "timeframe": "4h",
  "orderDetails": {
    "symbol": [
      "USDJPYm",
      "USDCHFm"
    ],
    "type": "SELL",
    "stop_loss_pct": 1.0,
    "take_profit_pct": 2.0
  },
  "entryRuleModel": [
    # {
    #   "type": "indicator",
    #   "name": "MACD",
    #   "parameters": {
    #     "fast period": 12,
    #     "slow period": 26,
    #     "signal period": 9
    #   }
    # },
    {
      "type": "indicator",
      "name": "william_fractal",
      "parameters": {
        "period": 12,
      
      }
    }
  ]
}
data = EvaluteStrategy(strategy = strategy)
print(data)