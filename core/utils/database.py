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

    __retr_sim_tri = """insert into tmp_score (select %s, rel.triple, rel.tot / total.cnt as score from \
(select triple, count(docid) as tot from docs where docid in \
(select distinct docid from docs where triple = %s) and docid != %s group by triple having tot > 1) as rel, \
(select count(*) as cnt from (select distinct docid from docs) as d) as total)"""


    __query_ent = """select   k.id, sum(k.count)/t.total as score from keywords k, (select sum(count) as total from keywords where keyword like "%%%s%%") as t where keyword like "%%%s%%" group by k.id order by score desc"""

    __create_tmp = """create temporary table tmp_score (tri_or integer, tri_ds integer, score numeric(5,4))"""


    def __init__ (self):
        self.user = mysqlsettings.MYSQL_USER
        self.passwd = mysqlsettings.MYSQL_PASSWD
        self.db = mysqlsettings.MYSQL_DB
        self.host = mysqlsettings.MYSQL_HOST


    def __start_connection (self):
        res =  True
        try:
            self.con = MySQLdb.connect (user = self.user, passwd = self.passwd, host = self.host, db = self.db)
            self.cur = self.con.cursor ();
        except MySQLdb.Error:
            res = False
        return res

    def insert_pin (self, pin):
        res = True
        db_start = self.__start_connection ()
        if db_start:
            try:
                self.cur.execute (self.__insert_pin, pin)
                self.con.commit ()
                self.cur.close ()
            except MySQLdb.IntegrityError, m:
                res = False
        else:
            res = False
        return res


    def insert_ent (self, ent):
        res = self.__start_connection ()
        if res:
            try:
                self.cur.execute (self.__insert_ent, ent)
                self.con.commit ()
                self.cur.close ()
            except MySQLdb.IntegrityError:
                pass
        return res


    def insert_kws (self, kws):
        return self.__insert_dupl (self.__insert_kws, self.__update_kws, kws)


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
                self.cur.close ()
            except MySQLdb.IntegrityError:
                pass


    def __insert_dupl (self, query_ins, query_upd, vals):
        res = self.__start_connection ()
        if res:
            try:
                self.cur.execute (query_ins, vals)
                self.con.commit ()
                self.cur.close ()
            except MySQLdb.IntegrityError:
                try:
                    self.cur.execute (query_upd, vals)
                    self.con.commit ()
                    self.cur.close ()
                except MySQLdb.Error:
                    res = False
        return res

    def lookup_tri (self, tri):
        res = -1
        db_start = self.__start_connection ()
        if db_start:
            self.cur.execute (self.__lookup_tri, tri)
            data = self.cur.fetchone ()
            self.cur.close ()
            if data:
                res = data [0]
        return res


    def lookup_ent (self, ent):
        res = -1
        db_start = self.__start_connection ()
        if db_start:
            self.cur.execute (self.__lookup_ent, ent)
            res = self.cur.fetchone () [0]
            self.cur.close ()
        return res


    def get_entity (self, kw):
        res = None
        db_start = self.__start_connection ()
        if db_start:
            query = self.__query_ent % (kw, kw,)
            self.cur.execute (query)
            scr = self.cur.fetchone ()
            self.cur.close ()
            if scr:
                res = int (scr [0])
        return res

    def get_docs (self):
        res = None
        db_start = self.__start_connection ()
        if db_start:
            self.cur.execute (self.__retr_docs)
            res = self.cur.fetchall ()
            self.cur.close ()
        return res


    def get_triples_doc (self, doc):
        res = None
        db_start = self.__start_connection ()
        if db_start:
            self.cur.execute (self.retr_triples, doc)
            res = self.cur.fetchall ()
            self.cut.close ()
        return res


    def store_scores (self, doc, tri, param):
        res = True
        db_start = self.__start_connection ()
        if db_start:
            self.cur.execute (self.__create_tmp)
            self.con.commit ()
            for t in tri:
                val = (tri, tri, doc,)
                self.cur.execute (self.__retr_sim_tri, val)
            self.con.commit ()
            self.__store_best (param)
            self.cur.close ()
            res = True
        return res

    def __store_best (self, param):
