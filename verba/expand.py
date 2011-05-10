#!/usr/bin/python

import database


class ExpandDocs:

    def __init__ (self):
        self.db = database.DataBaseMysql ()

def main ():
    exp = ExpandDocs ()

if __name__ == '__main__':
    main ()
