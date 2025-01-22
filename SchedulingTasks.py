import logging

# Configure the logging (temporarily set to DEBUG to check for errors)
logging.basicConfig(level=logging.INFO, 
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
handlers=[logging.StreamHandler()])

# Set the logging level for APScheduler
logging.getLogger('apscheduler').setLevel(logging.INFO)

# Your existing scheduler code
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import datetime
import time
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.dbconfig import MongoConnection
from services.evaluteImportant import  EvaluteStrategy

db = MongoConnection()
importantmodel_collection = db.get_collection("importantmodels")
strategiesmodel_collection = db.get_collection("strategies")

# Task functions
def task_1min():
    logging.info("Task for task_1min timeframe executed")
    try:
        strategiesmodel_documents = list(strategiesmodel_collection.find({"timeframe": "1m", "deployed": True}))
        for strategy in strategiesmodel_documents:
            EvaluteStrategy(strategy)
    except Exception as e:
        logging.error(f"Error in task_1min: {e}")

def task_5min():
    logging.info("Task for task_5min timeframe executed")
    try:
        strategiesmodel_documents = list(strategiesmodel_collection.find({"timeframe": "5m", "deployed": True}))
        for strategy in strategiesmodel_documents:
            EvaluteStrategy(strategy)
    except Exception as e:
        logging.error(f"Error in task_5min: {e}")

def task_15min():
    logging.info("Task for 15-minute timeframe executed")
    try:
        strategiesmodel_documents = list(strategiesmodel_collection.find({"timeframe": "15m", "deployed": True}))
        for strategy in strategiesmodel_documents:
            EvaluteStrategy(strategy)
    except Exception as e:
        logging.error(f"Error in task_15min: {e}")

def task_30min():
    logging.info("Task for task_30min timeframe executed")
    try:
        strategiesmodel_documents = list(strategiesmodel_collection.find({"timeframe": "30m", "deployed": True}))
        for strategy in strategiesmodel_documents:
            EvaluteStrategy(strategy)
    except Exception as e:
        logging.error(f"Error in task_30min: {e}")

def task_1h():
    logging.info("Task for task_1h timeframe executed")
    try:
        strategiesmodel_documents = list(strategiesmodel_collection.find({"timeframe": "1h", "deployed": True}))
        for strategy in strategiesmodel_documents:
            EvaluteStrategy(strategy)
    except Exception as e:
        logging.error(f"Error in task_1h: {e}")

def task_2h():
    logging.info("Task for task_2h timeframe executed")
    try:
        strategiesmodel_documents = list(strategiesmodel_collection.find({"timeframe": "2h", "deployed": True}))
        for strategy in strategiesmodel_documents:
            EvaluteStrategy(strategy)
    except Exception as e:
        logging.error(f"Error in task_2h: {e}")

def task_4h():
    logging.info("Task for task_4h timeframe executed")
    try:
        strategiesmodel_documents = list(strategiesmodel_collection.find({"timeframe": "4h", "deployed": True}))
        for strategy in strategiesmodel_documents:
            EvaluteStrategy(strategy)
    except Exception as e:
        logging.error(f"Error in task_4h: {e}")

def task_1d():
    logging.info("Task for task_1d timeframe executed")
    try:
        strategiesmodel_documents = list(strategiesmodel_collection.find({"timeframe": "1d", "deployed": True}))
        for strategy in strategiesmodel_documents:
            EvaluteStrategy(strategy)
    except Exception as e:
        logging.error(f"Error in task_1d: {e}")

# Function to start the scheduler
def start_scheduler():
    scheduler = BackgroundScheduler()

    # Aligning tasks to start at the top of the next minute
    next_minute = (datetime.datetime.now() + datetime.timedelta(minutes=1)).replace(second=0, microsecond=0)
    delay = (next_minute - datetime.datetime.now()).total_seconds()

    # Schedule tasks to start at the top of the next minute
    # scheduler.add_job(task_1min, IntervalTrigger(minutes=1), id='task_1min', replace_existing=True, next_run_time=next_minute)
    # scheduler.add_job(task_5min, IntervalTrigger(minutes=5), id='task_5min', replace_existing=True, next_run_time=next_minute)
    # scheduler.add_job(task_15min, IntervalTrigger(minutes=15), id='task_15min', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_30min, IntervalTrigger(minutes=30), id='task_30min', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_1h, IntervalTrigger(hours=1), id='task_1h', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_2h, IntervalTrigger(hours=2), id='task_2h', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_4h, IntervalTrigger(hours=4), id='task_4h', replace_existing=True, next_run_time=next_minute)
    scheduler.add_job(task_1d, IntervalTrigger(days=1), id='task_1d', replace_existing=True, next_run_time=next_minute)

    scheduler.start()
    logging.info("Scheduler started!")

    # Keep the scheduler running
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Scheduler stopped!")

if __name__ == "__main__":
    start_scheduler()
