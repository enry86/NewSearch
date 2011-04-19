#!/usr/bin/python

import sqlite3

class DataBase:
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
            res = res.fetchone()[0]
            self.con.close()
        return res
