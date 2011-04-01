'''
Tools for writing a document graph in dot language
'''

class Graph:
    def __init__ (self):
        self.nodes = list ()
        self.verbs = list ()
        self.archs = list ()

    def add_node (self, node):
        self.nodes.append (node)

    def add_verb (self, verb):
        self.verbs.append (verb)

    def add_arch (self, arch):
        self.archs.append (arch)

    def output_graph (self, name):
        of = open (name + '.gv', 'w')
        of.write ('graph ' + name + ' {\n')
        #self.write_nodes (of)
        self.write_archs (of)
        of.write ('}\n')
        of.close ()


    def write_nodes (self, of):
        for k in self.nodes:
            n = self.nodes[k]
            of.write (str (n[0]) + (' [label="%s"];\n' % n[1] ))

    def write_verbs (self, of):
        pass

    def write_archs (self, of):
        for a in self.archs:
            of.write (a[0] + ' -- ' + a[1] + ';\n')
