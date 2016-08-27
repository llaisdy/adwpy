#! /usr/bin/env python

import os.path

from adwpy_wn import wn_synsets_by_word
import alignment, comparison, sem_sig, utils
from config import DisambiguationMethod, SignatureComparison


def oov_check(text):
    "Checks input text for Out Of Vocaulary terms, either 'no synsets' or 'synset not in ppv database'"
    bad = []
    for (w,p) in utils.cook(text):
        sts = wn_synsets_by_word(w)
        if len(sts) == 0:
            bad.append([w, "No synsets", "n/a"])
        else:
            for st in sts:
                ss = sem_sig.sem_sig_for_synset(st, False)
                sfn = ss.get_src_fn()
                if not os.path.isfile(sfn):
                    bad.append([w, st.name(), os.path.basename(sfn)])
    return (not bad, bad)

def oov_filter(text):
    "Removes Out Of Vocaulary terms from input text; returns (word, pos) pairs"
    ok = []
    for (w,p) in utils.cook(text):
        sts = wn_synsets_by_word(w)
        if len(sts):
            for st in sts:
                ss = sem_sig.sem_sig_for_synset(st, False)
                sfn = ss.get_src_fn()
                if os.path.isfile(sfn):
                    ok.append((w,p))
                    continue
    return ok

def hack_bos_to_boss(wps):
    "The WordNet lemmatizer lemmatises 'boss' to 'bos'.  This function changes it back again.  Not generally useful, but needed for the example text from the Pilehvar paper."
    out = []
    for (i,j) in wps:
        if i == 'bos':
            i = 'boss'
        ## elif (i,j) == ('id','v'):
        ##     j = 'n'
        out.append((i,j))
    return out

def pair_similarity(s1, s2, dm, sc, topk=0):
    ts1 = hack_bos_to_boss(utils.cook(s1))
    ts2 = hack_bos_to_boss(utils.cook(s2))
    print "** Cooked texts:\nts1: {}\nts2: {}\n".format(ts1, ts2)

    if dm == DisambiguationMethod.NONE:
        as1 = sem_sig.sem_sig_for_wps(ts1)
        as2 = sem_sig.sem_sig_for_wps(ts2)
    elif dm == DisambiguationMethod.ALIGNMENT_BASED:
        ds1, ds2 = alignment.align(ts1, ts2, sc, topk)
        as1 = sem_sig.average_sem_sig(ds1)
        as2 = sem_sig.average_sem_sig(ds2)
    print "** sem sig map lengths: {}, {}\n".format(len(as1.map), len(as2.map))
        
    return comparison.compare(as1, as2, sc, topk)

