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
    
    def __init__(self, conf, pool, f_man):
        self.pg_saved = 0
        self.conf = conf
        self.pool = pool
        self.f_man = f_man
        self.quit = False
        self.init_dirs()

    
    def init_dirs(self):
        try:
            os.mkdir(self.conf['pag_dir'])
        except Exception:
            pass

    def quit_com(self):
        self.quit = True

    
    def status(self):
        print 'Articles retrieved:', self.f_man.articles
        print 'Pages saved:', self.pg_saved
        print 'Working sockets:', self.pool.working

    def console(self):
        s = ''
        while not self.quit:
            s = raw_input('> ')
            if s == 'q':
                self.quit_com()
            elif s == 's':
                self.status()
            
    
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
        if i != -1 and l[0] != '#':
            res.append((l[:i], l[i:]))
        elif l[0] != '#':
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
        v = f_man.items.pop(u)
        f_man.items_proc[u] = v
        tar = get_host_path(u)
        if tar != None:
            pool.start_socket(tar, 1)


def read_sock (pool, f_man, m):
    while not m.quit:
        data, t =  pool.read_socket()
        if t == 0:
            f_man.add_feed(data[0])
        elif t == 1:
            store_page(data, f_man, m)


def build_header (str_h):
    head = {}
    fields = str_h.split('\n')
    head['status'] = fields[0].strip()
    fields.remove(fields[0])
    for f in fields:
        try:
            k, v = f.split(': ')
            head[k.strip()] = v.strip()
        except ValueError:
            pass
    return head


def get_content (data):
    str_h = data[:data.find('<')]
    cont = data[data.find('<'):]
    head = build_header(str_h)
    return head, cont


def store_page (data, f_man, man):
    head, cont = get_content(data[0])
    st_ok = head['status'].find('200') != -1
    st_mv = head['status'].find('301') != -1
    st_fnd = head['status'].find('302') != -1
    if st_ok:
        path = man.conf['pag_dir'] + '/'
        f_name = str(time.time()).replace('.', '')
        f = open(path + f_name + '.html', 'w')
        f.write(cont)
        f.close()
        man.pg_saved += 1
    elif st_mv or st_fnd:
        url = head['Location']
        v = f_man.items_proc[data[1]]
        f_man.items[url] = (v, 'redirected')
        f_man.u_sem.release()
    elif head['status'] == '':
        v = f_man.items_proc[data[1]]
        f_man.items[data[1]] = (v, 'retry')
        f_man.u_sem.release()
    f_man.items_proc.pop(data[1])
        

def start_poll(man, pool):
    while not man.quit:
        time.sleep(10)
        pool.poll()


def main ():
    conf = read_options()
    feeds = get_feeds(conf['feeds'])
    f_man = feedman.FeedManager()
    pool = sock_pool.SockPool(conf)
    man = Manager(conf, pool, f_man)
    man.start_cons()
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
    p_args = (man, pool)
    p_thr = threading.Thread(target = start_poll, args = p_args)
    p_thr.setDaemon(True)
    p_thr.start()


if __name__ == '__main__':
    main()


