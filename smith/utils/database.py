#!/usr/bin/python

'''
Interface to the database
'''

import sqlite3
import threading

class DataBase:
    __lookup_page = 'select count(*) from pages where url = ?'
    __insert_page = "insert into pages values (?,?,datetime('now'))"

    def __init__ (self, file_db):
        self.db = file_db
        self.db_sem = threading.Semaphore(1)

    def __start_connection(self):
        res = True
        try:
            self.con = sqlite3.connect(self.db)
        except Exception:
            res = False
        return res

    def insert_ent (self, values):
        db_start = self.__start_connection ()
        if db_start:
            self.con.execute (self.__insert_page, values)
            self.con.commit ()
            self.con.close ()
        return db_start

    def lookup_ent (self, page):
        count = 0
        db_start = self.__start_connection()
        if db_start:
            res = self.con.execute(self.__lookup_page, page)
            count = res.fetchone()[0]
            self.con.close()
        return count
