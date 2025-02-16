import threading

# from services.placeOrderServices import placedOrder

# import config.appconfig
from flask import Flask, request, jsonify , abort
import logging
# from services.evaluteImportant import EvaluteBacktestResult
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/')
def home():
    return 'Kya haan Hai Lala'

@app.route('/vishal', methods=['GET'])
def placeRequestOrder():
    try:
        orderDetails = request.args.get("code")
        print(orderDetails)

        abort(400)
    
        # if placedOrder(orderDetails):
        #     return jsonify({"message": "success"}), 200
        # else:
        #     return jsonify({"error": "error during place order"}), 500
    except Exception as e:
        logging.error(f"Error in placeRequestOrder: {e}")
        return jsonify({"error": "internal server error"}), 500
    

 

# backtest Function 
@app.route("/backtest", methods=["GET"])
def backtest_Function():
    strategy = request.get_json()
    print(strategy)

    # results = EvaluteBacktestResult(strategy=strategy)
    # print(results)

    # if results:
    #         # data = {
    #         #     "message": "success",
    #         #     "data": list(results["resultBacktesPairs"]),  # Convert set to list
    #         #     "initialAmount": results["initialAmount"],
    #         #     "pnl": results["pnl"],
    #         # }
    #         data  = {
    #             "data": results
    #         }
    #         return data  # Use jsonify to ensure proper JSON response
    # else:
        # return "Heeljo gibe not " , 500
  


     # Remove debug=True to avoid the signal issue

if __name__ == '__main__':
 app.run(port=5800, host="0.0.0.0") 
#     # Run the scheduler in the main thread
#     run_scheduler()
