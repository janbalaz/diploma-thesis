"""Communicates both with GensimAPI and MongoDB database. Offers text classification and it's persisting.
Defines also own exception.
@author: Jan Balaz
"""

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
        #db = self.get_db()
        try:
            self.DB.drop_collection(self.TABLES[key])
            collection = self.DB[self.TABLES[key]]        
            categories = {'45': 'geography', '52': 'Russia', '98': 'indian movies', '40': 'test', '48': 'films', '36': 'classical music and opera', 
                           '87': 'railway', '30': 'dentistry', '75': 'Vietnam', '88': 'space', '85': 'India', '70': 'China', '9': 'music', 
                           '84': 'hockey', '79': 'biology', '5': 'winter sports', '72': 'islam', '58': 'roman and greek history', '22': 'England', 
                           '3': 'Scotland', '61': 'american football', '91': 'mathematics', '21': 'design', '65': 'Portugal', '39': 'South-East Asia', 
                           '49': 'butterflies', '82': 'sports', '47': 'horse racing', '35': 'basketball', '62': 'Africa', '69': 'martial arts', 
                           '51': 'Denmark', '41': 'football', '46': 'Sweden', '86': 'beauty competitions', '50': 'Brazil', '68': 'business', 
                           '42': 'soundtrack', '37': 'USA states', '19': 'flora', '13': 'indian science', '57': 'judaismus', '77': 'environment', 
                           '44': 'archeology', '96': 'Belgium', '1': 'paintings', '81': 'manga and anime', '12': 'moth', '89': 'rugby', 
                           '31': 'aviation', '64': 'history of wars', '78': 'balcan', '74': 'shopping', '56': 'oceania and islands', 
                           '7': 'South America', '16': 'restaurant', '28': 'medicine', '10': 'famous person', '94': 'art', '67': 'olympic', 
                           '53': 'military', '15': 'traffic', '55': 'Ireland', '54': 'science', '0': 'Korea', '90': 'house architecture', 
                           '20': 'massmedia', '80': 'english history', '63': 'naturalism', '33': 'airport', '99': 'Indonesia', '26': 'stars', 
                           '14': 'cristianity', '8': 'Mexico', '92': 'chinese dynasty', '34': 'energy production', '73': 'Finland', 
                           '25': 'criminality', '95': 'regions', '32': 'information technologies', '4': 'France', '17': 'education', 
                           '97': 'politics', '11': 'insect', '66': 'literature', '59': 'arctic', '83': 'games', '2': 'cell and dna biology', 
                           '6': 'pop music', '60': 'cricket', '27': 'Pakistan', '76': 'antarctic islands', '29': 'monarchy', '23': 'Italy', 
                           '43': 'Germany', '38': 'chemistry', '93': 'snail','18': 'law and human rights', '24': 'historic buildings', '71': 'racing'}
            for cnum, cname in categories.items():
                document = {}
                document["_id"] = int(cnum)
                document["name"] = cname
                collection.insert(document)
            return True
        except:
            return False 
    
if __name__ == "__main__":
    model = Model()