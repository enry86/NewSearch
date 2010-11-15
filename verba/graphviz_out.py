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

    
