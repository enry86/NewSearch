#!/usr/bin/python

from collections import defaultdict
from utils import database
import sys

class WordCount:
    stopw = ['a','able','about','across','after','all','almost','also',\
                 'am','among','an','and','any','are','as','at','be','because',\
                 'been','but','by','can','cannot','could','dear','did','do',\
                 'does','either','else','ever','every','for','from','get','got',\
                 'had','has','have','he','her','hers','him','his','how','however',\
                 'i','if','in','into','is','it','its','just','least','let','like',\
                 'likely','may','me','might','most','must','my','neither','no',\
                 'nor','not','of','off','often','on','only','or','other','our',\
                 'own','rather','said','say','says','she','should','since','so',\
                 'some','than','that','the','their','them','then','there','these',\
                 'they','this','tis','to','too','twas','us','wants','was','we',\
                 'were','what','when','where','which','while','who','whom','why',\
                 'will','with','would','yet','you','your',"'s",',']


    def __init__ (self, files):
        self.files = files
        self.db = database.DataBaseMysql ()

    def count (self):
        for f in self.files:
            in_f = open (f)
            cont = in_f.read ()
            in_f.close ()
            self.__word_count (cont)

    def __word_count (self, cont):
        counter = defaultdict (int)
        chars = """\!,;:'"#\/()*_|."""
        for c in chars:
            cont = cont.replace (c, '')
        cont = cont.replace ('<p>', '\n')
        cont = cont.replace ('</p>', '\n')
        words = cont.split ()
        for w in words:
            w = w.lower ()
            if w not in self.stopw:
                counter[w] += 1
        self.__store_cnt (counter)

    def __store_cnt (self, cnt):
        for c in cnt:
            self.db.update_wcount ((cnt[c], c))

def main ():
    files = sys.argv [1:]
    wc = WordCount (files)
    wc.count ()

if __name__ == '__main__':
    main ()
