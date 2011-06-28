#!/usr/bin/python

import nltk.metrics.distance as distance
import utils.database

ID = 0
SUB = 1
VRB = 2
OBJ = 3
N_FACTOR = 0.45
V_FACTOR = 0.10

class CompSimilarity:

    def __init__ (self):
        self.db = utils.database.DataBaseMysql ()

    def store_similarity (self):
        docs = self.db.get_docs ()
        for d1, in docs:
            for d2, in docs:
                if d1 != d2 and self.db.lookup_sim ((d1, d2, d2, d1)) == 0:
                    sim = self.__compute_sim (d1, d2)
                    self.db.insert_sim ((d1, d2, sim))

    def query_similarity (self, query):
        tris = self.db.get_triples()
        self.db.create_tmp_query ()
        for t in tris:
            tmp_s = list ()
            for q in query:
                sim = self.__sim_triple (q, t)
                tmp_s.append (sim)
            sim_max = max (tmp_s)
            self.db.insert_tmp_query ((t[0], sim))
        res = self.db.rank_docs_query ()
        return res


    def __compute_sim (self, d1, d2):
        t_d1 = self.db.get_doc_tri (d1)
        t_d2 = self.db.get_doc_tri (d2)
        sim = self.__get_similarity (t_d1, t_d2)
        return sim

    def __get_similarity (self, t_d1, t_d2):
        scores = dict ()
        for t1 in t_d1:
            scores[t1[ID]] = 0
            for t2 in t_d2:
                scores[t1[ID]] += (self.__sim_triple (t1, t2) / float (len (t_d2)))
        v = scores.values ()
        return sum (v) / float (len (v))


    def __sim_triple (self, t1, t2):
        if t1[ID] == t2[ID]:
            return 1

        ds1 = self.__get_dst (t1[SUB], t2[SUB])
        ds2 = self.__get_dst (t1[SUB], t2[OBJ])
        do1 = self.__get_dst (t1[OBJ], t2[OBJ])
        do2 = self.__get_dst (t1[OBJ], t2[SUB])

        if t1[SUB] == '*':
            ds1 = do1
        elif t1[OBJ] == '*':
            ds2 = do2

        sim_s1 = self.__get_sim (ds1)
        sim_o1 = self.__get_sim (do1)
        sim_s2 = self.__get_sim (ds2)
        sim_o2 = self.__get_sim (do2)
        simn = max (sim_s1 + sim_o1, sim_s2 + sim_o2)

        dsv = self.__get_dst (t1[VRB], t2[VRB])
        try:
            simv = 1 / (dsv + 1)
        except TypeError:
            simv = 0
        if t1[VRB] == '*':
            simv = simn
        res = (V_FACTOR * simv) + (N_FACTOR * simn)
        return res

    def __get_sim (self, dis):
        res = 0
        try:
            res = 1.0 / (dis + 1)
        except TypeError:
            res = 0
        return res


    def __get_dst (self, s1, s2):
        res = None
        if self.__is_ent (s1) | self.__is_ent (s2):
            if s1 == s2:
                res = 0
            else:
                res = None
        elif self.__is_none (s1) | self.__is_none (s2):
            res = None
        else:
            res = distance.edit_distance (s1, s2)
        return res

    def __is_ent (self, s):
        return s.startswith('_nsid')

    def __is_none (self, s):
        return s == '__NONE'
