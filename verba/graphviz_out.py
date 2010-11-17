'''
Tools for wirting a document graph in dot language
'''

class Graph:
    def __init__ (self):
        self.nodes = []
        self.archs = []

    def add_node (self, node):
        self.nodes.append (node)

    def add_arch (self, arch):
        self.archs.append (arch)

    def output_graph (self, name):
        of = open (name + '.gv', 'w')
        of.write ('graph ' + name + ' {\n')
        self.write_archs (of)
        of.write ('}\n')
        of.close ()

    
    def write_archs (self, of):
        for a in self.archs:    
            of.write (a[0] + ' -- ' + a[1] + ' [label="' + a[2]  + '"];\n')



