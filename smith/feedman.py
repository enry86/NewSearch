#! /usr/bin/python

import utils.feedparser as feedparser
import threading

class FeedManager:
    def __init__ (self):
        self.items = {}
        self.items_proc = {}
        self.u_sem = threading.Semaphore(0)

    def add_feed(self, xml):
        feeds = feedparser.parse(xml)
        for f in feeds['items']:
            self.items[f['link']] = (f['title'], f['summary'])
            self.u_sem.release()

            
