#! /usr/bin/env python

import os.path
ROOT_DIRN = os.path.abspath(os.path.dirname(__file__))    

#### PPVS_DIRN: directory name of the ppvs database
PPVS_DIRN = os.path.join(ROOT_DIRN, 'data/ppvs')

#### O2IMAP_FN: wordnet offset -> id map
O2IMAP_FN = os.path.join(ROOT_DIRN, 'data/offset2ID.map.tsv')

class DisambiguationMethod(object):
    NONE, ALIGNMENT_BASED = range(2)

class SignatureComparison(object):
    COSINE, WEIGHTED_OVERLAP, JACCARD = range(3)
                
