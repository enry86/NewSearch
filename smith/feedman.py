#! /usr/bin/python

import utils.feedparser as feedparser
import threading

class FeedManager:
    def __init__ (self):
        self.articles = 0
        self.items = {}
        self.items_proc = {}
        self.u_sem = threading.Semaphore(0)
        self.u_mut = threading.Semaphore(1)

    def add_feed(self, xml):
        feeds = feedparser.parse(xml)
        self.articles += len(feeds['items'])
        for f in feeds['items']:
            self.u_mut.acquire ()
            self.items[f['link']] = (f['title'], f['summary'])
            self.u_mut.release()
            self.u_sem.release()

            
