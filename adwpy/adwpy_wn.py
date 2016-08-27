from nltk.corpus import wordnet as wn

def wn_synsets_by_word_pos(word, pos):
    return wn.synsets(word, pos)

def wn_synsets_by_word(word):
    return wn.synsets(word)

def wn_synset_by_pos_offset(pos, offset):
    return wn._synset_from_pos_and_offset(pos,int(offset)).name()
