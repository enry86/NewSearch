#!/usr/bin/python

'''
Verba

usage:
./verba.py [OPTIONS]

Options:
    -i  input dir
    -o  output dir
    -d  verbs database
    -h  prints this help
'''


import sys
import os
import getopt
from xml.dom import minidom
import nltk_client


def read_opts (argv):
    res = {}
    res['db'] = 'verbs.db'
    res['out_dir'] = 'metadata'
    res['in_dir'] = 'xml_files'
    try:
        opts, args = getopt.gnu_getopt(argv, 'i:o:d:h')
    except getopt.GetoptError, err:
        print str(err)
        sys.exit(2)
    for o, v in opts:
        if o == '-h':
            print __doc__
            sys.exit(0)
        elif o == '-i':
            res['in_dir'] = v
        elif o == '-o':
            res['out_dir'] = v
        elif o == '-d':
            res['db'] = v
    return res


def main ():
    conf = read_opts(sys.argv)
    docs = read_files(conf['in_dir'], conf['out_dir'], conf['db'])


def read_files (xml_dir, out_dir, db):
    verbs_finder = nltk_client.Extractor()
    files = os.listdir(xml_dir)
    res = {}
    for f in files:
        d_id = f[:-4]
        cont = minidom.parse (xml_dir + '/'  + f)
        doc = cont.getElementsByTagName ('c:document')
        text = get_text (doc)
        desc = cont.getElementsByTagName ('rdf:Description')
        ents, pos = get_entities (desc)
        gph = verbs_finder.get_relationship (text, pos)
        add_nodes (gph, ents, pos)
        gph.output_graph ('prova')
        res[d_id] = (ents, gph)
    return res



def add_nodes (gph, ents, pos):
    for i in range (len (pos)):
        id = pos[i][1]
        try:
            keys = ents[id][0][0]
            gph.add_node ((id, i, keys))
        except KeyError:
            pass



def get_entities (ent_lst):
    doc = dict ()
    pos = list ()
    for e in ent_lst:
        id_ent = get_entity_id (e)
        if id_ent:
            data = retrieve_data (e)
            update_doc (doc, data, id_ent)
    prune_ents (doc)
    pos = generate_pos (doc)
    pos.sort ()
    return doc, pos

def generate_pos (ents):
    res = list ()
    for e in ents:
        for p in ents[e][2]:
            res.append ((p, e))
    return res


def prune_ents (ents):
    to_rm = list ()
    for e in ents:
        rel = ents[e][1]
        if not rel:
            to_rm.append (e)
    for r in to_rm:
        ents.pop (r)


def retrieve_data (ent):
    res = None
    kws_phr = ent.getElementsByTagName ('c:exact')
    rel_phr = ent.getElementsByTagName ('c:relevance')
    if kws_phr:
        kws = get_keywords (kws_phr)
        loc = get_location (ent)
        rel = None
        res = (kws, loc, rel)
    elif rel_phr:
        kws = []
        rel = get_relevance (rel_phr)
        loc = None
        res = (kws, loc, rel)
    return res


def update_doc (doc, data, id_ent):
    if data:
        kws, loc, rel = data
        if doc.has_key (id_ent):
            if rel > 0 or rel == None:
                if kws:
                    doc[id_ent][0].append (' '.join(kws))
                if loc:
                    doc[id_ent][2].append (loc)
                doc[id_ent][1] = max(rel, doc[id_ent][1])
            else:
                doc.pop(id_ent)
        elif kws:
            doc[id_ent] = [[' '.join(kws)], rel, [loc]]


def update_pos (pos, data, id_ent):
    if data:
        kws, loc, rel = data
        if rel > 0:
            pos.append ((loc, id_ent))



'''
def get_entities (ent_lst):
    doc = dict ()
    doc_f = dict ()
    pos = list ()
    for e in ent_lst:
        id_ent = get_entity_id(e)
        if id_ent != None:
            phrase = e.getElementsByTagName('c:exact')
            if phrase != []:
                kw = get_keywords(phrase)
                loc = get_location(e)
                pos.append((loc, id_ent))
                try:
                    doc[id_ent].append(kw)
                except:
                    doc[id_ent] = [kw]
            relev = e.getElementsByTagName('c:relevance')
            if relev != []:
                rel = get_relevance(relev)
                try:
                    doc_f[id_ent] =[doc[id_ent], rel]
                except:
                    pass
    pos.sort()
    return doc_f, pos
'''

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


def output_doc (d, doc, o_dir):
    f = open(o_dir + '/' + d + '.metadata', 'w')
    ent, rel = doc
    for e in ent:
        f.write(e + ' Relevance: ' + str(ent[e][1]) + '\n')
        for k in ent[e][0]:
            f.write(str(k))
            f.write('\n')
        f.write('\n')
    f.write('\n')
    for r in rel:
        for i in r[0]:
            f.write(str(i))
            f.write('\n')
        f.write(str(r[1]))
        f.write('\n')
    f.close()


if __name__ == '__main__':
    main()
