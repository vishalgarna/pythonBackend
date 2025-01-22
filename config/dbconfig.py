from pymongo import MongoClient
import certifi

class MongoConnection:
    """Singleton class to manage MongoDB connections."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoConnection, cls).__new__(cls)
            cls._instance.client = MongoClient(
                'mongodb+srv://vishalgarna:vishalgarna%401@cluster0.uxsnu.mongodb.net/',
                tlsCAFile=certifi.where()
            )
            cls._instance.db = cls._instance.client['UserAndStrategies']
        return cls._instance

    def get_collection(self, collection_name):
        """Retrieve a collection from the MongoDB database.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            Collection: The MongoDB collection.
        """
        return self._instance.db[collection_name]

