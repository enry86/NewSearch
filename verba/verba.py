#!/usr/bin/python

import sys
import os
import getopt

from xml.dom import minidom

def read_opts (argv):
    res = {}
    res['in_dir'] = 'xml'
    return res


def main ():
    conf = read_opts(sys.argv)
    docs = read_files(conf['in_dir'])
    

def read_files (xml_dir):
    files = os.listdir(xml_dir)
    res = {}
    for f in files:
        d_id = f[:-4]
        cont = minidom.parse(xml_dir + '/'  + f)
        desc = cont.getElementsByTagName('rdf:Description')
        ents = get_entities(desc)
        res[d_id] = ents
    return res


def get_entities (ent_lst):
    doc = {}
    for e in ent_lst:
        id_ent = get_entity_id(e)
        if id_ent != None:
            phrase = e.getElementsByTagName('c:exact')
            if phrase != []:
                kw = get_keywords(phrase)
                try:
                    doc[id_ent][0].append(kw)
                except:
                    doc[id_ent] = [[kw], 0.0]
            relev = e.getElementsByTagName('c:relevance')
            if relev != []:
                rel = get_relevance(relev)
                try:
                    doc[id_ent][1] = rel
                except:
                    pass
    return doc

            
def get_entity_id (e):
    res = None
    s = e.getElementsByTagName('c:subject')
    if s != []:
        res = str(s[0].getAttribute('rdf:resource'))
    return res


def get_keywords (exact):
    node = exact[0].firstChild
    value = str(node.nodeValue)
    res = value.split()
    return res


def get_relevance (rel):
    node = rel[0].firstChild
    value = str(node.nodeValue)
    res = float(value)
    return res
    





def parse (xml):
    cont = minidom.parse(xml)


if __name__ == '__main__':
    main()
