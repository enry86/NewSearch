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
import time

class CalaisClient:
    def __init__ (self, conf, files):
        self.conf = conf
        self.files = files
        self.test = conf['test']
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


    def __get_filename (self, f):
        res = f.split ('/') [-1]
        return res

    def call_srv (self):
        try:
            os.mkdir(self.conf['res'])
            os.mkdir(self.conf['read'])
        except OSError:
            pass
        for i,f in enumerate(self.files):
            fname = self.__get_filename (f)
            if not os.path.isfile ('%s/%spickle' % (self.conf['res'], fname[:-4])):
                try:
                    if self.test:
                        start = time.time ()
                    cont = self.read_file (f)
                    if self.test:
                        end_read = time.time ()
                    res = self.calais.analyze (cont, content_type = \
                                                   self.conf['type'], external_id = f)
                    if self.test:
                        end_calais = time.time ()
                    self.write_file(self.conf['res'] + '/' + fname[:-4] + 'pickle', res)
                    if self.test:
                        end_store = time.time ()
                        print 'read %f' % (end_read - start)
                        print 'query %f' % (end_calais - end_read)
                        print 'pickle %f' % (end_store - end_calais)
                    else:
                        print 'saved file %d out of %d' % (i, len(self.files))
                except ValueError:
                    if not self.test:
                        print 'Error on file %s' % f
            elif not self.test:
                print 'File already processed'


def main ():
    conf = read_opts(sys.argv)
    files = sys.argv[1:]
    cli = CalaisClient (conf, files)
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
