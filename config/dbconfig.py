from pymongo import MongoClient

class MongoConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
            cls._instance.client = MongoClient('mongodb+srv://vishalgarna:vishalgarna%401@cluster0.uxsnu.mongodb.net/')
            cls._instance.db = cls._instance.client['UserAndStrategies']
        return cls._instance

    def get_collection(self, collection_name):
        return self._instance.db[collection_name]


