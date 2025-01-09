
import SchedulingTasks as st
from services.placeOrderServices import placedOrder
import config.appconfig 
from flask  import Flask , request , jsonify
from backtest_results import backtest_results

# st.start_scheduler()
print('hello')

app = Flask(__name__)

@app.route('/')
def home():
    return 'Kya haan Hai Lala'



# orderPlaceFunction

@app.route('/vishal', methods=['POST'])
def placinReqeustOrder():
        orderDetails = request.get_json()
        try:

               if placedOrder(orderDetails):
                    return jsonify({
                         "message" : "success"
                    }),200      
               else : 
                    return jsonify({"error during place order"}), 500
        finally :
         return jsonify({"error during place order"}), 500
          


# backtest Function 
@app.route("/backtest" , methods = ["POST"])
def backtest_Function():
     strategy = request.get_json()
     try:

         results = backtest_results(strategy= strategy)

         if(results):
              return jsonify({
                   "message": "success",
                   "data" : results
              })

     finally:

          return jsonify({"Server Error try after Sometime"}), 500







if __name__ == '__main__':
    app.run(debug=True, port=5800, host="0.0.0.0")
