#! /usr/bin/env python

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

import config

format_dm = {config.DisambiguationMethod.NONE: "None",
             config.DisambiguationMethod.ALIGNMENT_BASED: "Alignment-based"}

format_sc = {config.SignatureComparison.COSINE: "Cosine",
             config.SignatureComparison.WEIGHTED_OVERLAP: "Weighted overlap",
             config.SignatureComparison.JACCARD: "Jaccard"}

def snd(x):
    "return second element"
    return x[1]


stopset = set(stopwords.words("english"))
wnl = WordNetLemmatizer()

tt_wn_tagmap = {'J': wn.ADJ,
                'N': wn.NOUN,
                'R': wn.ADV,
                'V': wn.VERB}

def get_wordnet_pos(treebank_tag):
    "The NLTK tokeniser uses 'Treebank' pos labels.  This function converts to WordNet pos labels"
    return tt_wn_tagmap.get(treebank_tag[0], '')

def cook(s):
    "converts a string into a list of (lemma, pos) pairs"
    tagged = nltk.pos_tag(nltk.word_tokenize(s.lower()))
    wnts = [(i, get_wordnet_pos(j)) for (i,j) in tagged]

    return [(wnl.lemmatize(i, pos=j), j)
            for (i,j) in wnts
            if j and (i not in stopset)]

