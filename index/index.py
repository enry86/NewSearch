#!/usr/bin/python
'''
Indexer for documents processed by OpenCalais

Usage:
   index.py <INPUT_DIR> [OPTIONS]

Options:
    -h  prints this help
'''

import sys
import getopt
import os
import process
from xml.dom import minidom
        

def read_opts (argv):
    res = {}
    try:
        opts, args = getopt.gnu_getopt(argv,'h')
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(1)
    for o, v in opts:
        if o == '-h':
            print __doc__
            sys.exit(0)
    try:
        res['dir'] = argv[1]
    except IndexError:
        print 'ERR: No input directory'
        print __doc__
        sys.exit(2)
    return res


def parse_files (xml_dir, lst):
    for f in self.lst:
        xml = minidom.parse(xml_dir + '/' + f)
        doc = xml.getElementsByTagName('c:document')
        terms = process.preprocess(doc[0])
        

def read_dir (d):
    lst = os.listdir(d)
    for l in lst:
        if l[l.find('.'):] != '.xml':
            lst.remove(l)
    return lst


def main ():
    conf = read_opts(sys.argv)
    lst = read_dir(conf['dir'])
    parse_files(conf['dir'], lst)


if __name__ == '__main__':
    main()
