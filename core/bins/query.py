#!/usr/bin/python

import utils.database
import sys
import nltk
from bins import relations

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
        self.query.append (self.curr_q.get_query ())


class QueryManager:

    def __init__ (self):
        self.db = utils.database.DataBaseMysql ()
        self.stm = nltk.stem.PorterStemmer ()

    def run_query (self, sq):
        query = self.__analyze (sq)
        cs = relations.CompSimilarity ()
        res = cs.query_similarity (query)
        print len(res)
        return res

    def __analyze (self, q):
        res = list ()
        tok = q.split ()
        pos = nltk.pos_tag (tok)
        qry = self.__build_query (pos)
        qry_ent = self.__find_ent (qry)
        query_fin = self.__refine_qry (qry_ent)
        return query_fin

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
        return query

    def __find_ent (self, qry):
        res = list ()
        for q in qry:
            self.__find_ent_cmp (q[0])
            self.__find_ent_cmp (q[2])
            tri = (q[0], q[1], q[2])
            res.append (tri)
        return res

    def __find_ent_cmp (self, c):
        for i, t in enumerate (c):
            e = self.db.get_entity (t)
            if e != None:
                c[i] = '_nsid' + str (e)
            else:
                c[i] = self.stm.stem (t)


    def __refine_qry (self, qry):
        res = list ()
        id_t = '__query__'
        for q in qry:
            tmp_res = list ()
            subs = self.__set_cmp (q[0])
            objs = self.__set_cmp (q[2])
            verb = q[1]
            if not verb:
                verb = '*'
            if subs and objs:
                for s in subs:
                    for o in objs:
                        tmp_res.append ((id_t, s, verb, o))
            elif subs:
                for k, s in enumerate (subs):
                    tmp_res.append ((id_t, s, verb, '*'))
                    for o in subs [k + 1:]:
                        tmp_res.append ((id_t, s, verb, o))

            if tmp_res:
                res += tmp_res
        return res


    def __set_cmp (self, lst):
        res = list ()
        l_e, l_n = self.__extr_ent (lst)
        res += l_e
        res += l_n
        if len (l_n) > 1:
            res.append (' '.join (l_n))
        return res


    def __extr_ent (self, c):
        ents = list ()
        words = list ()
        for t in c:
            if t.startswith ('_nsid'):
                ents.append (t)
            else:
                words.append (t)
        return ents, words

    '''
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
        '''

def main (q):
    qan = QueryManager ()
    qan.run_query (q)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main (sys.argv[1])
    else:
        print 'Error: no query'
        sys.exit (1)
