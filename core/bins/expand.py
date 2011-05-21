#!/usr/bin/python

import utils.database


class ExpandDocs:
    __PARAM = 0.50

    def __init__ (self):
        self.db = utils.database.DataBaseMysql ()

    def start_exp (self):
        docs = self.db.get_docs ()
        for d, in docs:
            self.expand_doc (d)

    def expand_doc (self, d):
        tr_d = self.db.get_triples_doc ((d))
        size = int (len (tr_d) * self.__PARAM)
        self.db.store_scores (d, tr_d, size)


def main ():
    exp = ExpandDocs ()
    exp.start_exp ()

if __name__ == '__main__':
    main ()
