"""Communicates both with GensimAPI and MongoDB database. Offers text classification and it's persisting.
Defines also own exception.
@author: Jan Balaz
"""

import os
import json
import pymongo
from bson import ObjectId
from gensim_P.gensimAPI import GensimAPI


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
    TABLES = {"cat_lda": "categories", "classif": "classification"}
    DIMENSION = 3
    
    def __init__(self, algo="lda"):
        """Initialises type of used algorithm and opens connection to database.  """
        self.algo = algo
        self._get_db()
        #self.DB.drop_collection(self.TABLES["classif"])
        
    def classify(self, text):
        """Classifies text with gensim and then persists it. """  
        try:
            gensim = GensimAPI(algo=self.algo)  
        except Exception as e:
            return False, e.get_message()
        else:
            categories = gensim.classify_text(text, self.DIMENSION)
            return self._persist(text, categories)
        
    def get_classified_text(self, classif_id, algo="lda"):
        """Returns single classified text based on unique key. For example 5543b3976312fc15cc3bd1ee.  """
        collection = self.DB[self.TABLES["classif"]]
        result = collection.find({"_id": classif_id, "algo": algo})
        if result.count():
            return result[0]
        else:
            return None
    
    def get_all_classified(self, algo="lda"):
        """Return all texts classified by given algo.  """
        collection = self.DB[self.TABLES["classif"]]
        result = collection.find({"algo": algo})
        if result.count():
            return list(result)
        else:
            return None
    
    def reconnect_db(self):
        """Tries to reconnect to db if connection was not established.  """
        self._get_db()
    
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
        
    def _persist(self, text, categories):
        """Persists text and all of it's classifications. """
        try:
            classif_id = self._persist_classification(text, categories)
        except Exception as e:
            return False, e.get_message()
        else:
            return True, classif_id
            
    def _persist_classification(self, text, categories):
        """Persists classification of text in database.  """
        try:
            named_categories = self._get_named_categories(categories)
            classif_id = ObjectId()
            insert = self.DB[self.TABLES["classif"]].insert({"_id": str(classif_id),
                                                             "categories": named_categories, 
                                                             "text": text, 
                                                             "algo": self.algo})               
        except pymongo.errors.PyMongoError:
            raise NotPersistedError("Error with database insertion through pymongo.")  
        else:
            if insert:
                return insert
            else:
                raise NotPersistedError("Classification was not inserted in database.")

    def get_all_categories(self):
        """Returns all named categories."""
        collection = self.DB[self.TABLES["cat_{}".format(self.algo)]]
        categories = []
        for row in collection.find():
            categories.append(row)

        return categories
            
    def _get_named_categories(self, categories):
        """Assigns names of categories to them.  """
        named_categories = []
        for c_id, probability in categories:
            c_name = self._get_category_name(c_id)
            named_categories.append((c_id, c_name, probability))
        return named_categories
            
    def _get_category_name(self, c_id):
        """Return name of category with given id.  """
        collection = self.DB[self.TABLES["cat_" + self.algo]]
        result = collection.find({"_id": c_id})
        if result.count():
            return result[0]["name"]
        else:
            return None
        
    def first_inicialization(self, key):
        """Used only once to map categories and their ids from classification algorithm.  """
        try:
            collection = self.DB[self.TABLES[key]]
            if collection.count() is not 0:
                self.DB.drop_collection(self.TABLES[key])
                collection = self.DB[self.TABLES[key]]

            filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources/named_categories.lda")
            with open (filepath, "r") as f:
                categories = f.read().replace('\n', '')

            categories = json.loads(categories)
            for cnum, cname in categories.items():
                document = {}
                document["_id"] = int(cnum)
                document["name"] = cname
                collection.insert(document)
            return True
        except Exception as e:
            print(e)
            return False 
    
if __name__ == "__main__":
    print(Model().first_inicialization("cat_lda"))