'''
Created on 11.3.2015

@author: Jan Balaz
'''
import re, unicodedata, string, gensim, logging, os
from nltk.corpus import stopwords
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
        #self.classif = self.get_trained_algo(algo) if trained else self.train_algo(algo, topics)
    
    def train_algo(self, algo, topics):
        '''
        Trains Gensim library with selected algorithm, uses English Wikipedia dump.
        '''
        id2word = gensim.corpora.Dictionary.load_from_text(os.path.join(self.PATH, 'wordids.txt.bz2'))
        mm = gensim.corpora.MmCorpus(os.path.join(self.PATH, 'tfidf.mm'))
        lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=topics, update_every=1, chunksize=10000, passes=1)
        lda.save(os.path.join(self.PATH, 'trained.' + str(algo).lower()))
        return lda
    
    def get_trained_algo(self, algo):
        '''
        Loads trained data as object of given algorithm.
        '''
        return gensim.models.ldamodel.LdaModel.load(self.PATH + 'trained.' + str(algo).lower())
    
    def classify_text(self, text, dimension):
        '''
        Classifies text, returns vector(of given dimension) of possible themes.
        '''
        text = self.preprocess_text(text)
        themes = self.classif[text]
        themes.sort() #is it necessary?
        return themes[:dimension]
        
    def preprocess_text(self, text):
        '''
        Remove accents, special characters, short words and stopwords.
        '''
        text = self.remove_accents(text)
        text = self.remove_special_characters(text)
        text = self.remove_stopwords(text)
        return text
    
    def remove_stopwords(self, text):
        text = text.split()
        stopwords = set(stopwords.words('english'))
        text = [w for w in text if w not in stopwords]
        return text
    
    def remove_short_words_and_special_chars(self, text):
        '''
        Removes special characters and words shorter than 3 characters.
        '''
        return re.sub(r"\\b\\w{1,4}\\b\\s?|[^\\sa-zA-Z]", "", text) #TODO rozpisat regex aj s komentarom
                    
    def remove_accents(self, text):
        '''
        Removes accents from unicode text.
        '''
        return ''.join(x for x in unicodedata.normalize('NFKD', text) if x in string.ascii_letters).lower()
    
if __name__ == "__main__":
    gens = GensimAPI()
    gens.train_algo('lda', 100)
    