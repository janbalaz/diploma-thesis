'''
Created on 11.3.2015

@author: Jan Balaz
'''
import gensim, logging, os
from gensim.corpora import wikicorpus
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class GensimAPI(object):
    '''
    API for Gensim library. Manages training of classification algorithm and process of text classification.
    '''
    PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
    ALGOS = { #dict of supported algorithms and their model functions
             'lsi': gensim.models.lsimodel.LsiModel,
             'lda': gensim.models.ldamodel.LdaModel #TODO train this algo
            }

    def __init__(self, trained=True, algo='lda', topics=100):
        '''
        Loads training data depending on classification algorithm. 
        Raises exception if algo is not supported.
        '''
        if algo.lower() not in self.ALGOS.keys():
            raise Exception #TODO add own exception about not supported
        self.model, self.dictionary = self.get_trained_algo(algo) if trained else self.train_algo(algo, topics)
        if self.model is None or self.dictionary is None:
            raise Exception #TODO add own exception about not trained or loaded
    
    def train_algo(self, algo, topics):
        '''
        Trains Gensim library with selected algorithm, uses English Wikipedia dump.
        '''
        try:
            dictionary = gensim.corpora.Dictionary.load_from_text(os.path.join(self.PATH, 'wordids.txt.bz2'))
            mm = gensim.corpora.MmCorpus(os.path.join(self.PATH, 'tfidf.mm'))
            model = self.get_model(self.ALGOS[algo], mm, dictionary, topics)
            self.persist(model, algo)
            return model, dictionary
        except:
            return None, None
        
    def persist(self, model, algo):
        '''
        Saves trained model to disc.
        '''
        model.save(os.path.join(self.PATH, 'trained.' + str(algo).lower()))
        
    def get_model(self, func, mm, id2word, topics):
        '''
        Returns model for given classification algorithm by func parameter.
        '''
        return func(corpus=mm, id2word=id2word, num_topics=topics)    
    
    def get_trained_algo(self, algo):
        '''
        Loads trained data as object of given algorithm.
        '''
        try:
            model = gensim.models.ldamodel.LdaModel.load(self.PATH + '\\trained.' + str(algo).lower())
            dictionary = gensim.corpora.Dictionary.load_from_text(os.path.join(self.PATH, 'wordids.txt.bz2'))
            return model, dictionary
        except:
            return None, None
    
    def classify_text(self, text, dimension=10):
        '''
        Classifies text, adjusts result vector to given dimension or smaller.
        Vector of possible themes is a list of tuples (theme id, suitability).
        Returns vector sorted by suitability descending.
        '''
        classified = self.model[self.get_query(text)]
        themes = list(sorted(classified, key=lambda x: x[1], reverse=True))
        #self.print_themes(themes) #for DEBUG only
        return themes[:dimension]
    
    def get_query(self, text):
        '''
        Preprocess and tokenize text, return it as BOW (bag of words)
        '''
        return self.dictionary.doc2bow(wikicorpus.tokenize(text))
    
    def print_themes(self, themes):
        '''
            Print suitable themes for debugging purpose. Delete before production.
        '''
        for theme in themes:
            print(str(theme[0]) + ": " + self.model.print_topic(theme[0]))
    
if __name__ == "__main__":
    #gens = GensimAPI()
    #gens = GensimAPI(False, 'lsi', 100)
    #gens.train_algo('lsi', 100)
    #themes = gens.classify_text('The Pope is the Bishop of Rome and the leader of the worldwide Catholic Church.[3] The importance of the Roman bishop is largely derived from his role as the traditional successor to Saint Peter, to whom Jesus gave the keys of Heaven and the powers of "binding and loosing", naming him as the "rock" upon which the church would be built. The current pope is Francis, who was elected on 13 March 2013, succeeding Benedict XVI.')
    #themes = gens.classify_text('French Paris Jean Jacques France French')
    #print(themes)
    