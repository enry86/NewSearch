#! /usr/bin/python

'''
Smith - Simple news feed crawler

Usage:
    ./smith.py <feed_urls_file> [OPTIONS]

Options:
    -p  proxy configuration (host:port)
    -s  maximum number of sockets used (default 100)
    -d  pages directory
    -h  prints this help
'''

import threading
import os
import time
import sys
import getopt

import sock_pool
import feedman


class Manager:
    def __init__(self, conf):
        self.conf = conf
        self.quit = False
        self.init_dirs()

    
    def init_dirs(self):
        try:
            os.mkdir(self.conf['pag_dir'])
        except Exception:
            pass

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
    res['pag_dir'] = 'pages'

    try:
        opts, args = getopt.gnu_getopt(sys.argv, 's:p:d:h')
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
        elif o == '-d':
            res['pag_dir'] = v

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
        res = (url[:i], url[i:])
    else:
        res = None
    return res


def read_feeds (feeds, pool):
    for f in feeds:
        pool.start_socket(f, 0)


def read_urls(f_man, pool, m):
    while not m.quit:
        f_man.u_sem.acquire()
        urls = f_man.items.keys()
        u = urls.pop()
        f_man.items.pop(u)
        tar = get_host_path(u)
        if tar != None:
            pool.start_socket(tar, 1)


def read_sock (pool, f_man, m):
    while not m.quit:
        data, t =  pool.read_socket()
        if t == 0:
            f_man.add_feed(data)
        elif t == 1:
            store_page(data, m)


def store_page(data, man):
    path = man.conf['pag_dir'] + '/'
    f_name = str(time.time()).replace('.', '')
    f = open(path + f_name + '.html', 'w')
    f.write(data)
    f.close()


def main ():
    conf = read_options()
    feeds = get_feeds(conf['feeds'])
    man = Manager(conf)
    man.start_cons()
    f_man = feedman.FeedManager()
    pool = sock_pool.SockPool(conf)
    s_thr = threading.Thread(target = read_feeds, args = (feeds, pool,))
    s_thr.setDaemon(True)
    s_thr.start()
    r_args = (pool, f_man, man)
    r_thr = threading.Thread(target = read_sock, args = r_args)
    r_thr.setDaemon(True)
    r_thr.start()
    u_args = (f_man, pool, man)
    u_thr = threading.Thread(target = read_urls, args = u_args)
    u_thr.setDaemon(True)
    u_thr.start()

if __name__ == '__main__':
    main()


