#!/usr/bin/python

import sys
sys.path.append ('lib')

from bins import verba_pic
from bins import calais_client
from bins import expand
from bins import relations

calais_cnf = {
    'read': 'files/html_proc',
    'res': 'files/calais_res',
    'key': '33q562d5y52rqsxvfwm9s27e',
    'type': 'text/html'
}

verba_cnf = {
    'out_dir': 'files/test_out',
    'in_dir': 'files/calais_res',
    'graph_dir': 'files/test_graph',
    'storetxt' : True
}

def main (fs):
    print 'Starting OpenCalais queries...'
    cal = calais_client.CalaisClient (calais_cnf, fs)
    cal.call_srv ()
    print 'OpenCalais service queried for %d files' % len (fs)
    print 'Starting documents analysis'
    vrb = verba_pic.Verba_Pickle (verba_cnf)
    vrb.analyze_docs ()
    print 'Finish documents processing'
    #print 'Expanding documents'
    #exp = expand.ExpandDocs ()
    #exp.start_exp ()
    #print 'Finish document expansion'
    print 'Computing docs similarity'
    sim = relations.CompSimilarity ()
    sim.store_similarity ()
    print 'Done'



if __name__ == '__main__':
    files = sys.argv[1:]
    main (files)
