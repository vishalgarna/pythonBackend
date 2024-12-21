
import SchedulingTasks as st
from services.placeOrderServices import placedOrder
import config.appconfig 
from flask  import Flask , request , jsonify

# st.start_scheduler()
print('hello')

app = Flask(__name__)

@app.route('/')
def home():
    return 'Kya haan Hai Lala'

@app.route('/vishal', methods=['POST'])
def placinReqeustOrder():
        
        orderDetails = request.get_json()
        if placedOrder(orderDetails):
             return jsonify({
                  "message" : "success"
             }),200      
        else : 
             return jsonify({"error during place order"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5800, host="0.0.0.0")
