'''
Tools for writing a document graph in dot language
'''

class Graph:
    def __init__ (self):
        self.sents = list ()
        self.nodes = list ()
        self.verbs = list ()
        self.archs = list ()

    def add_node (self, node):
        self.nodes.append (node)
        return 'node_' + str (len (self.nodes) -1)

    def add_verb (self, verb):
        self.verbs.append (verb)
        return 'verb_' + str (len (self.verbs) -1)

    def add_sent (self, sent):
        self.sents.append (sent)
        return 'sent_' + str (len (self.sents) -1)

    def add_arch (self, arch):
        self.archs.append (arch)

    def output_graph (self, name):
        of = open (name + '.gv', 'w')
        of.write ('graph ' + name + ' {\n')
        self.write_nodes (of, 'sent_', self.sents)
        self.write_nodes (of, 'node_', self.nodes)
        self.write_nodes (of, 'verb_', self.verbs)
        self.write_archs (of)
        of.write ('}\n')
        of.close ()


    def write_nodes (self, of, lab, lst):
        for i,n in enumerate (lst):
            of.write (lab + str (i) + (' [label="%s"];\n' % n))


    def write_archs (self, of):
        for a in self.archs:
            of.write (a[0] + ' -- ' + a[1] + ';\n')
