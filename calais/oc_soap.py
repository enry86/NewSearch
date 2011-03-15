#!/usr/bin/python
'''
OC_Soap - Soap client for OpenCalais WebService

Usage:
    ./oc_soap.py <pages_repo> [OPTIONS]

Options:
    -h  prints this help
    -r  directory of results
    -p  directory of read pages
    -k  OpenCalais key
'''

import utils.calais as calais
import os
import sys
import getopt
import pickle

class CalaisClient:       
    def read_file (self, filename):
        tmp = ''
        f = open(filename, 'r')
        for l in f:
            tmp += l
        f.close()
        res = str(unicode(tmp, errors = 'ignore'))
        return res


    def write_file (self, filename, cont):
        f = open(filename, 'w')
        f.write(cont)
        f.close()


    def move_file (self, s_dir, d_dir, fname):
        c = read_file(s_dir + '/' + fname)
        write_file(d_dir + '/' + fname, c)
        os.remove(s_dir + '/' + fname)


    def call_srv (self, conf, cxml, files, srv):
        try:
            os.mkdir(conf['res'])
            os.mkdir(conf['read'])
        except OSError:
            pass
        for f in files:
            cont = read_file(conf['repo'] + '/' + f)
        res = srv.service.Enlighten(conf['key'], cont, cxml)
        res_str = res.encode('utf8', 'ignore')
        write_file(conf['res'] + '/' + f[:-4] + 'xml', res_str)
        move_file(conf['repo'], conf['read'], f)
        

def main ():
    conf = read_opts(sys.argv)
    try:
        files = os.listdir(conf['repo'])
    except OSError:
        print 'ERR: Invalid path repo'
        sys.exit(3)
    cli = CalaisClient (conf)
    cli.call_srv ()

def read_opts (argv):
    res = {}
    res['read'] = 'pages_read'
    res['res'] = 'results'
    res['key'] = '33q562d5y52rqsxvfwm9s27e'
    try:
        opts, args = getopt.gnu_getopt(argv, 'w:r:p:h')
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    for o, v in opts:
        if o == '-h':
            print __doc__
            sys.exit(0)
        elif o == '-r':
            res['res'] = v
        elif o == '-p':
            res['read'] = v
        elif o == '-k':
            res['key'] = v
    try:
        res['repo'] = argv[1]
    except IndexError:
        print 'ERR: Argument error'
        print __doc__
        sys.exit(1)
    return res
 

if __name__ == '__main__':
    main()

