#!/usr/bin/python

import sqlite3
import MySQLdb

import mysqlsettings

class DbError (Exception):
    pass


class DataBaseSqlite:
    __insert_ent = 'insert into entities values (NULL, ?)'
    __lookup_ent = 'select id from entities where oc_id = ?'
    __insert_kws = 'insert into keywords values (?,?)'

    def __init__ (self, db_fn):
        self.db = db_fn


    def __start_connection(self):
        res = True
        try:
            self.con = sqlite3.connect(self.db)
        except Exception:
            res = False
        return res

    def insert_ent (self, ent):
        db_start = self.__start_connection ()
        if db_start:
            try:
                self.con.execute (self.__insert_ent, ent)
                self.con.commit ()
                self.con.close ()
            except sqlite3.IntegrityError:
                pass
        return db_start

    def insert_kws (self, kws):
        db_start = self.__start_connection ()
        if db_start:
            try:
                self.con.execute (self.__insert_kws, kws)
                self.con.commit ()
                self.con.close ()
            except sqlite3.IntegrityError:
                pass
        return db_start

    def lookup_ent (self, ent):
        res = -1
        db_start = self.__start_connection()
        if db_start:
            res = self.con.execute(self.__lookup_ent, ent)
            try:
                res = res.fetchone()[0]
            except TypeError:
                res = -1
            self.con.close()
        return res


class DataBaseMysql:
    __insert_ent = """insert into entities values (NULL, %s)"""
    __lookup_ent = """select id from entities where oc_id = %s"""
    __insert_kws = """insert into keywords values (%s, %s, %s, 1)"""
    __update_kws = """update keywords set count = count + 1 where id = %s and keyword = %s and docid = %s"""
    __insert_tri = """insert into triples values (NULL, %s, %s, %s, %s, 1)"""
    __update_tri = """update triples set count = count + 1 where subject = %s and verb = %s and object = %s and docid = %s"""

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
        return self.__insert_dupl (self.__insert_tri, self.__update_tri, tri)

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


    def lookup_ent (self, ent):
        res = -1
        db_start = self.__start_connection ()
        if db_start:
            self.cur.execute (self.__lookup_ent, ent)
            res = self.cur.fetchone () [0]
            self.cur.close ()
        return res
