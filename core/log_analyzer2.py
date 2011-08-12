#!/usr/bin/python
import sys
import numpy

class LogAnalyzer2:
    def __init__ (self, interval):
        self.inter = interval
        self.pr = list ()
        self.oc = list ()
        self.inde = list ()
        self.inde_avg = list ()
        self.oc_act = ['query', 'read', 'pickle']
        self.pr_act = ['importing', 'preprocessing', 'processing', 'storing']

    def analyze (self, log):
        inf = open (log)
        d_oc = 0
        d_pr = 0
        d_in = 0
        bucket_avg = list ()
        ocal = 0.0
        proc = 0.0
        inde = 0.0
        for l in inf:
            t = l.split ()
            if len (t) == 2:
                val = float (t[1])
                if t[0] in self.oc_act:
                    ocal += val
                elif t[0] in self.pr_act:
                    proc += val
                elif t[0] == 'memo_indexing':
                    inde += val
                    d_in += 1
                    bucket_avg.append (val)
                    if d_in % self.inter == 0:
                        self.inde.append (inde)
                        self.inde_avg.append (numpy.average (bucket_avg))
                        bucket_avg = list ()
                if t[0] == 'pickle':
                    d_oc += 1
                    if d_oc % self.inter == 0:
                        self.oc.append (ocal)
                elif t[0] == 'storing':
                    d_pr += 1
                    if d_pr % self.inter == 0:
                        self.pr.append (proc)
        inf.close ()
        self.__print_result ()

    def __print_result (self):
        for i in range (min (len (self.pr), len (self.oc))):
            docs = (i + 1)  * self.inter
            oc_t = self.oc[i] / 60
            pr_t = self.pr[i] / 60
            in_t = self.inde [i]
            in_a = self.inde_avg [i]
            print '%d\t%f\t%f\t%f\t%f' % (docs, oc_t + pr_t, pr_t, in_t, in_a)


def main ():
    f = sys.argv [1]
    inter = 100
    loga = LogAnalyzer2 (inter)
    loga.analyze (f)


if __name__ == '__main__':
    main()
