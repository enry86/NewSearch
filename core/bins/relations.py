#!/usr/bin/python

import nltk.metrics.distance as distance
import utils.database

SUB = 0
VRB = 1
OBJ = 2
N_FACTOR = 0.45
V_FACTOR = 0.10

class CompSimilarity:

    def __init__ (self):
        self.db = utils.database.DataBaseMySql ()

    def compute_sim (self, d1, d2):
        t_d1 = self.db.get_doc_tri (d1)
        t_d2 = self.db.get_doc_tri (d2)
        sim = self.__get_similarity (t_d1, t_d2)
        return sim

    def __get_similarity (self, t_d1, t_d2):
        for t1 in t_d1:
            for t2 in t_d2:
                self.__sim_triple (t1, t2):

    def __sim_triple (self, t1, t2):
        ds1 = self.__get_dst (t1[SUB], t2[SUB])
        ds2 = self.__get_dst (t1[SUB], t2[OBJ])
        do1 = self.__get_dst (t1[OBJ], t2[OBJ])
        do2 = self.__get_dst (t1[OBJ], t2[SUB])
        dt1 = ds1 + do1
        dt2 = ds2 + do2
        dsn = min (dt1, dt2)
        dsv = self.__get_dst (t1[VRB], t2[VRB])
        res = (V_FACTOR * dsv) + (N_FACTOR * dsn)
        return res
