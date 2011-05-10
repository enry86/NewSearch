#!/usr/bin/python

import database


class ExpandDocs:

    def __init__ (self):
        self.db = database.DataBaseMysql ()

    def start_exp (self):
        docs = self.db.get_docs ()
        tris = self.db.get_triples ()
        for d, in docs:
            self.expand_doc (d, docs, tris)

    def expand_doc (self, d, docs, tris):
        tr_d = self.db.get_triples ((d))


def main ():
    exp = ExpandDocs ()
    exp.start_exp ()

if __name__ == '__main__':
    main ()
