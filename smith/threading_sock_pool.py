#!/usr/bin/python

import urllib2
import feedman
import threading


class ThreadSocket:
    def __init__ (self, pohst, pport, callback):
        self.phost = phost 
        self.pport = pport
        self.maxredir = 50
        self.callback = callback

    def get_url (self, url, type):
        opener = __setup_opener ()
        urllib2.install_opener (opener)
        res = urrlib2.urlopen (url)
        if res.getcode () >= 400:
            callback.on_failure (url, res.getcode ())
        else:
            data = res.read ()
            callback.on_success (url, type, data)

    def __setup_opener (self):
        handler = urllib2.HTTPRedirectHandler ()
        handler.max_redirections = self.maxredir
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
    
    def read_socket (self):
        self.res_sem.acquire ()
        self.lst_sem.acquire ()
        res = res_lst.pop()
        self.lst_sem.release ()
        self.res_sem.release ()
        return res

    def start_socket (self, target, type):
        sock = ThreadSocket (self.phost, self.pport, self)
        arg_t = (target, type)
        self.thr_sem.acquire ()
        thr = threading.Thread (target = sock.get_url, args = arg_t)
        thr.start()


    def on_failure (self, url, code):
        print 'WARN: Http Error %d on %s' % (code, url)
        self.thr_sem.release ()
    
    def on_success (self, url, type, data):
        self.lst_sem.acqiure ()
        self.res_lst.append = ((data, url), type)
        self.lst_sem.release ()
        self.thr_sem.release ()
    

    def poll ():
        pass
        
