#!/usr/bin/python

import utils.database
import sys
import nltk

class QueryAnalyzer:
    def __init__ (self):
        pass

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
        bigr = self.__get_bigrams (ns)
        if not vs:
            vs = ['*']
        for v in vs:
            for b in bigr:
                res.append ((b[0], v, b[1]))
        return res


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
        for i in range (len (np)):
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
