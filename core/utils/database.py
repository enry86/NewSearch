#!/usr/bin/python

import MySQLdb
import mysqlsettings

class DataBaseMysql:
    __insert_ent = """insert into entities values (NULL, %s)"""
    __lookup_ent = """select id from entities where oc_id = %s"""
    __insert_kws = """insert into keywords values (%s, %s, %s, 1)"""
    __update_kws = """update keywords set count = count + 1 where id = %s and keyword = %s and docid = %s"""
    __lookup_tri = """select id from triples where subject = %s and verb = %s and object = %s"""
    __insert_tri = """insert into triples values (NULL, %s, %s, %s)"""
    __insert_doc = """insert into docs values (%s, %s, 1)"""
    __update_doc = """update docs set count = count + 1 where docid = %s and triple = %s"""
    __insert_pin = """insert into pages_index values (%s, NOW())"""
    __retr_triples_doc = """select triple from docs where docid = %s"""
    __get_tri_doc = """select d.triple, t.subject, t.verb, t.object from docs d, triples t where t.id = d.triple and d.docid = %s"""
    __lookup_sim = """select count(*) from doc_sim where (doc1 = %s and doc2=%s) or (doc1=%s and doc2=%s)"""
    __insert_sim = """insert into doc_sim values (%s, %s, %s)"""
    __get_docids = """select distinct docid from docs"""

    __retr_sim_tri = """insert into tmp_score (select %s, rel.triple, TRUNCATE(rel.tot / total.cnt, 10) as score from \
(select triple, count(docid) as tot from docs where docid in \
(select distinct docid from docs where triple = %s) and docid != %s group by triple having tot > 1) as rel, \
(select count(*) as cnt from (select distinct docid from docs) as d) as total where rel.triple != %s)"""

    #using 1 instead of count(t1.tri_or) to avoid out of scale scores due to highly overlapping related document sets
    __get_rnk_tri = """select t1.tri_ds, TRUNCATE(sum(t1.score) * (1 / t.tot), 10) as score  from tmp_score as t1, \
(select count(triple) as tot, docid from docs where  docid = %s) as t group by t1.tri_ds order by score desc"""


    __store_exp = """insert into expansion values (%s, %s, %s)"""
    __lookup_tri_doc = """select count(*) from docs where triple = %s and docid = %s"""

    __query_ent = """select   k.id, sum(k.count)/t.total as score from keywords k, (select sum(count) as total from keywords where keyword like "%%%s%%") as t where keyword like "%%%s%%" group by k.id order by score desc"""

    __create_tmp = """create temporary table tmp_score (tri_or integer, tri_ds integer, score numeric(11,10))"""

    #QUERY ANSWERING
    __get_all_triples = """select * from triples"""
    __tmp_query_result = """create temporary table tmp_query (tri integer, score numeric(11,10))"""
    __insert_tmp_query = """insert into tmp_query values (%s, %s)"""
    __rank_docs = """select d.docid, avg(tmp.score) as rel from docs d, tmp_query tmp where d.triple = tmp.tri group by d.docid having rel > 0 order by rel desc"""

    #WORD COUNTING
    __insert_cnt = """insert into word_count values (%s, %s)"""
    __update_cnt = """update word_count set count = count + %s where word = %s"""


    def __init__ (self):
        self.user = mysqlsettings.MYSQL_USER
        self.passwd = mysqlsettings.MYSQL_PASSWD
        self.db = mysqlsettings.MYSQL_DB
        self.host = mysqlsettings.MYSQL_HOST
        self.db_up = False
        self.__start_connection ()



    def close_con (self):
        self.con.close ()


    def __start_connection (self):
        res =  True
        if self.db_up:
            res = True
        else:
            try:
                self.con = MySQLdb.connect (user = self.user, passwd = self.passwd, host = self.host, db = self.db)
                self.cur = self.con.cursor ();
                self.db_up = True
            except MySQLdb.Error:
                res = False
        return res



    def __insert_dupl (self, query_ins, query_upd, vals):
        res = self.__start_connection ()
        if res:
            try:
                self.cur.execute (query_ins, vals)
                self.con.commit ()
                #self.cur.close ()
            except MySQLdb.IntegrityError:
                try:
                    self.cur.execute (query_upd, vals)
                    self.con.commit ()
                    #self.cur.close ()
                except MySQLdb.Error:
                    res = False
        return res

    def __insert_uni (self, query, vals):
        res = True
        db_start = self.__start_connection ()
        if db_start:
            try:
                self.cur.execute (query, vals)
                self.con.commit ()
                #self.cur.close ()
            except MySQLdb.IntegrityError, m:
                print m
                res = False
        else:
            res = False
        return res

    def __insert_uni_true (self, query, vals):
        res = self.__start_connection ()
        if res:
            try:
                self.cur.execute (query, vals)
                self.con.commit ()
                #self.cur.close ()
            except MySQLdb.IntegrityError:
                pass
        return res


    def insert_ent (self, ent):
        return self.__insert_uni_true (self.__insert_ent, ent)


    def insert_kws (self, kws):
        return self.__insert_dupl (self.__insert_kws, self.__update_kws, kws)


    def insert_pin (self, pin):
        return self.__insert_uni (self.__insert_pin, pin)


    def insert_sim (self, sim):
        return self.__insert_uni (self.__insert_sim, sim)


    def insert_tmp_query (self, tmpq):
        res = True
        try:
            self.cur.execute (self.__insert_tmp_query, tmpq)
            self.con.commit ()
        except MySQLdb.Error, m:
            print m
            res = False
        return res

    def insert_many_tri (self, tris):
        for t in tris:
            self.insert_tri (t)

    def insert_tri (self, tri):
        val_t = (tri[0], tri[1], tri[2])
        self.__ins_tri (val_t)
        id_t = self.lookup_tri (val_t)
        val_d = (tri[3], id_t)
        if val_d >= 0:
            res = self.__insert_dupl (self.__insert_doc, self.__update_doc, val_d)
        else:
            print 'ERROR: Cannot store triple'
            res = False
        return res


    def __ins_tri (self, tri):
        db_s = self.__start_connection ()
        if db_s:
            try:
                self.cur.execute (self.__insert_tri, tri)
                self.con.commit ()
                #self.cur.close ()
            except MySQLdb.IntegrityError:
                pass


    def __lookup_val (self, query, val):
        res = -1
        db_start = self.__start_connection ()
        if db_start:
            self.cur.execute (query, val)
            try:
                res = self.cur.fetchone () [0]
            except TypeError:
                res = -1
            #self.cur.close ()
        return res



    def lookup_tri (self, tri):
        return self.__lookup_val (self.__lookup_tri, tri)


    def lookup_ent (self, ent):
        return self.__lookup_val (self.__lookup_ent, ent)


    def lookup_sim (self, docs):
        return self.__lookup_val (self.__lookup_sim, docs)


    def rank_docs_query (self):
        res = list ()
        try:
            self.cur.execute (self.__rank_docs)
            res = self.cur.fetchall ()
            #self.cur.close ()
        except MySQLdb.Error, m:
            print m
            res = list ()
        return res


    def __get_all (self, query):
        res = list ()
        db_start = self.__start_connection ()
        if db_start:
            self.cur.execute (query)
            res = self.cur.fetchall ()
            #self.con.close ()
        return res


    def get_entity (self, kw):
        res = None
        db_start = self.__start_connection ()
        if db_start:
            query = self.__query_ent % (kw, kw,)
            self.cur.execute (query)
            res = self.cur.fetchall ()
            #self.cur.close ()
        return res

    def __get_all_query (self, query, val):
        res = list ()
        db_start = self.__start_connection ()
        if db_start:
            self.cur.execute (query, val)
            res = self.cur.fetchall ()
            #self.cur.close ()
        return res

    def get_docs (self):
        return self.__get_all (self.__get_docids)


    def get_triples (self):
        return self.__get_all (self.__get_all_triples)


    def get_triples_doc (self, doc):
        return self.__get_all_query (self.__retr_triples_doc, doc)


    def get_doc_tri (self, doc):
        return self.__get_all_query (self.__get_tri_doc, doc)


    def create_tmp_query (self):
        res = True
        db_start = self.__start_connection ()
        if db_start:
            try:
                self.cur.execute (self.__tmp_query_result)
                self.con.commit ()
            except MySQLdb.Error:
                res = False
        return res



    def store_scores (self, doc, tri, size):
        res = False
        db_start = self.__start_connection ()
        if db_start:
            print 'Expandind doc %s with %d triples' % (doc, size)
            self.cur.execute (self.__create_tmp)
            self.con.commit ()
            for t in tri:
                val = (t[0], t[0], doc, t[0])
                self.cur.execute (self.__retr_sim_tri, val)
            self.con.commit ()
            self.__store_best (size, doc, tri)
            #self.cur.close ()
            res = True
        return res

    def __store_best (self, size, doc, triples):
        self.cur.execute (self.__get_rnk_tri, (doc,))
        res = self.cur.fetchall ()
        cnt = 0
        queries = list ()
        while cnt < len(res) and cnt < size:
            tri = res[cnt][0]
            scr = res[cnt][1]
            if not (tri) in triples:
                queries.append ((doc, tri, scr,))
                cnt += 1
        try:
            self.cur.executemany (self.__store_exp, queries)
        except MySQLdb.IntegrityError:
            print 'Document %s already expanded' % doc
        self.con.commit ()

    def __lu_tri_doc (self, val):
        res = 0
        self.cur.execute (self.__lookup_tri_doc, val)
        tmp = self.cur.fetchone ()
        try:
            res = tmp[0]
        except TypeError:
            res = False
        return res


    def update_wcount (self, cnt):
        return self.__insert_dupl (self.__insert_cnt, self.__update_cnt, cnt)
