#!/usr/bin/python

import utils.database
import sys
import nltk
import time
from bins import relations
from bins import index

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
            self.curr_q.set_verb (v)
            self.state = 2
        elif self.state == 1:
            self.curr_q.set_verb (v)
            self.state = 3
        elif self.state == 2:
            self.query.append (self.curr_q.get_query ())
            self.state = 0
            self.found_verb (v)
        elif self.state == 3:
            self.query.append (self.curr_q.get_query ())
            l = self.curr_q.get_right ()
            if l:
                self.curr_q = Query ()
                for tok in l:
                    self.curr_q.add_left (tok)
                self.curr_q.set_verb (v)
                self.state = 2
            else:
                self.curr_q = Query ()
                self.state = 1

    def end_query (self):
        self.query.append (self.curr_q.get_query ())


class QueryManager:
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



    def __init__ (self, ind, test, hexa, db):
        #self.db = utils.database.DataBaseMysql ()
        self.db = db
        self.lem = nltk.stem.WordNetLemmatizer ()
        self.test = test
        if hexa:
            self.sim = index.IndexSimilarity (test, ind, db)
        else:
            self.sim = relations.CompSimilarity (test)

    def run_query (self, sq):
        start = time.time ()
        query = self.__analyze (sq)
        end = time.time ()
        res = self.sim.query_similarity (query)
        return res, (end - start), len (query)

    def __analyze (self, q):
        res = list ()
        tok = q.split ()
        tok = self.__rem_stopw (tok)
        pos = nltk.pos_tag (tok)
        qry = self.__build_query (pos)
        query_kw = self.__refine_qry (qry)
        query_fin = list ()
        for tri in query_kw:
            query_fin += self.__find_ent (tri)
            idt, s, v, o = tri
            s = self.lem.lemmatize (s)
            if v != '*':
                v = self.lem.lemmatize (v)
            if o != '*':
                o = self.lem.lemmatize (o)
            query_fin.append (('__query__', s, v, o))
        return query_fin

    def __rem_stopw (self, tok):
        res = list ()
        if len (tok) == 1:
            return tok
        else:
            for t in tok:
                if t not in self.stopw:
                    res.append (tok)
        if len (res) == 0:
            return tok
        else:
            return res


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

    def __find_ent (self, tri):
        res = list ()
        idt, s, v, o = tri
        #ents_s = self.db.get_entity (s)
        ents_s = self.sim.resolve_ent (s)
        if o != '*':
            #ents_o = self.db.get_entity (o)
            ents_o = self.sim.resolve_ent (o)
        else:
            ents_o = list ()
        if ents_s and ents_o:
            for e_s in ents_s:
                for e_o in ents_o:
                    sub = '_nsid' + str (e_s)
                    obj = '_nsid' + str (e_o)
                    res.append((idt, sub, v, obj))
        elif ents_s:
            for ent in ents_s:
                sub = '_nsid' + str (ent)
                res.append ((idt, sub, v, self.lem.lemmatize (o)))
        return res


    def __find_ent_cmp (self, c):
        ent_k = list ()
        for i, t in enumerate (c):
            e = self.db.get_entity (t)
            if e != None:
                c[i] = '_nsid' + str (e)
                ent_k.append (self.lem.lemmatize (t))
            else:
                c[i] = self.lem.lemmatize (t)
        c += ent_k


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
            if objs and not subs:
                tmp = objs
                objs = subs
                subs = tmp
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



def main (q):
    qan = QueryManager ()
    qan.run_query (q)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main (sys.argv[1])
    else:
        print 'Error: no query'
        sys.exit (1)
