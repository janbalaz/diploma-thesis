'''
Created on 16.3.2015

@author: Jan Balaz
'''
import unittest
from GensimAPI import GensimAPI


class Test(unittest.TestCase):
    
    def setUp(self):
        self.gensim = GensimAPI()
        self.gensim.train_algo('lda', 100)


    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()