#!/usr/bin/python

import urllib2
import feedman
import threading


class ThreadSocket:
    def __init__ (self, phost, pport, callback):
        self.phost = phost 
        self.pport = pport
        if self.phost != None:
            self.proxy = self.phost + ':' + self.pport
            print self.proxy
        else:
            self.proxy = None
        self.maxredir = 50
        self.callback = callback

    def get_url (self, url, type):
        code = 200
        opener = self.__setup_opener ()
        urllib2.install_opener (opener)
        try:
            res = urllib2.urlopen (url)
            #code = res.gedcode ()
            #print 'CODE:', code
        except:
            print 'Error on URL:', url
            code = 404
        if code >= 400:
            self.callback.on_failure (url, code)
        else:
            data = res.read ()
            self.callback.on_success (url, type, data)

    def __setup_opener (self):
        handler = urllib2.HTTPRedirectHandler ()
        handler.max_redirections = self.maxredir
        if self.proxy != None:
            proxy_h = urllib2.ProxyHandler ({'http' : self.proxy})
            opener = urllib2.build_opener (handler, proxy_h)
        else:
            opener = urllib2.build_opener (handler)
        return opener
        

class SockPool:
    def __init__ (self, conf):
        self.phost = conf['phost']
        self.pport = conf['pport']
        self.thr_sem = threading.Semaphore (conf['max_sock'])
        self.lst_sem = threading.Semaphore (1)
        self.res_sem = threading.Semaphore (0)
        self.res_lst = []
        self.working = 0
    
    def read_socket (self):
        self.res_sem.acquire ()
        self.lst_sem.acquire ()
        res = self.res_lst.pop()
        self.lst_sem.release ()
        return res

    def start_socket (self, target, type):
        sock = ThreadSocket (self.phost, self.pport, self)
        arg_t = (target, type)
        self.thr_sem.acquire ()
        thr = threading.Thread (target = sock.get_url, args = arg_t)
        thr.start()
        self.working += 1


    def on_failure (self, url, code):
        print 'WARN: Http Error %d on %s' % (code, url)
        self.thr_sem.release ()
        self.working -= 1
    
    def on_success (self, url, type, data):
        self.lst_sem.acquire ()
        self.res_lst.append (((data, url), type))
        self.working -= 1
        self.lst_sem.release ()
        self.thr_sem.release ()
        self.res_sem.release ()
    

    def poll ():
        pass
        
