import os , sys
from bson.objectid import ObjectId
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__) , '..')))
import services.indicatorsFunction  as it  
import services.placeOrderServices as pt  
from config.dbconfig import MongoConnection


db = MongoConnection()
importantmodel_collection = db.get_collection("importantmodels")
strategies_collection = db.get_collection("importantmodels")


def evaluteImportant (document):
    orderDetails = document["orderDetails"]
    # check Macdcroosover
    if it.checkkCoressOverMacd(document):
        if pt.placedOrder(orderDetails = orderDetails):
            id = document["_id"]
            importantmodel_collection.update_one({"_id": ObjectId(id)} , {"$set" :  {"deployed": False}} )


def EvaluteStrategy(strategy):
    print("helloji")
    orderDetails = strategy["orderDetails"]
    result = it.evaluate_strategy( strategy= strategy)

    if result:
        if pt.placedOrder(orderDetails = orderDetails):
            id = strategy["_id"]
            strategies_collection.update_one({"_id": ObjectId(id)} , {"$set" :  {"deployed": False}} )
        
             



