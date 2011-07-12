#!/usr/bin/python

'''
Adaptation and extension of hexastore indexing
'''

import utils.database

class Index:

    def __init__ (self):
        self.dsov = dict ()
        self.do = dict ()

    def add_triple (self, tri):
        doc, idt, sub, vrb, obj = tri
        self.__add_dsov (doc, sub, vrb, obj)
        self.__add_do (doc, obj)

    def __init_entry (self, dic, ent, cnt):
        if cnt:
            dic [ent] = 1
        else:
            dic [ent] = [1, dict ()]

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



class Indexer:

    def __init__ (self):
        self.db = utils.database.DataBaseMysql ()
        self.ind = Index ()

    def build_index (self):
        docs = self.db.get_docs ()
        for d, in docs:
            tris = self.db.get_doc_tri (d)
            for tri in tris:
                t = (d,) + tri
                self.ind.add_triple (t)
        return self.ind
