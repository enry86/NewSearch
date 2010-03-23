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
        

def start_pool (conf, feeds, sock, ready, free, s_sem, r_sem, f_sem):
    for f in feeds:
        if f_sem.acquire(False):
            s = free.pop()
            s.start_connection(f)
        elif s_sem.acquire(False):
            tmp = asocket.AsynSocket(conf['phost'], conf['pport'], ready,\
                r_sem)
            tmp.start_connection(f)
            sock.append(tmp)
        else:
            f_sem.acquire()
            s = free.pop()
            s.start_connection(f)
    asocket.start_loop()    
    

def read_sock (free, ready, r_sem, f_sem):
    r_sem.acquire()
    s = ready.pop()
    print s.data
    s.data = ''
    free.append(s)
    f_sem.release()


def main ():
    sock = []
    free = []
    ready = []
    conf = read_options()
    feeds = get_feeds(conf['feeds'])
    ready_sem = threading.Semaphore(0)
    free_sem = threading.Semaphore(0)
    slot_sem = threading.Semaphore(conf['max_sock'])
    pool_args = (conf, feeds, sock, ready, free, slot_sem, ready_sem,\
        free_sem,)
    thr = threading.Thread(target = start_pool, args = pool_args)
    thr.start()
    read_sock(free, ready, ready_sem, free_sem)


if __name__ == '__main__':
    main()


