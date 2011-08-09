#!/usr/bin/python

import utils.database
import sys
sys.path.append ('lib')

newsearch_cnf = {
    'test': False,
    'hexa_memo': True
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
    from bins import index

    db = utils.database.DataBaseMysql ()
    if not  db.db_up:
        print 'Database error'
        sys.exit (1)
    if not newsearch_cnf['test']:
        print 'Starting OpenCalais queries...'
    cal = calais_client.CalaisClient (calais_cnf, fs)
    cal.call_srv ()
    if not newsearch_cnf['test']:
        print 'OpenCalais service queried for %d files' % len (fs)
        print 'Starting documents analysis'
    vrb = verba_pic.Verba_Pickle (verba_cnf, db)
    vrb.analyze_docs ()
    if not newsearch_cnf['test']:
        print 'Finish documents processing'

    ind = index.Indexer (newsearch_cnf['test'], db)
    index_memo = ind.build_index ()
    if not newsearch_cnf['test']:
        print 'Index Built'

    #print 'Expanding documents'
    #exp = expand.ExpandDocs ()
    #exp.start_exp ()
    #print 'Finish document expansion'

    if not newsearch_cnf['test']:
        print 'Computing docs similarity'
    if newsearch_cnf['hexa_memo'] == True:
        sim = index.IndexSimilarity (newsearch_cnf['test'], index_memo, db)
    else:
        sim = relations.CompSimilarity (newsearch_cnf['test'], db)
    sim.store_similarity ()
    db.close_con ()
    if not newsearch_cnf['test']:
        print 'Done'

def main_query (q):
    from bins import query
    from bins import index
    index_memo = None
    db = utils.database.DataBaseMysql ()
    if newsearch_cnf['hexa_memo']:
        if not newsearch_cnf['test']:
            print '#Building Index...'
        ind = index.Indexer (newsearch_cnf['test'], db)
        index_memo = ind.build_index ()
        if not newsearch_cnf['test']:
            print '#Index Built'
    qa = query.QueryManager (index_memo, newsearch_cnf['test'], newsearch_cnf['hexa_memo'], db)
    res = qa.run_query (q)
    res.sort ()
    db.close_con ()
    for r in res:
        print r[0], r[1]


def main_index_test ():
    from bins import index
    import time
    test = False
    db = utils.database.DataBaseMysql ()
    ind = index.Indexer (test, db)
    start = time.time ()
    index_memo = ind.build_index ()
    stop = time.time ()
    print 'Index built: %f' % (stop - start)
    raw_input ('Press any key...')

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
    elif sys.argv [1] == '-i':
        main_index_test ()
    else:
        files = sys.argv[1:]
        main_index (files)
