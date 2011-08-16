#!/usr/bin/python

import utils.database
import sys
sys.path.append ('lib')

class QueryConstructor:
    def __init__ (self):
        self.db = utils.database.DataBaseMysql ()

    def query_1 (self, terms):
        doc = self.db.get_rand_doc () [0]
        kws = self.db.get_query_1 ((doc, terms))
        qry = ' '.join (map(lambda x: x[0], kws))
        return doc, qry


if __name__ == '__main__':
    qc = QueryConstructor ()
    for t in range (5):
        for i in range (50):
            doc, qry = qc.query_1 (t + 1)
            print '%s:%s:%d' % (qry, doc, t + 1)
