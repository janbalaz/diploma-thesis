"""Communicates both with GensimAPI and MongoDB database. Offers text classification and it's persisting.
Defines also own exception.
@author: Jan Balaz
"""

import pymongo
import datetime
import json
from bson import ObjectId, json_util
from classification.gensimAPI import GensimAPI
from classification.classifications import Algos


class ModelError(Exception):
    """Base exception class for other exception from this module.  """
    pass


class NotPersistedError(ModelError):
    """Raised when data was not persisted in database.  """
    pass


class Model(object):
    """Communicates both with GensimAPI and MongoDB. Stores categories, 
    classified data and offers them to higher layers of application.
    """
    DATABASE = "my_database"
    TABLES = {
        Algos.LDA: "lda",
        Algos.LSI: "lsi"
    }
    DIMENSION = None
    MIN_PROBABILITY = 0.05
    
    def __init__(self, algo=Algos.LDA):
        """Initialises type of used algorithm and opens connection to database.  """
        self.algo = algo
        self.gensim = GensimAPI(algo=algo, trained=True)
        self._get_db()
        # self.DB.drop_collection(self.TABLES[self.algo])

    def classify(self, text):
        """Classifies text with gensim and then persists it. """  
        try:
            categories = self.gensim.classify_text(text, self.DIMENSION, self.MIN_PROBABILITY)
            if categories:
                return True, self._persist_classification(text, categories)
            else:
                raise ModelError("No topic was found for given text. Please try longer or more meaningful text.")
        except Exception as e:
            return False, e
        
    def get_classified_text(self, classif_id):
        """Returns single classified text based on unique key. For example 5543b3976312fc15cc3bd1ee.  """
        collection = self.DB[self.TABLES[self.algo]]
        result = collection.find({"_id": ObjectId(classif_id)})
        if result.count():
            return result[0]
        else:
            return None
    
    def get_all_classified(self):
        """Return all texts classified by given algo, newest first.  """
        collection = self.DB[self.TABLES[self.algo]]
        result = collection.find().sort([("_id", -1)])
        if result.count():
            return list(result)
        else:
            return None
    
    def close_connection(self):
        """Closes connection to database. 
        Recommended to call only when closing whole application because reconnecting is costly operation.
        """
        if self.CONNECTION:
            self.CONNECTION.close()
    
    def _get_db(self, n_tries=3):
        """Tries to connect to DB. Sets DB as class variable.
        If connection failure, tries to repeat itself max. three times.
        """
        try:
            conn = pymongo.MongoClient()
            db = conn[self.DATABASE]
        except pymongo.errors.ConnectionFailure:
            if n_tries:
                self._get_db(n_tries-1)
            else:
                self.DB = None
                self.CONNECTION = None             
        else:
            self.DB = db
            self.CONNECTION = conn
            
    def _persist_classification(self, text, categories):
        """Persists classification of text in database.  """
        try:
            insert = self.DB[self.TABLES[self.algo]].insert_one({
                "categories": categories,
                "text": text,
                "timestamp": json.dumps(datetime.datetime.utcnow(), default=json_util.default)
            })
        except Exception:
            raise NotPersistedError("Error with database insertion through pymongo.")
        else:
            if insert:
                return str(insert.inserted_id)
            else:
                raise NotPersistedError("Classification was not inserted in database.")

    def get_all_categories(self, words):
        """Returns all named categories as tuples."""
        return self.gensim.get_all_topics(words)


if __name__ == "__main__":
    m = Model()
    text = '''The Pope is the Bishop of Rome and the leader of the worldwide Catholic Church.[3]
        The importance of the Roman bishop is largely derived from his role as the traditional successor to Saint Peter,
        to whom Jesus gave the keys of Heaven and the powers of "binding and loosing",
        naming him as the "rock" upon which the church would be built.
        The current pope is Francis, who was elected on 13 March 2013, succeeding Benedict XVI.
        '''
    # print(m.classify(text))
    print(m.get_all_classified())
    # print(m.get_classified_text(ObjectId('5a411a7a71227c6bb3bfc860')))
