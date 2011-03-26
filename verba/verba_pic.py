#!/usr/bin/python

'''
Verba

usage:
./verba.py [OPTIONS]

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
from xml.dom import minidom
import nltk_client


class Verba_Pickle:
    def __init__ (self, conf):
        self.conf = conf
        fnames = os.listdir (conf['in_dir'])
        self.docs = self.__read_files (fnames)

    def __read_files (fnames):
        res = list ()
        for fn in fnames:
            id = fn[:fn.find('.pickle')]
            fi = open(fn)
            ob = pickle.load (fi)
            fi.close ()
            res.append (id, ob)
        return res



def read_opts (argv):
    res = dict()
    res['out_dir'] = 'metadata'
    res['in_dir'] = 'xml_files'
    res['graph_dir'] = 'graphs'
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
