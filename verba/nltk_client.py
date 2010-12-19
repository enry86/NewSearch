#!/usr/bin/python

import nltk
import graphviz_out

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
        self.graph = graphviz_out.Graph()
    

    '''
    It works, really...
    '''
    def get_relationship (self, text, pos):
        text = self.mark_ent (text, pos)
        text = nltk.clean_html (text)
        sent = self.s_tok.tokenize(text)
        for s in sent:
            if s.count('_') > 0:
                self.parse_sent (s)
        return self.graph


    '''
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
    '''


    def parse_sent (self, sen):
        words = nltk.word_tokenize (sen)
        tags = nltk.pos_tag (words)
        tree = self.pars.parse (tags)
        self.analyze_sent (tree)

    
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


    def analyze_sent (self, tree):
        orig = list ()
        dest = list ()
        verb = list ()
        for t in tree:
            if type (t) != tuple:
                if t.node == 'S':
                    self.analyze_sent (t)
                elif t.node == 'NP':
                    if len(orig) == 0:
                        orig += self.read_ent (t)
                    else:
                        dest += self.read_ent (t)
                elif t.node == 'VP':
                    verb.append (self.read_verb (t))
        self.update_graph (orig, dest, verb)
    

    def update_graph (self, orig, dest, verb):
        is_dest = len(dest) > 0
        if is_dest:
            for o in orig:
                for d in dest:
                    self.graph.add_arch ((str(o), str(d), ', '.join(verb)))
        else:
            for o in orig:
                self.graph.add_arch ((str(o), str(o), ', '.join(verb)))


    def read_ent (self, tree):
        res = list()
        for w in tree:
            if w[0].count('_') == 2:
                res.append (int (w[0].replace('_','')))
        return res
    

    def read_verb (self, tree):
        res = ''
        for w in tree:
            res += w[0] + ' '
        return res

    '''
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
    '''

