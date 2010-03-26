#! /usr/bin/python

'''
ASocket - Asynchronous socket implementation
'''

import asyncore
import socket
import threading

class AsynSocket (asyncore.dispatcher):
    def __init__(self, phost, pport, ready, r_sem, req_type):
        asyncore.dispatcher.__init__(self)
        self.data = ''
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.phost = phost
        self.pport = pport
        self.ready = ready
        self.r_sem = r_sem
        self.req_type = req_type
        

    def start_connection (self, (host, path)):
        if self.phost:
            target = (self.phost, self.pport)
        else:
            target = (host, 80)
        url = 'http://%s%s' % (host, path)
        self.connect(target)
        self.buffer = 'GET %s HTTP/1.0\r\n\r\n' % url


    def handle_connect (self):
        pass
    

    def handle_close (self):
        self.close()
        self.ready.append(self)
        self.r_sem.release()


    def handle_read (self):
        self.data += self.recv(1024)


    def writable (self):
        return (len(self.buffer) > 0)


    def handle_write (self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]



class SockPool:
    def __init__ (self, conf):
        self.phost = conf['phost']
        self.pport = conf['pport']
        self.sock = []
        self.free = []
        self.ready = []
        self.r_sem = threading.Semaphore(0)
        self.f_sem = threading.Semaphore(0)
        self.s_sem = threading.Semaphore(conf['max_sock'])


    def start_socket(self, target, req_type):
        if self.f_sem.acquire(False):
            s = self.free.pop()
            s.start_connection(target)
        elif self.s_sem.acquire(False):
            tmp = AsynSocket(self.phost, self.pport, self.ready,\
                self.r_sem, req_type)
            tmp.start_connection(target)
            self.sock.append(tmp)
        else:
            self.f_sem.acquire()
            s = free.pop()
            s.start_connection(f)
    

    def read_socket(self):
        self.r_sem.acquire()
        s = self.ready.pop()
        res = s.data
        s.data = ''
        self.free.append(s)
        self.f_sem.release()
        return (res, s.req_type)


    def start_loop (self):
        asyncore.loop()

