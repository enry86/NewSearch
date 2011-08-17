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

    def query_2 (self, terms):
        qry = str ();
        doc = self.db.get_rand_doc () [0]
        tri = self.db.get_tri_q2 ((doc, terms))
        for s, v, o in tri:
            if s.startswith ('_nsid'):
                s = self.__resolve_kw (s) [0]
            if o.startswith ('_nsid'):
                o = self.__resolve_kw (o) [0]
            vt = v.split ()
            tmp_v = str ()
            for t in vt:
                if '_nsid' not in t:
                    tmp_v += ' ' + t

            if tmp_v:
                v = tmp_v.strip ()
            elif '_nsid' in v:
                v = str ()
            qry += '%s %s %s ' % (s, v, o)
        qry = qry.replace ('__NONE', '')
        return doc, qry.strip ()


    def query_3 (self, terms):
        qry = str ();
        doc = self.db.get_rand_doc () [0]
        tri = self.db.get_tri_q2 ((doc, terms))
        for s, v, o in tri:
            if s.startswith ('_nsid'):
                s = self.__resolve_kw (s, doc) [0]
            if o.startswith ('_nsid'):
                o = self.__resolve_kw (o, doc) [0]
            vt = v.split ()
            tmp_v = str ()
            for t in vt:
                if '_nsid' not in t:
                    tmp_v += ' ' + t

            if tmp_v:
                v = tmp_v.strip ()
            elif '_nsid' in v:
                v = str ()
            qry += '%s %s %s ' % (s, v, o)
        qry = qry.replace ('__NONE', '')
        return doc, qry.strip ()



    def __resolve_kw (self, ent, doc = None):
        i = int (ent.replace ('_nsid', ''))
        if doc:
            kw = self.db.get_kws_q3 ((i, doc)) [0]
        else:
            kw = self.db.get_kws_q2 ((i)) [0]
        return kw


if __name__ == '__main__':
    mode = sys.argv [1]
    qc = QueryConstructor ()
    if mode == '1':
        for t in range (5):
            for i in range (50):
                doc, qry = qc.query_1 (t + 1)
                print '%s:%s:%d' % (qry, doc, t + 1)
    elif mode == '2':
        for t in range (3):
            for i in range (70):
                doc, qry = qc.query_2 (t + 1)
                print '%s:%s:%d' % (qry, doc, t + 1)
    elif mode == '3':
        for t in range (3):
            for i in range (70):
                doc, qry = qc.query_3 (t + 1)
                print '%s:%s:%d' % (qry, doc, t + 1)
