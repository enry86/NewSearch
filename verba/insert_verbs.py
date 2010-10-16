#!/usr/bin/python

import sys
import sqlite3

def main ():
    try:
        filename = sys.argv[1]
    except:
        sys.exit(1)
    in_f = open(filename, 'r')
    store_db(in_f, 'verbs.db')
    in_f.close()

def store_db (in_f, db):
    con = sqlite3.connect(db)
    sql = 'insert into verbs values ("%s")'
    for v in in_f:
        try:
            v = v.strip()
            con.execute(sql % v)
        except sqlite3.IntegrityError:
            pass
    con.commit()
    con.close()
    

if __name__ == '__main__':
    main()
