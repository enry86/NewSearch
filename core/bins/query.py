#!/usr/bin/python

import utils.database
import sys
import nltk

class Query:
    def __init__ (self):
        self.__su = list ()
        self.__ob = list ()
        self.__vb = str ()

    def add_left (self, l):
        self.__su.append (l)

    def add_right (self, r):
        self.__ob.append (r)

    def set_verb (self, v):
        self.__vb = v

    def get_left (self):
        return self.__su

    def get_right (self):
        return self.__ob

    def get_query (self):
        return (self.__su, self.__vb, self.__ob)


class QueryParser:
    def __init__ (self):
        self.state = 0
        self.query = list ()

    def get_result (self):
        return self.query

    def found_noun (self, n):
        if self.state == 0:
            self.curr_q = Query ()
            self.curr_q.add_left (n)
            self.state = 1
        elif self.state == 1:
            self.curr_q.add_left (n)
        elif self.state == 2:
            self.curr_q.add_right (n)
            self.state = 3
        elif self.state == 3:
            self.curr_q.add_right (n)

    def found_verb (self, v):
        if self.state == 0:
            self.curr_q = Query ()
            self.set_verb (v)
            self.state = 2
        elif self.state == 1:
            self.curr_q.set_verb (v)
            self.state = 3
        elif self.state == 2:
            self.query.append (self.curr_q)
            self.state = 0
            self.found_verb (v)
        elif self.state == 3:
            self.query.append (self.curr_q)
            l = self.curr_q.get_right ()
            self.curr_q = Query ()
            self.curr_q.add_left (l)
            self.curr_q.set_verb (v)
            self.state = 2

    def end_query (self):
        self.query.append (self.curr_q)


class QueryAnalyzer:

    def __init__ (self):
        self.db = utils.database.DataBaseMysql ()
        self.stm = nltk.stem.PorterStemmer ()

    def analyze (self, q):
        res = list ()
        tok = q.split ()
        pos = nltk.pos_tag (tok)
        print pos
        self.__build_query (pos)
        print res

    '''
    def analyze (self, q):
        res = list ()
        subqs = q.split (';')
        for sq in subqs:
            sub_q = self.__get_triples (sq)
            res.append (sub_q)
        print res
        '''

    def __build_query (self, pos):
        prs = QueryParser ()
        for w, t in pos:
            if 'VB' in t:
                prs.found_verb (w)
            else:
                prs.found_noun (w)
        prs.end_query ()
        query = prs.get_result ()
        print query[0].get_query ()



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
