#!/usr/bin/python
'''
OC_Soap - Soap client for OpenCalais WebService

Usage:
    ./oc_soap.py <pages_repo> <configuration_file> [OPTIONS]

Options:
    -w  wsdl url
    -r  directory of results
    -p  directory of read pages
    -k  OpenCalais key
'''

from suds.client import Client
import os
import sys
import getopt

def read_opts (argv):
    res = {}
    res['wsdl_u'] = 'http://api.opencalais.com/enlighten/?wsdl'
    res['read'] = 'pages_read'
    res['res'] = 'results'
    res['key'] = '33q562d5y52rqsxvfwm9s27e'
    try:
        opts, args = getopt.gnu_getopt(argv, 'w:r:p:k:')
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    for o, v in opts:
        if o == '-w':
            res['wsdl_u'] = v
        elif o == '-r':
            res['res'] = v
        elif o == '-p':
            res['read'] = v
        elif o == '-k':
            res['key'] = v
    try:
        res['repo'] = argv[1]
        res['cxml'] = argv[2]
    except IndexError:
        print 'ERR: Argument error'
        print __doc__
        sys.exit(1)
    return res
        
def read_file (filename):
    res = ''
    f = open(filename, 'r')
    for l in f:
        res += l
    f.close()
    return res


def write_file (filename, cont):
    f = open(filename, 'w')
    f.write(cont)
    f.close()

def move_file (s_dir, d_dir, fname):
    c = read_file(s_dir + '/' + fname)
    write_file(d_dir + '/' + fname, c)
    os.remove(s_dir + '/' + fname)

def call_srv (conf, cxml, files, srv):
    try:
        os.mkdir(conf['res'])
        os.mkdir(conf['read'])
    except OSError:
        pass
    for f in files:
        cont = read_file(conf['repo'] + f)
        res = srv.service.Enlighten(conf['key'], cont, cxml)
        write_file(conf['res'] + '/' + f[:-4] + 'xml', res)
        move_file(conf['repo'], conf['read'], f)
        

def main ():
    conf = read_opts(sys.argv)
    srv = Client(conf['wsdl_u'])#, http_proxy = 'http://proxyopera.unitn.it:3128')
    c_xml = read_file(conf['cxml'])
    try:
        files = os.listdir(conf['repo'])
    except OSError:
        print 'ERR: Invalid path repo'
        sys.exit(3)
    call_srv(conf, c_xml, files, srv) 
    print res


if __name__ == '__main__':
    main()

