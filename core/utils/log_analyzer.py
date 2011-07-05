#!/usr/bin/python

import sys
import numpy

class LogAnalyzer:
    def __init__ (self):
        self.res = {
            'importing': 0.0,
            'preprocessing': 0.0,
            'processing': 0.0,
            'storing': 0.0,
            'read': 0.0,
            'query': 0.0,
            'pickle': 0.0,
            'relationship':0.0
            }


    def analyze (log):
        log_f = open (log)
        for l in log_f:
            t = l.split ()
            if len (t) == 2:
                try:
                    self.res[t[0]] += float (t[1])
                except KeyError:
                    pass
        log_f.close ()

    def print_res (self):
        imp = numpy.average (self.res['importing'])
        pre = numpy.average (self.res['preprocessing'])
        pro = numpy.average (self.res['processing'])
        sto = numpy.average (self.res['storing'])
        rea = numpy.average (self.res['read'])
        que = numpy.average (self.res['query'])
        pic = numpy.average (self.res['pickle'])
        rel = numpy.average (self.res['relationship'])

        print 'QUERY OPENCALAIS:    %f' % (rea + que + pic)
        print 'Read time:           %f' % rea
        print 'Query time:          %f' % que
        print 'Storage time:        %f' % pic
        print '\n'

        print 'INDEXING:            %f' % (imp + pre + pro + sto)
        print 'Importing time:      %f' % imp
        print 'Preprocessing time:  %f' % pre
        print 'Processing time:     %f' % pro
        print 'Storage time:        %f' % sto
        print '\n'

        print 'COMP. RELATINOSHIPS: %f' % rel



if __name__ == '__main__':
    log = sys.argv[1]
    a =  LogAnalyzer ()
    a.analyze (log)
