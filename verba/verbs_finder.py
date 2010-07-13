#!/usr/bin/python

def get_relationship (text, pos):
    sent = select_sent(text, pos)
  #  rels = constr_rel(sent)


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


def constr_rel (sent):
    for sen, pos, ent_l in sent:
        base, end = pos
        for e in ent_l:
            off, leng = e[0]
            off -= base

        
