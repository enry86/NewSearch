#!/usr/bin/python

import numpy
import sys

class ResAnalyzer:
    def __init__(self):
        self.rows = list ()

    def read (self, f):
        rf = open (f)
        for l in rf:
            self.rows.append (l.split (':'))
        rf.close ()

    def mean_time_bucket (self, bkt_s):
        res_rt = dict ()
        res_qt = dict ()
        for rt, qt, hit, trm, tri, doc in self.rows:
            key = int (tri) / bkt_s
            try:
                res_rt [key].append (float (rt))
            except KeyError:
                res_rt [key] = [float (rt)]
            try:
                res_qt [key].append (float (qt))
            except KeyError:
                res_qt [key] = [float (qt)]
        keys = res_rt.keys ()
        keys.sort ()
        print '0\t0\t0'
        for k in keys:
            print '%d\t%f\t%f' % ((k + 1) * bkt_s, numpy.average (res_rt [k]), numpy.average (res_qt [k]))

    def tri_distr_bucket (self, bkt_s):
        res = dict ()
        for rt, qt, hit, trm, tri, doc in self.rows:
            key = int (tri) / bkt_s
            try:
                res [key] += 1
            except KeyError:
                res [key] = 1
        keys = res.keys ()
        keys.sort ()
        print '0\t0'
        for k in keys:
            print '%d\t%d' % ((k + 1) * bkt_s, res [k])


def main ():
    f = sys.argv[1]
    ra = ResAnalyzer ()
    ra.read (f)
    #ra.mean_time_bucket (50)
    ra.tri_distr_bucket (25)

if __name__ == '__main__':
    main ()
