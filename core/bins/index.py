#!/usr/bin/python

'''
Adaptation and extension of hexastore indexing
'''

import utils.database
import time

class Index:

    def __init__ (self):
        self.dsov = dict ()
        self.do = dict ()

    def add_triple (self, tri):
        doc, idt, sub, vrb, obj = tri
        self.__add_dsov (doc, sub, vrb, obj)
        if obj != '__NONE':
            self.__add_do (doc, obj)


    def __add_dsov (self, doc, sub, vrb, obj):
        try:
            self.dsov [doc] [0] += 1
        except KeyError:
            self.dsov [doc] = [1, dict ()]
        curr = self.dsov[doc][1]
        try:
            curr [sub] [0] += 1
        except KeyError:
            curr [sub] = [1, dict ()]
        curr = curr [sub] [1]
        try:
            curr [obj] [0] += 1
        except KeyError:
            curr [obj] = [1, dict ()]
        curr = curr [obj] [1]
        try:
            curr [vrb] += 1
        except KeyError:
            curr [vrb] = 1



    def __add_do (self, doc, obj):
        try:
            self.do [doc] [0] += 1
        except KeyError:
            self.do [doc] = [0, dict ()]
        curr = self. do [doc] [1]
        try:
            curr [obj] += 1
        except KeyError:
            curr [obj] = 1


class IndexSimilarity:
    def __init__ (self, test, index):
        self.db = utils.database.DataBaseMysql ()
        self.test = test
        self.index = index

    def store_similarity (self):
        docs = self.db.get_docs ()
        for d1, in docs:
            if self.test:
                start = time.time ()
            for d2, in docs:
                if d1 != d2 and self.db.lookup_sim ((d1, d2, d2, d1)) == 0:
                    sim = self.__compute_sim (d1, d2)
                    self.db.insert_sim ((d1, d2, sim))
            if self.test:
                stop = time.time ()
                print 'relationship %f' % (stop - start)

    def __compute_sim (self, d1, d2):
        tri = self.db.get_doc_tri (d1)
        a = b = c = d = 0
        d = len (tri) + self.index.dsov [d2][0]
        for t in tri:
            tmp_a = self.__get_a_cnt (t, d2)
            tmp_b = self.__get_b_cnt (t, d2)
            tmp_c1 = self.__get_c1_cnt (t, d2)
            tmp_c2 = self.__get_c2_cnt (t, d2)
            a += tmp_a
            b += (tmp_b - tmp_a)
            c += ((tmp_c1 + tmp_c2) - (tmp_b + tmp_a))
        s1 = float (a) / float (d)
        s2 = float (b) / float (d - a)
        s3 = float (c) / float (d - a - b)
        res = s1 + (1 - s1) * (s2 + (1 - s2) * s3)
        return res

    def __get_a_cnt (self, t, d):
        i, s, v, o = t
        res = 0
        try:
            res = self.index.dsov [d][1][s][1][o][1][v]
        except KeyError:
            res = 0
        return res

    def __get_b_cnt (self, t, d):
        i, s, v, o = t
        res = 0
        try:
            res = self.index.dsov [d][1][s][1][o][0]
        except KeyError:
            res = 0
        return res

    def __get_c1_cnt (self, t, d):
        i, s, v, o = t
        res = 0
        try:
            res = self.index.dsov [d][1][s][0]
        except KeyError:
            res = 0
        return res

    def __get_c2_cnt (self, t, d):
        i, s, v, o = t
        res = 0
        try:
            res = self.index.do [d][1][o]
        except KeyError:
            res = 0
        return res



class Indexer:

    def __init__ (self, test):
        self.db = utils.database.DataBaseMysql ()
        self.test = test
        self.ind = Index ()

    def build_index (self):
        docs = self.db.get_docs ()
        for d, in docs:
            if self.test:
                start = time.time ()
            tris = self.db.get_doc_tri (d)
            for tri in tris:
                t = (d,) + tri
                self.ind.add_triple (t)
            if self.test:
                end = time.time ()
                print 'memo_indexing %f' % (end - start)
        return self.ind
