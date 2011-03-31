#!/usr/bin/python

import nltk
import graphviz_out
import re

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
    def get_relationship (self, doc_cal):
        text = doc_cal.doc['info']['document']
        text = self.mark_ent (text, doc_cal.entities)
        text = nltk.clean_html (text)
        sent = self.s_tok.tokenize(text)
        for s in sent:
            self.parse_sent (s)
        return self.graph


    def parse_sent (self, sen):
        words = self.__word_tokenize (sen)
        print words
        tags = nltk.pos_tag (words)
        print tags
        #tree = self.pars.parse (tags)
        #self.analyze_sent (tree)


    def mark_ent (self, text, ents):
        base = 0
        mark_text = str ()
        pos = self.__get_positions (ents)
        for p in pos:
            mark_text += text[base : p[0]]
            mark_text += (' %s ' % p[2])
            base = p[0] + p[1]
        mark_text += text[base:]
        return mark_text


    def __word_tokenize (self, sent):
        r = r"\s*(http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(?:/\S*)?)\s*|\s*([^,:;\(\)!\?\+\s]+)\s*|\s*([,:;\(\)!\?\+])\s*"
        tok = re.findall (r, sent)
        tok = self.__flatten_toks (tok)
        return tok

    def __flatten_toks (self, tok):
        res = list()
        for t in tok:
            tmp = filter (lambda x: x, t)
            res.append (tmp[0])
        return res


    def __get_positions (self, ents):
        res = list ()
        for tmp_ent in ents:
            tmp_lst = tmp_ent['instances']
            tmp_pos = map (lambda x: (x['offset'], x['length'], tmp_ent['__reference']),tmp_lst)
            res += tmp_pos
        res.sort()
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
