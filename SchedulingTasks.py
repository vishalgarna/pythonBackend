from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import datetime
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from config.dbconfig import  MongoConnection

from services.evaluteImportant import  evaluteImportant
from services.evaluteStrategy import  evaluate_strategy


db = MongoConnection()
importantmodel_collection = db.get_collection("importantmodel")
strategiesmodel_collection = db.get_collection("strategies")
# Sample functions for tasks



def task_1min(): 

        #evaluting important

    importantmodel_documents = importantmodel_collection.find({"timeframe": "1m"})
    for document in importantmodel_documents:
         evaluteImportant(document)
        
        #evaluting strategies

    strategiesmodel_documents = strategiesmodel_collection.find({"timeframe": "1m"})
    for strategy in strategiesmodel_documents:
         evaluate_strategy(strategy)
    print(f"Task for task_1min timeframe executed at {datetime.datetime.now()}")



     #******************************

def task_5min():
    
     # evaluting important  
    importantmodel_documents = importantmodel_collection.find({"timeframe": "5m"})
    for document in importantmodel_documents:
         evaluteImportant(document)
    
   # evaluting strategy  
    strategiesmodel_documents = strategiesmodel_collection.find({"timeframe": "5m"})
    for strategy in strategiesmodel_documents:
         evaluate_strategy(strategy)
    
    print(f"Task for task_5min timeframe executed at {datetime.datetime.now()}")


    #******************************

def task_15min():

        #evaluting important
    importantmodel_documents = importantmodel_collection.find({"timeframe": "15m"})
    for document in importantmodel_documents:
         evaluteImportant(document)
     
       # evaluting strategy
    strategiesmodel_documents = strategiesmodel_collection.find({"timeframe": "15m"})
    for strategy in strategiesmodel_documents:
         evaluate_strategy(strategy)
    print(f"Task for 15-minute timeframe executed at {datetime.datetime.now()}")


    #******************************

def task_30min():

        #evaluting important
    importantmodel_documents = importantmodel_collection.find({"timeframe": "30m"})
    for document in importantmodel_documents:
         evaluteImportant(document)
         
  # evaluting strategy
    strategiesmodel_documents = strategiesmodel_collection.find({"timeframe": "30m"})
    for strategy in strategiesmodel_documents:
         evaluate_strategy(strategy)
    print(f"task_30min tasks at {datetime.datetime.now()}")


    #******************************

def task_1h():
    
    #evaluting important

    importantmodel_documents = importantmodel_collection.find({"timeframe": "1h"})
    for document in importantmodel_documents:
         evaluteImportant(document)


  # evaluting strategy
    strategiesmodel_documents = strategiesmodel_collection.find({"timeframe": "1h"})
    for strategy in strategiesmodel_documents:
         evaluate_strategy(strategy)
    print(f"Task for task_1h timeframe executed at {datetime.datetime.now()}")


    #******************************

def task_2h():
    
    #ievaluting important

    importantmodel_documents = importantmodel_collection.find({"timeframe": "2h"})
    for document in importantmodel_documents:
         evaluteImportant(document)


  # evaluting strategy

    strategiesmodel_documents = strategiesmodel_collection.find({"timeframe": "2h"})
    for strategy in strategiesmodel_documents:
         evaluate_strategy(strategy)
    print(f"Task for -task_2h timeframe executed at {datetime.datetime.now()}")


    #******************************

def task_4h():
    
    #ievaluting important

    importantmodel_documents = importantmodel_collection.find({"timeframe": "4h"})
    for document in importantmodel_documents:
         evaluteImportant(document)


  # evaluting strategy
    strategiesmodel_documents = strategiesmodel_collection.find({"timeframe": "4h"})
    for strategy in strategiesmodel_documents:
         evaluate_strategy(strategy)
    print(f"task_4h tasks at {datetime.datetime.now()}")


    #******************************

def task_1d():

    #ievaluting important
    importantmodel_documents = importantmodel_collection.find({"timeframe": "1d"})
    for document in importantmodel_documents:
         evaluteImportant(document)

  # evaluting strategy
    strategiesmodel_documents = strategiesmodel_collection.find({"timeframe": "1d"})
    for strategy in strategiesmodel_documents:
         evaluate_strategy(strategy)


    print(f"task_1d tasks at {datetime.datetime.now()}")



    #******************************

# Function to start the scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()

    # Aligning tasks to start at the top of the next minute
    next_minute = (datetime.datetime.now() + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
    delay = (next_minute - datetime.datetime.now()).total_seconds()

    # Schedule tasks to start at the top of the next minute
    scheduler.add_job(task_1min, IntervalTrigger(minutes=1), id='task_1min', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_5min, IntervalTrigger(minutes=5), id='task_5min', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_15min, IntervalTrigger(minutes=15), id='task_15min', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_30min, IntervalTrigger(minutes=30), id='task_30min', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_1h, IntervalTrigger(hours=1), id='task_1h', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_2h, IntervalTrigger(hours=2), id='task_2h', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_4h, IntervalTrigger(hours=4), id='task_4h', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_1d, IntervalTrigger(days=1), id='task_1d', replace_existing=True, next_run_time=next_minute)
    
    
    scheduler.start()
    print("Scheduler started!")

    # Keep the scheduler running
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped!")

