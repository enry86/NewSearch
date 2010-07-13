#!/usr/bin/python

import sqlite3

def get_relationship (text, pos, db):
    sent = select_sent(text, pos)
    rels = constr_rel(sent, db)
    return rels


def select_sent (text, pos):
    base = 0
    ent = 0
    res = []
    while base < len(text):
        ent_l = []
        sent, n_base = isolate_sent(text[base:], base)
        while ent < len(pos) and pos[ent][0][0] < n_base:
            ent_l.append(pos[ent])
            ent += 1
        if ent_l != []:
            node = (sent, (base, n_base), ent_l)
            res.append(node)
        base = n_base + 1
    return res


def isolate_sent (text, base):
    dot = text.find('.')
    res = None
    while dot < 100 and res == None:
        if dot == -1:
            res = text
        else:
            dot = text.find('.', dot + 1)
    if res == None:
        res = text[:dot + 1]
    return res, base + len(res)


def constr_rel (sent, db):
    res = []
    for sen, pos, ent_l in sent:
        base, end = pos
        for e in ent_l:
            off, lng = e[0]
            off -= base
            sen = sen.replace(sen[off : off + lng], '')
            base += lng
        verbs = retr_verbs(sen, db)
        res.append((ent_l, verbs))
    return res


def retr_verbs (s, db):
    res = []
    s = s.replace('.',' ')
    s = s.replace(',',' ')
    s = s.replace(';',' ')
    s = s.replace(':',' ')
    kw = s.split()
    
    con = sqlite3.connect(db)
    for k in kw:
        if is_verb(k, con):
            res.append(k)
        else:
            k = stem(k)
            if is_verb(k, con):
                res.append(k)
    con.close()
    return res
            
def stem (word):
    res = None
    if word.endswith('ing'):
        res = word[:-3]
    elif word.endswith('ed'):
        res = word[:-2]
    elif word.endswith('s'):
        res = word[:-1]
    return res
        

def is_verb (word, con):
    sql = 'select count(*) from verbs where verb like "%s"'
    res = con.execute(sql % word)
    cnt, = res.fetchone()
    return cnt
