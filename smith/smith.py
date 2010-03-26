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
import sys
import getopt

import sock_pool
import feedman


class Manager:
    def __init__(self):
        self.quit = False


    def quit_com(self):
        self.quit = True


    def console(self):
        s = ''
        while not self.quit:
            s = raw_input('> ')
            if s == 'q':
                self.quit_com()
            
    
    def start_cons(self):
        thr = threading.Thread(target = self.console)
        thr.start()



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
        
def get_host_path (url):    
    url = url.replace('http://', '')
    i = url.find('/')
    if i != -1:
        return (l[:i], l[i:])
    else:
        return None
        



def read_feeds (feeds, pool):
    for f in feeds:
        pool.start_socket(f)
        print 'socket started'
    pool.start_loop()


def read_urls(f_man, pool):
    for u in f_man.items:
        pool.start_socket(get_host_path(u))


def read_sock (pool, f_man, m):
    while not m.quit:
        rss =  pool.read_socket()
        f_man.add_feed(rss)


def main ():
    conf = read_options()
    feeds = get_feeds(conf['feeds'])
    man = Manager()
    man.start_cons()
    f_man = feedman.FeedManager()
    pool = sock_pool.SockPool(conf)
    thr = threading.Thread(target = read_feeds, args = (feeds, pool,))
    thr.start()
    read_sock(pool, f_man, man)


if __name__ == '__main__':
    main()


