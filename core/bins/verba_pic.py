#!/usr/bin/python

'''
Verba

usage:
./verba_pic.py [OPTIONS]

Options:
    -i  input dir
    -o  output dir
    -c  graph dir
    -h  prints this help
'''

import pickle
import sys
import os
import getopt
import nltk_client
import time


class Verba_Pickle:
    def __init__ (self, conf, db):
        self.conf = conf
        self.test = conf['test']
        self.db = db
        fnames = os.listdir (conf['in_dir'])
        self.docs = self.__read_files (fnames)
        first_tid = self.db.get_first_tid () [0]
        first_eid = self.db.get_first_eid () [0]
        self.ext = nltk_client.Extractor (conf, first_tid, first_eid, db)


    def __read_files (self, fnames):
        res = list ()
        for fn in fnames:
            if self.test:
                start = time.time ()
            id = fn[:fn.find('.pickle')]
            fi = open(self.conf['in_dir'] + '/' + fn)
            ob = pickle.load (fi)
            fi.close ()
            res.append ((id, ob))
            if self.test:
                stop = time.time ()
                print 'importing %f' % (stop - start)
        return res


    def analyze_docs (self):
        tot = len (self.docs)
        cnt = 1
        err = False
        wdb_st = 0
        for i, d in self.docs:
            try:
                graph = self.ext.get_relationship (d, i, self.test)
            except AttributeError:
                err = True
            if graph and not err:
                graph.output_graph (self.conf['graph_dir'], i)
            #if not err:
            #    os.remove (self.conf['in_dir'] + '/' + i + '.pickle')
            if not self.test:
                print "Processed document %d out of %d" % (cnt, tot)
            cnt += 1
            err = False
        if self.test:
            wdb_st = time.time ()
        self.db.commit_con ()
        if self.test:
            wdb_end = time.time ()
            print 'write_db %f' % (wdb_end - wdb_st)


def read_opts (argv):
    res = dict()
    res['out_dir'] = 'test_out'
    res['in_dir'] = 'test_in'
    res['graph_dir'] = 'test_graph'
    res['db_file'] = 'entities.db'
    res['storetxt'] = False
    try:
        opts, args = getopt.gnu_getopt(argv, 'i:o:g:d:sh')
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    for o, v in opts:
        if o == '-h':
            print __doc__
            sys.exit(0)
        elif o == '-i':
            res['in_dir'] = v
        elif o == '-o':
            res['out_dir'] = v
        elif o == '-g':
            res['graph_dir'] = v
        elif o == '-d':
            res['db_file'] = v
        elif o == '-s':
            res['storetxt'] = True
    return res



def main ():
    conf = read_opts(sys.argv)
    verba = Verba_Pickle (conf)
    verba.analyze_docs ()


if __name__ == '__main__':
    main ()
