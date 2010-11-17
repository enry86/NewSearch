#!/usr/bin/python

import nltk

class Extractor:
    def __init__ (self):
        self.gram = r""" 
                NP: {<.*>+} 
                }<TO>?<MD>*<VB|VB[A-Z]|CC>+<JJ>?{ 
                VP: {<TO>?<MD>*<VB|VB[A-Z]>+<JJ>?}
                S: {<S><CC><S>|<NP>*<VP><NP>*}
                """
        self.pars = nltk.RegexpParser(self.gram)
        self.s_tok = nltk.data.load('tokenizers/punkt/english.pickle')
    
    def get_relationship (self, text, pos):
        res = []
        text = self.mark_ent (text, pos)
        sent = self.s_tok.tokenize(text)
        sent_ent = self.associate_ent (sent, pos)
        base = 0
        for s in sent_ent:
            verb_ent = self.retr_verbs(s, base)
            res.append((s[1], verb_ent))
            base += len(s[0])
        print len(text), base
        return res


    def associate_ent (self, sent, pos):
        base = 0
        ent = 0
        res = []
        for s in sent:
            tmp = []
            while ent < len(pos) and pos[ent][0][0] < (base + len(s)):
                tmp.append(pos[ent])
                ent += 1
            res.append((s, tmp))
            base += len(s)
        return res


    def retr_verbs (self, sen, base):
        words = nltk.word_tokenize (sen[0])
        tags = nltk.pos_tag (words)
        tree = self.pars.parse(tags)
        tree.draw ()
        verbs = self.analyze_tree(tree)
        return verbs

    
    def mark_ent (self, sen, ents):
        res = ''
        prev = 0
        cnt = 0
        added = 0
        for e in ents:
            pos = e[0][0]
            marker =  ' _' + str(cnt)  + '_ '
            res += sen[prev:pos] + marker
            prev = pos
            cnt += 1
        res += sen[prev:]
        return res


    def analyze_tree (self, tree):
        res = []
        for t in tree:
            if type(t) == tuple:
                if t[1].find('VB') >= 0:
                    res.append(t[0])
            elif t.node == 'S':
                res += (self.analyze_tree (t))
            elif t.node.find('VP') >= 0:
                res += (self.analyze_tree (t))
        return res

