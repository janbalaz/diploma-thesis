"""Module trains chosen algorithms and then classifies text inputs.
@author: Jan Balaz
"""

import os
import gensim
import logging
from gensim.corpora import wikicorpus


class GensimAPIError(Exception):
    """Base exception class for other exception from this module.  """
    pass


class NotSupportedError(GensimAPIError):
    """Raised when given algorithm is not supported in this API.  """
    pass


class NotTrainedError(GensimAPIError):
    """Raised when algorithm was not trained or properly loaded.  """
    pass


class GensimAPI(object):
    """API for Gensim library. Manages training of classification algorithm and process of text classification.  """
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources")
    TF_IDF = "tfidf.mm.bz2"
    WORD_IDS = "wordids.txt.bz2"
    ALGOS = {
        "lda": {
            "model": gensim.models.LdaModel,
            "dir": "lda_100",
            "topics": 100
        },
        "lsi": {
            "model": gensim.models.LsiModel,
            "dir": "lsi_100",
            "topics": 100
        }
    }

    def __init__(self, trained=False, algo="lda", topics=100):
        """Loads training data depending on classification algorithm.Raises exception if algo is not supported.  """
        if algo.lower() not in self.ALGOS.keys():
            raise NotSupportedError("Training algorithm used for classification is not supported by this application.")
        self.model, self.dictionary = self._get_trained_algo(algo) if trained else self._train_algo(algo, topics)
        if self.model is None or self.dictionary is None:
            raise NotTrainedError("Training of algorithm was not successful, cannot be used for classification.")
        
    def classify_text(self, text, dimension=10):
        """Classifies text, adjusts result vector to given dimension or smaller.  
        Vector of possible themes is a list of tuples (theme id, suitability).  
        Returns vector sorted by suitability descending.  
        """
        classified = self.model[self._get_query(text)]
        themes = list(sorted(classified, key=lambda x: x[1], reverse=True))
        return themes[:dimension]
    
    def _train_algo(self, algo, topics):
        """Trains Gensim library with selected algorithm, uses English Wikipedia dump.  """
        try:
            dictionary = gensim.corpora.Dictionary.load_from_text(os.path.join(self.PATH, self.WORD_IDS))
            mm = gensim.corpora.MmCorpus(os.path.join(self.PATH, self.TF_IDF))
            model = self._get_model(self.ALGOS[algo]["model"], mm, dictionary, topics)
            self._persist(model, algo)
        except Exception:
            return None, None
        else:
            return model, dictionary
        
    def _persist(self, model, algo):
        """Saves trained model to disc.  """
        model.save(os.path.join(self.PATH, self.ALGOS[algo]["dir"], 'trained.' + str(algo).lower()))
        
    def _get_model(self, func, mm, id2word, topics):
        """Returns model for given classification algorithm by func parameter.  """
        return func(corpus=mm, id2word=id2word, num_topics=topics, distributed=True)
    
    def _get_trained_algo(self, algo):
        """Loads trained data as object of given algorithm.  """
        try:
            path = os.path.join(self.PATH, self.ALGOS[algo]["dir"], "trained.{}".format(str(algo).lower()))
            model = gensim.models.LdaModel.load(path)
            dictionary = gensim.corpora.Dictionary.load_from_text(os.path.join(self.PATH,
                                                                               self.ALGOS[algo]["dir"],
                                                                               self.WORD_IDS))
        except Exception as e:
            print(e)
            return None, None
        else:
            return model, dictionary
    
    def _get_query(self, text):
        """Preprocess and tokenize text, return it as BOW (bag of words).  """
        return self.dictionary.doc2bow(wikicorpus.tokenize(text))
    
    def _print_themes(self, themes):
        """Print suitable themes for debugging purpose. Delete before production.  """
        for theme in themes:
            print(str(theme[0]) + ": " + self.model.print_topic(theme[0]))
            
    def _get_all_themes(self, count=100):
        """Themes for debugging purpose. Delete before production.  """
        themes = self.model.print_topics(count)
        return themes


if __name__ == "__main__":
    gens = GensimAPI(trained=True)
    print(gens.classify_text('''The Pope is the Bishop of Rome and the leader of the worldwide Catholic Church.[3] 
        The importance of the Roman bishop is largely derived from his role as the traditional successor to Saint Peter, 
        to whom Jesus gave the keys of Heaven and the powers of "binding and loosing", 
        naming him as the "rock" upon which the church would be built. 
        The current pope is Francis, who was elected on 13 March 2013, succeeding Benedict XVI.
        '''))
    print(gens._get_all_themes())
