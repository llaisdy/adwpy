#! /usr/bin/env python

from adwpy.api import oov_check, pair_similarity
from adwpy.config import DisambiguationMethod, SignatureComparison
from adwpy.utils import format_dm, format_sc

pairs = {
    'paper': {
        't1': 'a manager fired the worker',
        't2': 'an employee was terminated from work by his boss',
        DisambiguationMethod.NONE: {  ## py
            SignatureComparison.COSINE: 0.09653745464900583,  ## 0.0930320595266
            SignatureComparison.WEIGHTED_OVERLAP: 0.36908219302925027,  ## 0.367446337847
            SignatureComparison.JACCARD: 0.32818303698982393  ## 0.322731465951
             },
        DisambiguationMethod.ALIGNMENT_BASED: {
            SignatureComparison.COSINE: 0.38975614379488677,  ## 0.389764005497
            SignatureComparison.WEIGHTED_OVERLAP: 0.6243046313299656,  ## 0.629662511565
            SignatureComparison.JACCARD: 0.5088887207806945  ## 0.531475176182
             }},
    'g1': {
        't1': 'Study Identifier',
        't2': 'protocol id',
        DisambiguationMethod.NONE: {  ## py
            SignatureComparison.COSINE: 99.99,
            SignatureComparison.WEIGHTED_OVERLAP: 99.99,
            SignatureComparison.JACCARD: 99.99
             },
        DisambiguationMethod.ALIGNMENT_BASED: {
            SignatureComparison.COSINE: 99.99,
            SignatureComparison.WEIGHTED_OVERLAP: 99.99,
            SignatureComparison.JACCARD: 99.99
        }}}

def pair_similarity_test(pair, dm, sc, topk=0):
    text1 = pairs[pair]['t1']
    text2 = pairs[pair]['t2']

    expected = pairs[pair][dm][sc]
    
    (ok, bad) = oov_check(text1 + "  " + text2)

    if not ok:
        badstr = '\n- '.join(["\t".join(b) for b in bad])
        print "Texts contain Out Of Vocabulary terms:\n\n- {}\n\nStopping".format(badstr)
        raise SystemExit
    else:
        actual = pair_similarity(text1, text2, dm, sc, topk)
        print "Disambiguation Method: {}\nSignature Comparison: {}\n".format(format_dm[dm],
                                                                             format_sc[sc])
        print "expected: {}\nactual: {}".format(expected, actual)
        return round(expected, 3) == round(actual, 3)
    
def main():
    pair = 'paper'
    ## pair = 'g1'
    ## dm = DisambiguationMethod.NONE
    dm = DisambiguationMethod.ALIGNMENT_BASED
    sc = SignatureComparison.COSINE
    ## sc = SignatureComparison.WEIGHTED_OVERLAP
    ## sc = SignatureComparison.JACCARD
    
    return pair_similarity_test(pair, dm, sc)

if __name__ == '__main__':
    print main()
