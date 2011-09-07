#!/usr/bin/python

import sys
import numpy

class Qual_meas:
    def __init__ (self, lcn_f, nsc_f):
        self.lcn_f = lcn_f
        self.nsc_f = nsc_f

    def get_res (self):
        avg_l = list ()
        avg_c = list ()
        avg_n = list ()
        print ',ONLY LUCENE,COMMON,ONLY NEWSEARCH'
        for i in range (len (self.lcn_f)):
            nf_lu = self.lcn_f [i]
            nf_ns = self.nsc_f [i]
            hs_lu = self.__read_file (nf_lu)
            hs_ns = self.__read_file (nf_ns)
            res = self.__get_qual (hs_lu, hs_ns)
            l, c, n = res
            tot = float (sum (res))
            print '# Docs,%d,%d,%d' % res
            print 'Perc.,%f,%f,%f\n' % (l / tot, c / tot, n / tot)
            avg_l.append (l/tot)
            avg_c.append (c/tot)
            avg_n.append (n/tot)
        al = numpy.average (avg_l)
        ac = numpy.average (avg_c)
        an = numpy.average (avg_n)
        print '\n,Average Results'
        print 'Perc.,%f,%f,%f' % (al, ac, an)

    def __read_file (self, fname):
        res = list ()
        f = open (fname)
        for l in f:
            if l != '\n':
                s, d = l.split ()
                res.append (d)
        f.close ()
        return res

    def __get_qual (self, lu, ns):
        lu_c = 0
        com_c = 0
        ns_c = 0
        for d in lu:
            if d in ns:
                com_c += 1
                ns.remove (d)
            else:
                lu_c += 1
        ns_c = len (ns)
        return lu_c, com_c, ns_c


def main ():
    lu_f = sys.argv [sys.argv.index ('-l') + 1 : sys.argv.index ('-n')]
    ns_f = sys.argv [sys.argv.index ('-n') + 1 :]
    qm = Qual_meas (lu_f, ns_f)
    qm.get_res ()


if __name__ == '__main__':
    main ()
