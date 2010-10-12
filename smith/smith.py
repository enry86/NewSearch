#! /usr/bin/python

'''
Smith - Simple news feed crawler

Usage:
    ./smith.py <feed_urls_file> [OPTIONS]

Options:
    -p  proxy configuration (host:port)
    -s  maximum number of sockets used (default 100)
    -d  pages directory
    -o  database file 
    -a  forces asyncronous mode (buggy)
    -h  prints this help
'''

import threading
import os
import time
import sys
import getopt

import async_sock_pool
import threading_sock_pool
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



class Smith:
    conf = {}

    def __init__ (self, conf):
        self.conf = conf
        self.feeds = self.get_feeds(conf['feeds'])
        self.f_man = feedman.FeedManager()
        if self.conf['async']:
            self.pool = async_sock_pool.SockPool (conf)
        else:
            self.pool = threading_sock_pool.SockPool (conf)
        self.man = Manager(self.conf, self.pool, self.f_man)
        self.man.start_cons()

    def start (self):
        self.feeds_thr = self.__start_component (self.read_feeds)
        self.pool_thr = self.__start_component (self.read_sock)
        self.urls_thr = self.__start_component (self.read_urls)
        if self.conf['async']:
           self.poll_thr = self.__start_component(self.start_poll)


    def __start_component(self, fun):
        thr = threading.Thread(target = fun)
        thr.setDaemon(True)
        thr.start()
        return thr


    def get_feeds (self, filename):
        res = []
        try:
            f = open(filename)
        except Exception:
            return res
        for l in f:
            if l[0] != '#':
                if self.conf['async']:
                    tmp = self.get_host_path (l)
                else:
                    tmp = l
                res.append (tmp)
        f.close()
        return res


    def get_host_path (self, url):    
        url = url.replace('http://', '')
        i = url.find('/')
        if i != -1:
            res = (url[:i], url[i:])
        else:
            res = None
        return res


    def read_feeds (self):
        for f in self.feeds:
            self.pool.start_socket(f, 0)


    def read_urls(self):
        while not self.man.quit:
            self.f_man.u_sem.acquire()
            urls = self.f_man.items.keys()
            u = urls.pop()
            v = self.f_man.items.pop(u)
            self.f_man.items_proc[u] = v
            if self.conf['async']:
                tar = self.get_host_path(u)
            else:
                tar = u
            if tar != None:
                self.pool.start_socket(tar, 1)


    def read_sock (self):
        while not self.man.quit:
            data, t =  self.pool.read_socket()
            if t == 0:
                self.f_man.add_feed(data[0])
            elif t == 1:
                self.store_page(data)


    def build_header (self, str_h):
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


    def get_content (self, data):
        str_h = data[:data.find('<')]
        cont = data[data.find('<'):]
        head = self.build_header(str_h)
        return head, cont

    def store_page (self, data):
        if self.conf['async']:
            self.store_page_async (data)
        else:
            self.write_page (data[0])

    def write_page (self, data):
        path = self.conf['pag_dir'] + '/'
        f_name = str(time.time()).replace('.', '')
        f = open(path + f_name + '.html', 'w')
        f.write(data)
        f.close()
        self.man.pg_saved += 1


    def store_page_async (self, data):
        head, cont = self.get_content(data[0])
        st_ok = head['status'].find('200') != -1
        st_red = self.__is_redir (head)
        if st_ok:
            write_page (data)
        elif st_red:
            url = head['Location']
            v = self.f_man.items_proc[data[1]]
            self.f_man.items[url] = (v, 'redirected')
            self.f_man.u_sem.release()
        elif head['status'] == '':
            v = self.f_man.items_proc[data[1]]
            self.f_man.items[data[1]] = (v, 'retry')
            self.f_man.u_sem.release()
        self.f_man.items_proc.pop(data[1])
    
    def __is_redir (self, header):
        errors = [301, 302, 303, 304, 305, 306, 307]
        res = false
        for e in errors:
            res = res or head['status'].find(e) != -1
        return res

    def start_poll (self):
        while not self.man.quit:
            time.sleep(10)
            self.pool.poll()

def read_options ():
    res = {}
    res['phost'] = None
    res['pport'] = None
    res['max_sock'] = 100
    res['pag_dir'] = 'pages'
    res['database'] = '../newsearch.sqlite'
    res['async'] = False;

    try:
        opts, args = getopt.gnu_getopt(sys.argv, 's:p:d:o:ah')
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
        elif o == '-o':
            res['database'] = v
        elif o == '-a':
            res['async'] = True;

    try:
        res['feeds'] = args[1]
    except IndexError:
        print 'ERR: No feeds url file provided'
        print __doc__
        sys.exit(1)
    return res


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


def main ():
    conf = read_options()
    smith = Smith(conf)
    smith.start()

if __name__ == '__main__':
    main()


