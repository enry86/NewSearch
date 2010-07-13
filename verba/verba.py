#!/usr/bin/python

import sys
import os
import getopt
import verbs_finder
from xml.dom import minidom

def read_opts (argv):
    res = {}
    res['db'] = 'verbs.db'
    try:
        res['in_dir'] = argv[1].replace('/', '')
    except:
        res['in_dir'] = 'xml'
    return res


def main ():
    conf = read_opts(sys.argv)
    docs = read_files(conf['in_dir'], conf['db'])
    output_docs(docs)
    

def read_files (xml_dir, db):
    files = os.listdir(xml_dir)
    res = {}
    for f in files:
        d_id = f[:-4]
        cont = minidom.parse(xml_dir + '/'  + f)
        doc = cont.getElementsByTagName('c:document')
        text = get_text(doc)
        desc = cont.getElementsByTagName('rdf:Description')
        ents, pos = get_entities(desc)
        rel = verbs_finder.get_relationship(text, pos, db)
        res[d_id] = (ents, rel)
    return res 


def get_entities (ent_lst):
    doc = {}
    pos = []
    for e in ent_lst:
        id_ent = get_entity_id(e)
        if id_ent != None:
            phrase = e.getElementsByTagName('c:exact')
            if phrase != []:
                kw = get_keywords(phrase)
                loc = get_location(e)
                pos.append((loc, id_ent))
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
    pos.sort()
    return doc, pos


def get_text (doc):
    res = None
    try:
        node = doc[0].firstChild
        res = node.nodeValue
    except:
        pass
    return res



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
    

def get_location (ent):
    res = None
    o_lst = ent.getElementsByTagName('c:offset')
    l_lst = ent.getElementsByTagName('c:length')
    try:
        o_node = o_lst[0].firstChild
        l_node = l_lst[0].firstChild
        res = (int(o_node.nodeValue), int(l_node.nodeValue))
    except:
        pass
    return res


def output_docs (docs):
    for d in docs:
        ent, rel = docs[d]
        for e in ent:
            print e, 'Relevance:', ent[e][1]
            for k in ent[e][0]:
                print k
            print '\n'
        print '\n'
        for r in rel:
            for i in r[0]:
                print i
            print r[1]
            print '\n'



        






if __name__ == '__main__':
    main()
