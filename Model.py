'''
Created on 3.4.2015

@author: Jan Balaz
'''
import pymongo
from Gensim_P.GensimAPI import GensimAPI

class Model(object):
    '''Communicates both with GensimAPI and MongoDB. Stores categories, classified data and offers them to higher layers of application.'''
    DATABASE = 'my_database'
    TABLES = {'cat_lda': 'categories', 'texts': 'texts', 'classif': 'classification', 'cnt': 'counters'}
    DIMENSION = 3
    
    def __init__(self, algo='lda'):
        '''
        Constructor
        '''
        self.algo = algo
    
    def get_db(self):
        '''Tries to connect to DB. Returns DB if successful.'''
        try:
            conn = pymongo.MongoClient()
            db = conn[self.DATABASE]
            return db 
        except pymongo.errors.ConnectionFailure:
            return None
        
    def classify(self, text):
        '''Classifies text with gensim and then persists it.'''
        gensim = GensimAPI(algo=self.algo)
        categories = gensim.classify_text(text, self.DIMENSION)
        return self.persist_classification(text, categories)
        
    def persist_classification(self, text, categories):
        '''Persists text and all of it's classifications.'''
        try:
            db = self.get_db()
            text_id = self.get_next_sequence('texts')
            db[self.TABLES['texts']].insert({'_id': text_id, 'text': text})
            for c_id, c_prob in categories:
                cl_id = self.get_next_sequence('classif')
                db[self.TABLES['classif']].insert({'_id': cl_id, 'category_id': c_id, 'text_id': text_id, 'probability': c_prob})
            return True
        except pymongo.errors.PyMongoError:
            return False
      
    def get_next_sequence(self, name):
        '''Generator of next sequence for collection with given name.'''
        db = self.get_db()
        ret = db[self.TABLES['cnt']].findAndModify({'query': {'_id': name },'update': { '$inc': { 'seq': 1 } }, 'new': True});
        return ret.seq;  
        
    def first_inicialization(self, key):
        '''Used to clear all tables and create mapping and counters.'''
        self.map_categories(key)
        self.create_counters()
        
    def create_counters(self):
        '''Creates counters for auto increment of table's ids.'''
        db = self.get_db()
        db.drop_collection(self.TABLES['cnt'])
        for key, table in self.TABLES:
            db.drop_collection(table)
            db[self.TABLES['cnt']].insert({'_id': key, 'seq': 0})
        
    def map_categories(self, key):
        '''Used only once to map categories and their ids from classification algorithm'''
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
                document['_id'] = int(cnum)
                document['name'] = cname
                collection.insert(document)
            return True
        except:
            return False 
    
if __name__ == "__main__":
    model = Model()
    model.classify('The Pope is the Bishop of Rome and the leader of the worldwide Catholic Church.[3] The importance of the Roman bishop is largely derived from his role as the traditional successor to Saint Peter, to whom Jesus gave the keys of Heaven and the powers of "binding and loosing", naming him as the "rock" upon which the church would be built. The current pope is Francis, who was elected on 13 March 2013, succeeding Benedict XVI.')