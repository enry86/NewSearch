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
    doc, qry = qc.query_1 (3)
    print ':%s' % doc
    print qry