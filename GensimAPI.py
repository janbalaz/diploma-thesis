'''
Created on 11.3.2015

@author: Jan Balaz
'''
import re, gensim, logging, os
from nltk.corpus import stopwords
from gensim import utils
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class GensimAPI(object):
    '''
    API for Gensim library. Manages training of classification algorithm and process of text classification.
    '''
    PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
    ALGOS = {'lsi', 'lda', 'tfidf'} #set of supported algorithms

    def __init__(self, trained=True, algo='lda', topics=100):
        '''
        Loads training data depending on classification algorithm. 
        Raises exception if algo is not supported.
        '''
        if algo.lower() not in self.ALGOS:
            raise Exception #TODO add own exception
        self.model = self.get_trained_algo(algo) if trained else self.train_algo(algo, topics)
    
    def train_algo(self, algo, topics):
        '''
        Trains Gensim library with selected algorithm, uses English Wikipedia dump.
        '''
        id2word = gensim.corpora.Dictionary.load_from_text(os.path.join(self.PATH, 'wordids.txt.bz2'))
        mm = gensim.corpora.MmCorpus(os.path.join(self.PATH, 'tfidf.mm'))
        lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=topics, update_every=0, passes=20)
        lda.save(os.path.join(self.PATH, 'trained.' + str(algo).lower()))
        return lda
    
    def get_trained_algo(self, algo):
        '''
        Loads trained data as object of given algorithm.
        '''
        return gensim.models.ldamodel.LdaModel.load(self.PATH + '\\trained.' + str(algo).lower())
    
    def classify_text(self, text, dimension=10):
        '''
        Classifies text, returns vector(of given dimension) of possible themes.
        '''
        text = self.preprocess_text(text)
        dictionary = gensim.corpora.Dictionary()
        dictionary.merge_with(self.model.id2word)   
        query = dictionary.doc2bow(text)
        themes = list(sorted(self.model[query], key=lambda x: x[1], reverse=True))
        #for theme in themes:
        #    print(str(theme[0]) + ": " + self.model.print_topic(theme[0]))
        return themes[:dimension]
    
    def preprocess_text(self, text):
        '''
        Remove accents, special characters, short words and stopwords.
        '''
        text = self.remove_accents(text)
        text = self.remove_short_words_and_special_chars(text)
        text = self.remove_stopwords(text)
        return text
    
    def remove_stopwords(self, text):
        text = text.split()
        sw = set(stopwords.words('english'))
        text = [w.lower() for w in text if w not in sw]
        return text
    
    def remove_short_words_and_special_chars(self, text):
        '''
        Removes special characters and words shorter than 3 characters.
        '''
        return re.sub(r"\b\w{1,4}\b\s?|[^\sa-zA-Z]", "", text) #TODO rozpisat regex aj s komentarom
                    
    def remove_accents(self, text):
        '''
        Removes accents from unicode text.
        '''
        return utils.to_unicode(text)
    
if __name__ == "__main__":
    gens = GensimAPI(False)
    #themes = gens.classify_text('The Pope is the Bishop of Rome and the leader of the worldwide Catholic Church.[3] The importance of the Roman bishop is largely derived from his role as the traditional successor to Saint Peter, to whom Jesus gave the keys of Heaven and the powers of "binding and loosing", naming him as the "rock" upon which the church would be built. The current pope is Francis, who was elected on 13 March 2013, succeeding Benedict XVI.')
    #themes = gens.classify_text('French Paris Jean Jacques France French')
    #print(themes)
    