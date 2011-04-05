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



    '''
    It works, really...
    '''
    def get_relationship (self, doc_cal):
        self.graph = graphviz_out.Graph()
        text = doc_cal.doc['info']['document']
        text = self.mark_ent (text, doc_cal.entities)
        text = nltk.clean_html (text)
        sent = self.s_tok.tokenize(text)
        for i, s in enumerate (sent):
            self.parse_sent (s, i)
        return self.graph


    def parse_sent (self, sen, i):
        words = self.__word_tokenize (sen)
        tags = nltk.pos_tag (words)
        tree = self.pars.parse (tags)
        s_gr = self.analyze_sent (tree)
        self.update_graph (s_gr, i)


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
        np = list ()
        verb = str ()
        res = list ()
        for t in tree:
            if type (t) != tuple:
                if t.node == 'S':
                    res += (self.analyze_sent (t))
                elif t.node == 'NP':
                    np_tmp = self.read_tree (t)
                    if np_tmp:
                        np.append (np_tmp)
                elif t.node == 'VP':
                    verb = (self.read_tree (t))
        if verb or np:
            res.append ((verb, np))
        return res


    def read_tree (self, tree):
        res = str ()
        for w in tree:
            res += w[0] + ' '
        return res


    def update_graph (self, s_gr, s_id):
        verbs = list ()
        graph_v = str ()
        graph_s = self.graph.add_sent (s_id)
        for v, np in s_gr:
            if v:
                v = v.replace ('"', "'")
                graph_v = self.graph.add_verb (v)
            if graph_v:
                self.graph.add_arch ((graph_s, graph_v))
            for n in np:
                n = n.replace ('"', "'")
                graph_n = self.graph.add_node (n)
                if graph_v:
                    self.graph.add_arch ((graph_v, graph_n))
