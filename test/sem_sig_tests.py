#! /usr/bin/env python

from nltk.corpus import wordnet as wn

from adwpy import sem_sig
from adwpy.utils import snd

def ss_map_test():
    word, pos = ('manager', u'n')
    synsets = wn.synsets(word, pos)
    st = synsets[0]
    ss = sem_sig.sem_sig_for_synset(st)
#    ss.truncate(10)
    fields = '\n'.join(["{}\t{}".format(i,j)
                        for (i,j) in sorted(ss.map.items(), key=snd, reverse=True)])
    print "** ss_map_test\n\nst: {}\n\nss:\n\n{}".format(st, fields)
        
def average_ss_test(wp = ('manager', 'n')):
    word, pos = wp
    ss = sem_sig.average_sem_sig(sem_sig.sem_sigs_for_wordpos(word, pos))
    ## ss.truncate(10)
    fields = '\n'.join(["{}\t{}".format(i,j)
                        for (i,j) in sorted(ss.map.items(), key=snd, reverse=True)])
    print "** average_ss_test\n\nst: {}\n\nss:\n\n{}".format((word, pos), fields)

def ss_for_text_test():
    ts = [('employee', u'n'), (u'terminate', u'v'), ('work', u'n'), (u'boss', u'n')]
    ss = sem_sig.sem_sig_for_text(ts)
    heading = "ss_for_text_test"
    fields = '\n'.join(["{}\t{}".format(i,j)
                        for (i,j) in sorted(ss.map.items(), key=snd, reverse=True)])
    print "** ss_for_text_test\n\nst: {}\n\nss:\n\n{}".format(ts, fields)

def ss_for_synset_test(st):    
    ss = sem_sig.sem_sig_for_synset(wn.synset(st))
##    fields = '\n'.join(["{}\t{}".format(i,j)
##                        for (i,j) in sorted(ss.map.items(), key=snd, reverse=True)])
##    print fields  #"** ss_for_synset_test\n\nst: {}\n\nss:\n\n{}".format(st, fields)
    print sum(ss.map.values())
    
def main(x):
    ss_for_synset_test(x)

if __name__ == '__main__':
    import sys
    x = sys.argv[1]
    main(x)
