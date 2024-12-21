import os , sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__) , '..')))
from services.indicatorsFunction import checkkCoressOverMacd 
from services.placeOrderServices import placedOrder 


def evaluteImportant (strategies):
    orderDetails = strategies["orderDetails"]
    #// check Macdcroosover
    if checkkCoressOverMacd(strategies):
        if placedOrder(orderDetails = orderDetails):
            print('orderplace')
            

        
  
