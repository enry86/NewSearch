#! /usr/bin/python

'''
ASocket - Asynchronous socket implementation
'''

import asyncore
import socket

class AsynSocket (asyncore.dispatcher):
    def __init__(self, phost, pport, ready, r_sem):
        asyncore.dispatcher.__init__(self)
        self.data = ''
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.phost = phost
        self.pport = pport
        self.ready = ready
        self.r_sem = r_sem
        

    def start_connection (self, host, path):
        if self.phost:
            target = (phost, pport)
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


def start_loop ():
    asyncore.loop()
