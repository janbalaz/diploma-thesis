"""TODO add desc
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
    TABLES = {"cat_lda": "categories", "texts": "texts", "classif": "classification"}
    DIMENSION = 3
    
    def __init__(self, algo="lda"):
        """
        Constructor
        """
        self.algo = algo
        self._get_db()
    
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
        else:
            self.DB = db
        
    def classify(self, text):
        """Classifies text with gensim and then persists it. """  
        try:
            gensim = GensimAPI(algo=self.algo)  
        except Exception as e:
            return False, e.get_message()
        else:
            categories = gensim.classify_text(text, self.DIMENSION)
            return self._persist(text, categories)
        
    def _persist(self, text, categories):
        """Persists text and all of it's classifications. """
        try:
            text_id = self._persist_text(text)
            self._persist_classification(text, categories)
        except Exception as e:
            return False, e.get_message()
        else:
            return True, text_id
        
    def _persist_text(self, text):
        """Persists text which was classified in database.  """
        text_id = ObjectId()
        try:
            insert = self.DB[self.TABLES["texts"]].insert({"_id": text_id, 
                                                           "text": text})
        except pymongo.errors.PyMongoError:
            raise NotPersistedError("Error with database insertion through pymongo.")
        else:
            if insert["nInserted"]:
                return text_id
            else:
                raise NotPersistedError("Number of inserted objects is 0.")
            
    def _persist_classification(self, t_id, categories):
        """Persists classification of text in database.  """
        try:
            counter = 0
            for c_id, c_prob in categories:
                insert = self.DB[self.TABLES["classif"]].insert({"category_id": c_id, 
                                                                 "text_id": t_id, 
                                                                 "probability": c_prob, 
                                                                 "algo": self.algo})
                if not insert["nInserted"]:
                    counter += 1                
        except pymongo.errors.PyMongoError:
            raise NotPersistedError("Error with database insertion through pymongo.")  
        else:
            if counter:
                raise NotPersistedError("{} categories were not inserted in database.".format(counter))
        
    def first_inicialization(self, key):
        """Used only once to map categories and their ids from classification algorithm.  """
        db = self.get_db()
        try:
            db.drop_collection(self.TABLES[key])
            collection = db[self.TABLES[key]]        
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
    model.classify('The Pope is the Bishop of Rome and the leader of the worldwide Catholic Church.[3] The importance of the Roman bishop is largely derived from his role as the traditional successor to Saint Peter, to whom Jesus gave the keys of Heaven and the powers of "binding and loosing", naming him as the "rock" upon which the church would be built. The current pope is Francis, who was elected on 13 March 2013, succeeding Benedict XVI.')