#! /usr/bin/env python

from nltk.corpus import wordnet as wn

from adwpy.config import PPVS_DIRN, O2IMAP_FN

class SemSig(object):
    def __init__(self, ppvs_dirn=""):
        self.ppvs_dirn = ppvs_dirn
        self.synset = None
        self.map = {} # {synset_id: weight}
        self.ksvs = [] # cache for keys sorted by val
        self.rnkd = {} # cache for ranks

    def __repr__(self):
        return "SemSig('{}')".format(self.synset.name())
        
    def set_synset(self, synset):
        self.synset = synset

    def load(self):
        "loads semantic signature from file"
        previous = ''
        for line in open(self.src_fn()).readlines():
            synset_id, weight = line.split('\t')
            if not weight.strip():
                weight = previous
            else:
                previous = weight
            self.map[int(synset_id)] = float(weight)
        self.load_ksvs()
        self.load_rnkd()

    def save(self, fn, tr=5000):
        out = ''
        if self.ksvs == []:
            self.load_ksvs()
        for k in self.ksvs[:tr]:
            out += '{}\t{}\n'.format(k, self.map[k])
        open(fn, 'w').write(out)

    def load_ksvs(self):
        self.ksvs = self.keys_sorted_by_val()

    def load_rnkd(self):
        for r, k in enumerate(self.ksvs):
            self.rnkd[k] = r+1

    def truncate(self, length):
        """
        Parameter: int
        Limits self.map to the <length> keys with highest value
        """
        self.map = dict([(j,i) for (i,j) in
                         sorted([(v,k) for (k,v) in self.map.items()],
                                reverse=True)[:length]])

    def normalise(self):
        "makes it so that sum(self.map.values()) == 1.0"
        s = sum(self.map.values())
        for k in self.map:
            self.map[k] /= s

    def euclidean_norm(self):
        import math
        return math.sqrt(sum([i * i for i in self.map.values()]))

    def ranks(self, keys):
        """
        Parameter: list of ints
        returns the rank of each key in keys
        where "rank" is position in a list of keys sorted by their values
        """
        if self.ksvs == []:
            self.load_ksvs()
        if self.rnkd == {}:
            self.load_rnkd()
        mykeys = self.ksvs
        ret = [self.rnkd[k] for k in keys]
        return ret

    def report(self):  ## was report(self, n):
        if self.ksvs == []:
            self.load_ksvs()
        i2omap = get_i2omap()
        for k in self.ksvs:  #keys:
            lab = synset_for_id(k, i2omap)
            print '{}\t{}'.format(lab, self.map[k])

    def keys_sorted_by_val(self):
        "return list of keys sorted by descending value"
        return [j for (i,j) in
                sorted([(v,k) for (k,v) in self.map.items()], reverse=True)]

    def src_fn(self):
        "source path and filename of this semantic signature"
        offset = str(self.synset.offset()).zfill(8)
        pos = anrv(self.synset.pos())
        gpar = offset[0:2]
        par  = offset[2:4]
        path = '{}/{}/{}/{}-{}.ppv'.format(self.ppvs_dirn, gpar, par,
                                           offset, pos)
        return path

def anrv(x):
    "converts wordnet 's' pos tag to 'a' for use with semantic signature database"
    if x == 's': return 'a'
    else: return x

def get_i2omap():
    d = {}
    for line in open(O2IMAP_FN).readlines():
        o,i = line.strip().split('\t')
        d[i] = o
    return d

def synset_for_id(i, i2o):
    return offset_to_synset(i2o[str(i)])

def offset_to_synset(x):
    o,p = x.split('-')
    return wn._synset_from_pos_and_offset(p,int(o)).name()
    
def sem_sig_for_synset(synset, load=True):
    ss = SemSig(PPVS_DIRN)
    ss.set_synset(synset)
    if load is True:
        ss.load()
    return ss

def sem_sig_for_wps(wps):
    "Parameter wps is a list of (word, pos) pairs"
    ss = []
    for (word, pos) in wps:
        ss.append(average_sem_sig(sem_sigs_for_wordpos(word, pos)))
    if len(ss) == 1:
        return ss[0]
    else:
        return average_sem_sig(ss)

def sem_sigs_for_wordpos(word, pos):    
    ss = [sem_sig_for_synset(s) for s in wn.synsets(word, pos)]
    return ss

def average_sem_sig(ss):
    """
    Parameter: list of SemSigs
    Returns: SemSig
    returned SemSig.map has mean value for each key in union of map keys in input SemSigs
    """
    a = SemSig()
    for s in ss:
        for k in s.map:
            a.map.setdefault(k, 0)
            a.map[k] += s.map[k]
    for k in a.map:
        a.map[k] /= len(ss)
    return a

#### test
    
def test(ppvs_dirn):
    word = 'manager'
    pos = 'n'
    ss = sem_sigs_for_wordpos(word, pos)
    asg = average_sem_sig(ss)
    asg.normalise()
    print sum(asg.map.values())
    assert(round(sum(asg.map.values())) == 1.0)
    asg.truncate(100)
    assert(len(asg.map) == 100)
    print asg

if __name__ == '__test__':
    main(ppvs_dirn)
