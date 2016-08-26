#! /usr/bin/env python

from adwpy import comparison, sem_sig
from adwpy_wn import wn_synsets_by_word_pos

def align(wps1, wps2, sc, topk=0):
    """
    Parameters: wps1 and wps2 are lists of (word, pos) pairs. sc is a signature comparison method name (see config).
    Output: two lists of semantic signatures.
    For each word in each input list, this returns the Semantic Signature of the synset with highest similarity score to a synset from the other input list. 
    """
    t1 = safe_dict(wps1)
    t2 = safe_dict(wps2)
    return align_dicts(t1, t2, sc, topk)

def align_dicts(t1, t2, sc, topk):
    p1, p2 = prime(t1, t2, sc, topk)
    o1 = maximise(p1)
    o2 = maximise(p2)
    return (o1, o2)

def safe_dict(wps):
    return safetify(dictify(wps))

#### private

def dictify(wps):
    """
    Parameter: a list of (word, pos) pairs.
    Output: a nested dictionary: {(word,pos): {sem_sig: {}}}.
    Where sem_sig is a Semantic Signature (see sem_sig.py).
    """
    d = {}
    for wp in wps:
        d[wp] = {}
        for st in wn_synsets_by_word_pos(wp[0], wp[1]):
            ss = sem_sig.sem_sig_for_synset(st)
            d[wp][ss] = {}
    return d

def prime(t1, t2, sc, topk=0):
    for wp1 in t1:
        for ss1 in t1[wp1]:
            for wp2 in t2:
                for ss2 in t2[wp2]:
                    score = comparison.compare(ss1, ss2, sc, topk)
                    t1[wp1][ss1][ss2] = score
                    t2[wp2][ss2][ss1] = score
    return (t1, t2)

def safetify(d):
    "Remove keys with empty values"
    for k in d.keys():
        if d[k] == {}:
            d.pop(k)
    return d

def maximise(d):
    """
    Parameter: a dictionary as produced by dictify.
    Output: a list of sem_sigs.
    For each (word,pos) pair in the dictionary - {(word,pos): {sem_sig: {other: score}}} - this returns the sem_sig with highest score.
    """
    return [sorted([(max(d[wp][ss].values()), ss)
                    for ss in d[wp]],
                    reverse=True)[0][1]
            for wp in d]
