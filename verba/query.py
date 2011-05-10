#!/usr/bin/python

import utils.database
import sys
import nltk

class QueryAnalyzer:

    def __init__ (self):
        self.db = utils.database.DataBaseMysql ()
        self.stm = nltk.stem.PorterStemmer ()

    def analyze (self, q):
        res = list ()
        subqs = q.split (';')
        for sq in subqs:
            sub_q = self.__get_triples (sq)
            res.append (sub_q)
        print res

    def __get_triples (self, sq):
        res = list ()
        ws = sq.split ()
        ps = nltk.pos_tag (ws)
        vs, ns = self.__isolate_verbs (ps)
        is_ent = self.__get_entities (ns)
        bigr = self.__get_bigrams (ns)
        if not vs:
            vs = ['*']
        for v in vs:
            for b in bigr:
                v = self.stm.stem (v)
                res.append ((b[0], v, b[1]))
        return res

    def __get_entities (self, np):
        for i, n in enumerate (np):
            e = self.db.get_entity (n)
            if e != None:
                np[i] = '_nsid' + str (e)
            else:
                np[i] = self.stm.stem (np[i])


    def __isolate_verbs (self, ps):
        verbs = list ()
        nouns = list ()
        for t in ps:
            if 'VB' in t[1]:
                verbs.append (t[0])
            else:
                nouns.append (t[0])
        return verbs, nouns

    def __get_bigrams (self, np):
        res = list ()
        for i in range (len (np) - 1):
            if i < len (np) - 1:
                res.append ((np[i], np[i + 1]))
            else:
                res.append ((np[i], '*'))
        return res


def main (q):
    qan = QueryAnalyzer ()
    qan.analyze (q)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main (sys.argv[1])
    else:
        print 'Error: no query'
        sys.exit (1)