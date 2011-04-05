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
        self.ext = nltk_client.Extractor ()

    def __read_files (self, fnames):
        res = list ()
        for fn in fnames:
            id = fn[:fn.find('.pickle')]
            fi = open(self.conf['in_dir'] + '/' + fn)
            ob = pickle.load (fi)
            fi.close ()
            res.append ((id, ob))
        return res

    def analyze_docs (self):
        for i, d in self.docs:
            graph = self.ext.get_relationship (d)
            graph.output_graph (i)


def read_opts (argv):
    res = dict()
    res['out_dir'] = 'test_out'
    res['in_dir'] = 'test_in'
    res['graph_dir'] = 'test_graph'
    try:
        opts, args = getopt.gnu_getopt(argv, 'i:o:c:h')
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
        elif o == '-c':
            res['graph_dir'] = v
    return res



def main ():
    conf = read_opts(sys.argv)
    verba = Verba_Pickle (conf)
    verba.analyze_docs ()


if __name__ == '__main__':
    main ()
