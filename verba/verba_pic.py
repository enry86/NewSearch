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



class Verba_Pickle:
    def __init__ (self, conf):
        self.conf = conf
        fnames = os.listdir (conf['in_dir'])
        self.docs = self.__read_files (fnames)
        self.ext = nltk_client.Extractor (conf)

    def __read_files (self, fnames):
        res = list ()
        for fn in fnames:
            id = fn[:fn.find('.pickle')]
            fi = open(self.conf['in_dir'] + '/' + fn)
            ob = pickle.load (fi)
            fi.close ()
            res.append ((id, ob))
        return res

    def __dump_graph (self, gr, fn):
        fo = open (self.conf['out_dir'] + '/' + fn + '.pickle', 'w')
        pickle.dump (gr, fo)
        fo.close ()

    def analyze_docs (self):
        tot = len (self.docs)
        cnt = 1
        for i, d in self.docs:
            graph = self.ext.get_relationship (d, i)
            if graph:
                self.__dump_graph (graph, i)
                graph.output_graph (self.conf['graph_dir'], i)
            print "Processed document %d out of %d" % (cnt, tot)
            cnt += 1


def read_opts (argv):
    res = dict()
    res['out_dir'] = 'test_out'
    res['in_dir'] = 'test_in'
    res['graph_dir'] = 'test_graph'
    res['db_file'] = 'entities.db'
    try:
        opts, args = getopt.gnu_getopt(argv, 'i:o:g:d:h')
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
    return res



def main ():
    conf = read_opts(sys.argv)
    verba = Verba_Pickle (conf)
    verba.analyze_docs ()


if __name__ == '__main__':
    main ()
