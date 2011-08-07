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
        self.sovd = dict ()
        self.od = dict ()
        self.sod = dict ()
        self.sd = dict ()
        self.svd = dict ()

    def add_triple (self, tri):
        doc, idt, sub, vrb, obj = tri
        sub = sub.strip ()
        vrb = vrb.strip ()
        obj = obj.strip ()
        self.__add_dsov (doc, sub, vrb, obj)
        self.__add_sovd (doc, sub, vrb, obj)
        self.__add_sod (doc, sub, obj)
        self.__add_sd (doc, sub)
        if obj != '__NONE':
            self.__add_do (doc, obj)
            self.__add_od (doc, obj)


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

    def __add_sovd (self, doc, sub, vrb, obj):
        try:
            self.sovd [sub] [0] += 1
        except KeyError:
            self.sovd [sub] = [1, dict ()]
        curr = self.sovd [sub] [1]
        try:
            curr [obj] [0] += 1
        except KeyError:
            curr [obj] = [1, dict ()]
        curr = curr [obj] [1]
        try:
            curr [vrb] [0] += 1
        except KeyError:
            curr [vrb] = [1, dict ()]
        curr = curr [vrb] [1]
        try:
            curr [doc] += 1
        except KeyError:
            curr [doc] = 1

    def __add_sod (self, doc, sub, obj):
        try:
            self.sod [sub] [0] += 1
        except KeyError:
            self.sod [sub] = [1, dict ()]
        curr = self.sod [sub] [1]
        try:
            curr [obj] [0] += 1
        except KeyError:
            curr [obj] = [1, dict ()]
        curr = curr [obj] [1]
        try:
            curr [doc] += 1
        except KeyError:
            curr [doc] = 1

    def __add_svd (self, doc, sub, vrb):
        try:
            self.sod [sub] [0] += 1
        except KeyError:
            self.sod [sub] = [1, dict ()]
        curr = self.sod [sub] [1]
        try:
            curr [vrb] [0] += 1
        except KeyError:
            curr [vrb] = [1, dict ()]
        curr = curr [vrb] [1]
        try:
            curr [doc] += 1
        except KeyError:
            curr [doc] = 1

    def __add_sd (self, doc, sub):
        try:
            self.sd [sub] [0] += 1
        except KeyError:
            self.sd [sub] = [1, dict ()]
        curr = self.sd [sub] [1]
        try:
            curr [doc] += 1
        except KeyError:
            curr [doc] = 1



    def __add_od (self, doc, obj):
        try:
            self.od [obj] [0] += 1
        except KeyError:
            self.od [obj] = [1, dict ()]
        curr = self.od [obj] [1]
        try:
            curr [doc] += 1
        except KeyError:
            curr [doc] = 1


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
        self.docs = self.db.get_docs ()
        self.tot_d = len (self.docs)
        self.test = test
        self.index = index

    def query_similarity (self, query):
        tmp_res = dict ()
        for q in query:
            q_res = self.__compute_qsim (q)
            self.__add_tmp_res (q_res, tmp_res)
        res = self.__get_results (tmp_res)
        return res

    def store_similarity (self):
        for d1, in self.docs:
            if self.test:
                start = time.time ()
            for d2, in self.docs:
                if d1 != d2 and self.db.lookup_sim ((d1, d2, d2, d1)) == 0:
                    sim = self.__compute_sim (d1, d2)
                    self.db.insert_sim ((d1, d2, sim))
            if self.test:
                stop = time.time ()
                print 'relationship %f' % (stop - start)

    def __compute_qsim (self, q):
        res = dict ()
        a_res = self.__get_a_res (q)
        self.__add_a_res (res, a_res)
        b_res = self.__get_b_res (q)
        self.__add_b_res (res, b_res)
        c_res = self.__get_c_res (q)
        self.__add_c_res (res, c_res)
        return res

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

    def __get_a_res (self, q):
        i, s, v, o = q
        docs_a = dict ()
        docs_b = dict ()
        cnt_a = 0
        cnt_b = 0
        try:
            if v == '*' and o == '*':
                docs_a = self.index.sd [s][1]
                cnt_a = self.index.sd [s][0]
            elif v == '*':
                docs_a = self.index.sod [s][1][o][1]
                cnt_a = self.index.sod [s][1][o][0]
            elif o == '*':
                docs_a = self.index.svd [s][1][v][1]
                cnt_a = self.index.svd [s][1][v][0]
            else:
                docs_a = self.index.sovd [s][1][o][1][v][1]
                cnt_a = self.index.sovd [s][1][o][1][v][0]
        except KeyError:
            cnt_a = 0
        if o != '*':
            try:
                if v == '*':
                    docs_b = self.index.sod [o][1][s][1]
                    cnt_b = self.index.sod [o][1][s][0]
                else:
                    docs_b = self.index.sovd [o][1][s][1][v][1]
                    cnt_b = self.index.sovd [o][1][s][1][v][0]
            except KeyError:
                cnt_b = 0
        if cnt_b > cnt_a:
            docs_a = docs_b
        return docs_a

    def __add_a_res (self, store, t_res):
        self.__add_t_res (store, t_res, 0)


    def __get_b_cnt (self, t, d):
        i, s, v, o = t
        res = 0
        try:
            res = self.index.dsov [d][1][s][1][o][0]
        except KeyError:
            res = 0
        return res

    def __get_b_res (self, q):
        i, s, v, o = q
        docs_a = dict ()
        docs_b = dict ()
        cnt_a = 0
        cnt_b = 0
        try:
            if o == '*':
                docs_a = self.index.sd [s][1]
                cnt_a = self.index.sd [s][0]
            else:
                docs_a = self.index.sod [s][1][o][1]
                cnt_a = self.index.sod [s][1][o][0]
        except KeyError:
            cnt_a = 0
        if o != '*':
            try:
                docs_b = self.index.sod [o][1][s][1]
                cnt_b = self.index.sod [o][1][s][0]
            except KeyError:
                cnt_b = 0
        if cnt_b > cnt_a:
            docs_a = docs_b
        return docs_a

    def __add_b_res (self, store, t_res):
        self.__add_t_res (store, t_res, 1)


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

    def __get_c_res (self, q):
        i, s, v, o = q
        docs_s1 = dict ()
        docs_s2 = dict ()
        docs_o1 = dict ()
        docs_o2 = dict ()
        try:
            docs_s1 = self.index.sd [s][1]
        except KeyError:
            pass
        if o != '*':
            try:
                docs_s2 = self.index.sd [o][1]
                print docs_s2
            except KeyError:
                pass
            try:
                docs_o1 = self.index.od [o][1]
            except KeyError:
                pass
        try:
            docs_o2 = self.index.od [s][1]
        except KeyError:
            pass
        print len (docs_s1), len (docs_s2), len (docs_o1), len (docs_o2)
        docs = dict ()
        self.__merge_res (docs, docs_s1)
        self.__merge_res (docs, docs_s2)
        self.__merge_res (docs, docs_o1)
        self.__merge_res (docs, docs_o2)
        return docs


    def __merge_res (self, dst, src):
        for d in src:
            try:
                dst [d] += src [d]
            except KeyError:
                dst [d] = src [d]


    def __add_c_res (self, store, t_res):
        self.__add_t_res (store, t_res, 2)


    def __add_tmp_res (self, q_store, tmp_store):
        for k in q_store:
            q_res = q_store [k]
            q_res[1] -= q_res[0]
            q_res[2] -= (q_res[0] + q_res[1])
            try:
                tmp_store [k].append (q_res)
            except KeyError:
                tmp_store [k] = list ()
                tmp_store [k].append (q_res)

    def __get_results (self, tmp_store):
        res = list ()
        sub_l = lambda r, i: r[i]
        for doc in tmp_store:
            d_res = tmp_store [doc]
            d_tot = len (d_res)
            a_lst = map (lambda x: sub_l (x, 0), d_res)
            b_lst = map (lambda x: sub_l (x, 1), d_res)
            c_lst = map (lambda x: sub_l (x, 2), d_res)
            a = float (sum (a_lst)) / d_tot
            b = float (sum (b_lst)) / d_tot
            c = float (sum (c_lst)) / d_tot
            d = self.index.dsov [doc][0]
            s1 = float (a) / float (d)
            s2 = float (b) / float (d - a)
            s3 = float (c) / float (d - a - b)
            #print a, b, c, d
            score = s1 + (1 - s1) * (s2 + (1 - s2) * s3)
            res.append ((score, doc))
        return res


    def __add_t_res (self, store, t_res, i):
        for k in t_res:
            try:
                store [k] [i] = t_res [k]
            except KeyError:
                store [k] = [0, 0, 0]
                store [k] [i] = t_res [k]

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
                #self.ind.add_triple (self.__flip (t))
            if self.test:
                end = time.time ()
                print 'memo_indexing %f' % (end - start)
        return self.ind

    def __flip (self, tri):
        d, i, s, v, o = tri
        return (d, i, o, v, s)
