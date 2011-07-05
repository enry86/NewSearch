#!/usr/bin/python

import sys
sys.path.append ('lib')

newsearch_cnf = {
    'test': False
}

calais_cnf = {
    'read': 'files/html_proc',
    'res': 'files/calais_res',
    'key': '33q562d5y52rqsxvfwm9s27e',
    'type': 'text/html',
    'test': False
}

verba_cnf = {
    'out_dir': 'files/test_out',
    'in_dir': 'files/calais_res',
    'graph_dir': 'files/test_graph',
    'storetxt' : True,
    'test': False
}

def main_index (fs):
    from bins import verba_pic
    from bins import calais_client
    from bins import expand
    from bins import relations

    if not newsearch_cnf['test']:
        print 'Starting OpenCalais queries...'
    cal = calais_client.CalaisClient (calais_cnf, fs)
    cal.call_srv ()
    if not newsearch_cnf['test']:
        print 'OpenCalais service queried for %d files' % len (fs)
        print 'Starting documents analysis'
    vrb = verba_pic.Verba_Pickle (verba_cnf)
    vrb.analyze_docs ()
    if not newsearch_cnf['test']:
        print 'Finish documents processing'
    #print 'Expanding documents'
    #exp = expand.ExpandDocs ()
    #exp.start_exp ()
    #print 'Finish document expansion'
    if not newsearch_cnf['test']:
        print 'Computing docs similarity'
    sim = relations.CompSimilarity (newsearch_cnf['test'])
    sim.store_similarity ()
    if not newsearch_cnf['test']:
        print 'Done'

def main_query (q):
    from bins import query

    qa = query.QueryManager ()
    res = qa.run_query (q)
    for r in res:
        print r



if __name__ == '__main__':
    if sys.argv [1] == '-q':
        try:
            query = sys.argv[2]
            main_query (query)
        except KeyError:
            print 'No query provided\n'
            sys.exit (0)
    elif sys.argv [1] == '-t':
        newsearch_cnf['test'] = True
        calais_cnf['test'] = True
        verba_cnf['test'] = True
        files = sys.argv[2:]
        main_index (files)
    else:
        files = sys.argv[1:]
        main_index (files)
