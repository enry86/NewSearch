#! /usr/bin/python

'''
Smith - Simple news feed crawler

Usage:
    ./smith.py <feed_urls_file> [OPTIONS]

Options:
    -p  proxy configuration (host:port)
    -s  maximum number of sockets used (default 100)
    -h  prints this help
'''

import threading
import asocket
import sys
import getopt


def get_proxy (conf, opt):
    res = True
    opt.replace('http://','')
    if opt.count(':') != 1:
        res = False
    else:
        conf['phost'], port = opt.split(':')
        try:
            conf['pport'] = int(port)
        except Exception:
            res = False
    return res


def read_options ():
    res = {}
    res['phost'] = None
    res['pport'] = None
    res['max_sock'] = 100

    try:
        opts, args = getopt.gnu_getopt(sys.argv, 's:p:h')
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    for o, v in opts:
        if o == '-h':
            print __doc__
            sys.exit(0)
        elif o == '-p':
            if not get_proxy(res, v):
                print 'ERR: Wrong proxy configuration'
                print __doc__
                sys.exit(1)
        elif o == '-s':
            try:
                res['max_sock'] = int(v)
            except ValueError:
                print 'WARN: Invalid number of sockets, using default'
    
    try:
        res['feeds'] = args[1]
    except IndexError:
        print 'ERR: No feeds url file provided'
        print __doc__
        sys.exit(1)
    return res


def get_feeds (filename):
    res = []
    try:
        f = open(filename)
    except Exception:
        return res
    for l in f:
        l = l.replace('http://', '')
        i = l.find('/')
        if i != -1:
            res.append((l[:i], l[i:]))
        else:
            print 'WARN: invalid feed - %s' % l
    f.close()
    return res
        

def setup_pool (conf, feeds, sock, free):
    pass

def read_sock (ready, r_sem):
    r_sem.acquire()
    s = ready.pop()
    print s.data

def main ():
    sock = []
    free = []
    ready = []
    conf = read_options()
    feeds = get_feeds(conf['feeds'])
    ready_sem = threading.Semaphore(0)
    
    asocket.start_loop()    



if __name__ == '__main__':
    main()


