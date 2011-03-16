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
    -t  type of content [html, raw, xml]
'''

import utils.calais as calais
import os
import sys
import getopt
import pickle

class CalaisClient:       
    def __init__ (self, conf):
        self.conf = conf
        try:
            self.files = os.listdir(conf['repo'])
        except OSError:
            print 'ERR: Invalid path repo'
            sys.exit(3)
        self.calais = calais.Calais(conf['key'], submitter='NewSearch')
        self.calais.processing_directives['omitOutputtingOriginalText'] = 'false'
        self.calais.processing_directives['contentType'] = conf['type']
        


    def read_file (self, filename):
        tmp = ''
        f = open(filename, 'r')
        for l in f:
            tmp += l
        f.close()
        res = str(unicode(tmp, errors = 'ignore'))
        return res


    def write_file (self, filename, res):
        f = open(filename, 'w')
        pickle.dump(res, f)
        f.close()


    def move_file (self, s_dir, d_dir, fname):
        os.rename(s_dir + '/' + fname, d_dir + '/' + fname)


    def call_srv (self):
        try:
            os.mkdir(self.conf['res'])
            os.mkdir(self.conf['read'])
        except OSError:
            pass
        for f in self.files:
            cont = self.read_file (self.conf['repo'] + '/' + f)
            res = self.calais.analyze (cont, content_type = \
                self.conf['type'], external_id = f)
            self.write_file(self.conf['res'] + '/' + f[:-4] + 'pickle', res)
            self.move_file(self.conf['repo'], self.conf['read'], f)
        

def main ():
    conf = read_opts(sys.argv)
    cli = CalaisClient (conf)
    cli.call_srv ()

def read_opts (argv):
    res = {}
    res['read'] = 'pages_read'
    res['res'] = 'results'
    res['key'] = '33q562d5y52rqsxvfwm9s27e'
    res['type'] = 'text/html'
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
        elif o == '-t':
            res['type'] = 'text/' + v
    try:
        res['repo'] = argv[1]
    except IndexError:
        print 'ERR: Argument error'
        print __doc__
        sys.exit(1)
    return res
 

if __name__ == '__main__':
    main()

