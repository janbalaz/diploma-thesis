"""Module trains chosen algorithms and then classifies text inputs.
@author: Jan Balaz
"""

import os
import gensim
import logging
from gensim.corpora import wikicorpus
from classification.classifications import Algos


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
        Algos.LDA: {
            "name": "lda",
            "model": gensim.models.LdaModel,
            "dir": "lda_100",
            "topics": 100
        },
        Algos.LSI: {
            "name": "lsi",
            "model": gensim.models.LsiModel,
            "dir": "lsi_100",
            "topics": 100
        }
    }

    def __init__(self, trained=False, algo=Algos.LDA, topics=100):
        """Loads training data depending on classification algorithm.Raises exception if algo is not supported.  """
        if algo not in self.ALGOS.keys():
            raise NotSupportedError("Training algorithm used for classification is not supported by this application.")
        self.algo = algo
        self.model, self.dictionary = self._get_trained_algo(algo) if trained else self._train_algo(algo, topics)
        if self.model is None or self.dictionary is None:
            raise NotTrainedError("Training of algorithm was not successful, cannot be used for classification.")
        
    def classify_text(self, text, dimension=None, minimum_probability=None):
        """Classifies text, adjusts result vector to:
        a) ignore topics which categorize given text with probability belog minimum_probability
        b) take only 'dimension' topics from ordered array.
        Vector of possible themes is a list of tuples (theme id, suitability).
        Returns vector sorted by suitability descending.  
        """
        try:
            classified = self.model.get_document_topics(self._get_query(text), minimum_probability=minimum_probability)
        except Exception:
            classified = self.model[self._get_query(text)]
        topics = list(sorted(classified, key=lambda x: x[1], reverse=True))
        topics = topics[:dimension] if dimension else topics
        return list(map(lambda t: (t[0] if (self.algo == Algos.LDA) else t[0].item(), t[1].item()), topics))

    def get_all_topics(self, words=10):
        """Returns list of topics tuples.  """
        result = []
        topics = self.model.show_topics(self.ALGOS[self.algo]["topics"], num_words=words, log=False, formatted=False)
        for t in topics:
            entry = {
                "id": t[0],
                "words": sorted([
                    {"word": w[0], "value": w[1].item()} for w in t[1]
                ], key=lambda x: x["value"], reverse=True)
            }
            result.append(entry)

        return result
    
    def _train_algo(self, algo, topics):
        """Trains Gensim library with selected algorithm, uses English Wikipedia dump.  """
        try:
            dictionary = gensim.corpora.Dictionary.load_from_text(os.path.join(self.PATH,
                                                                               self.ALGOS[algo]["dir"],
                                                                               self.WORD_IDS))
            mm = gensim.corpora.MmCorpus(os.path.join(self.PATH, self.ALGOS[algo]["dir"], self.TF_IDF))
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
        return func(corpus=mm, id2word=id2word, num_topics=topics)
    
    def _get_trained_algo(self, algo):
        """Loads trained data as object of given algorithm.  """
        try:
            path = os.path.join(self.PATH, self.ALGOS[algo]["dir"], "trained.{}".format(self.ALGOS[algo]["name"]))
            model = self.ALGOS[algo]["model"].load(path)
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
        return self.dictionary.doc2bow(wikicorpus.tokenize(wikicorpus.filter_wiki(text)))
    
    def _print_themes(self, themes):
        """Print suitable themes for debugging purpose. Delete before production.  """
        for theme in themes:
            print(str(theme[0]) + ": " + self.model.print_topic(theme[0]))


if __name__ == "__main__":
    gens = GensimAPI(algo=Algos.LSI, trained=True)
    """
    print(gens.classify_text('''The Pope is the Bishop of Rome and the leader of the worldwide Catholic Church.[3] 
        The importance of the Roman bishop is largely derived from his role as the traditional successor to Saint Peter, 
        to whom Jesus gave the keys of Heaven and the powers of "binding and loosing", 
        naming him as the "rock" upon which the church would be built. 
        The current pope is Francis, who was elected on 13 March 2013, succeeding Benedict XVI.
        '''))
    """
    print(gens.get_all_topics())

