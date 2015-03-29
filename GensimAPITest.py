'''
Created on 16.3.2015

@author: Jan Balaz
'''
import unittest
from GensimAPI import GensimAPI


class Test(unittest.TestCase):
       
    def test_classify_pope(self):
        gensim = GensimAPI()
        text1 = 'The Pope is the Bishop of Rome and the leader of the worldwide Catholic Church.[3] The importance of the Roman bishop is largely derived from his role as the traditional successor to Saint Peter, to whom Jesus gave the keys of Heaven and the powers of "binding and loosing", naming him as the "rock" upon which the church would be built. The current pope is Francis, who was elected on 13 March 2013, succeeding Benedict XVI.'
        themes = gensim.classify_text(text1)
        themes = [id for id, num in themes]
        self.assertEqual(themes, [14, 57, 64, 9, 2])
    
    def test_dimension(self):
        gensim = GensimAPI()
        text1 = 'The Pope is the Bishop of Rome and the leader of the worldwide Catholic Church.[3] The importance of the Roman bishop is largely derived from his role as the traditional successor to Saint Peter, to whom Jesus gave the keys of Heaven and the powers of "binding and loosing", naming him as the "rock" upon which the church would be built. The current pope is Francis, who was elected on 13 March 2013, succeeding Benedict XVI.'
        themes = gensim.classify_text(text1, dimension=3)
        themes = [id for id, num in themes]
        self.assertEqual(themes, [14, 57, 64])
    
    def test_classify_french(self):
        gensim = GensimAPI()
        text2 = 'French Paris Jean Jacques France French'
        themes = gensim.classify_text(text2)
        self.assertEqual(themes[0][0], 4)

if __name__ == "__main__":
    unittest.main()