#! /usr/bin/env python

from config import SignatureComparison

#### api

def compare(as1, as2, sc, topk=0):
    """
    Parameters:
    - as1, as2: SemSigs (see sem_sig.py)
    - sc: signature comparison method
    - topk (int): optional top-k used in Jaccard method
    Returns: float in range 0.0-1.0
    """
    if sc == SignatureComparison.COSINE:
        c = cosine_compare_sem_sigs(as1, as2)
    elif sc == SignatureComparison.WEIGHTED_OVERLAP:
        c = weighted_overlap_compare_sem_sigs(as1, as2)
    elif sc == SignatureComparison.JACCARD:
        c = jaccard_compare_sem_sigs(as1, as2, topk)
    return c


#### private


max_poss_d = {
    0:0, 1:0.5,           2:0.75,               3:0.916666666667,    4:1.04166666667,
    5:1.14166666667,      6:1.225,              7:1.29642857143,     8:1.35892857143,
    9:1.41448412698,     10:1.46448412698,    11:1.50993867244,    12:1.55160533911,
    13:1.59006687757,    14:1.62578116328,    15:1.65911449661,    16:1.69036449661,
    17:1.71977626132,    18:1.7475540391,     19:1.77386982857,    20:1.79886982857,
    21:1.82267935238,    22:1.84540662511,    23:1.86714575554,    24:1.88797908888,
    25:1.90797908888,    26:1.92720985811,    27:1.94572837663,    28:1.96358551948,
    29:1.98082689879,    30:1.99749356546,    31:2.01362259772,    32:2.02924759772,
    33:2.04439911287,    34:2.05910499522,    35:2.07339070951,    36:2.0872795984,
    37:2.10079311191,    38:2.11395100665,    39:2.12677151947,    40:2.13927151947,
    41:2.15146664142,    42:2.16337140332,    43:2.1749993103,     44:2.18636294666,
    45:2.19747405778,    46:2.20834362299,    47:2.21898192087,    48:2.22939858753,
    49:2.23960266916,    50:2.24960266916,    51:2.25940659073,    52:2.26902197535,
    53:2.27845593761,    54:2.28771519687,    55:2.29680610596,    56:2.30573467739,
    57:2.31450660722,    58:2.32312729687,    59:2.33160187314,    60:2.33993520648,
    61:2.34813192779,    62:2.35619644392,    63:2.36413295185,    64:2.37194545185,
    65:2.37963775955,    66:2.38721351712,    67:2.39467620369,    68:2.40202914486,
    69:2.40927552168,    70:2.41641837882,    71:2.42346063234,    72:2.43040507678,
    73:2.43725439185,    74:2.44401114861,    75:2.45067781528,    76:2.45725676264,
    77:2.46375026914,    78:2.47016052555,    79:2.47648963947,    80:2.48273963947,
    81:2.48891247898,    82:2.49501003995,    83:2.50103413634,    84:2.50698651729,
    85:2.51286887023,    86:2.51868282372,    87:2.52442995016,    88:2.53011176834,
    89:2.53572974587,    90:2.54128530142,    91:2.54677980692,    92:2.55221458953,
    93:2.55759093361,    94:2.56291008255,    95:2.56817324044,    96:2.57338157378,
    97:2.57853621295,    98:2.58363825377,    99:2.58868875882,    100:2.59368875882
    }


def cosine_compare_sem_sigs(s1, s2):
    s1.normalise()
    s2.normalise()
    n1 = s1.euclidean_norm()
    n2 = s2.euclidean_norm()
    if (n1 == 0) or (n2 == 0):
        return 0.0
    else:
        return dot_product(s1.map, s2.map) / (n1 * n2)

def dot_product(m1, m2):
    return sum([m1[k] * m2.get(k, 0) for k in m1])


def weighted_overlap_compare_sem_sigs(s1, s2):
    s = overlap(s1, s2)
    rs1 = s1.ranks(s)
    rs2 = s2.ranks(s)
    total = sum([1.0/(i+j) for (i,j) in zip(rs1, rs2)])
    ls = len(s)
    if ls > 100:
        max_poss = sum([1.0/(x*2.0) for x in range(1,len(s)+1)])
    else:
        max_poss = max_poss_d[ls]
    if total == 0.0 or max_poss == 0.0:
        return 0.0
    else:
        return total / max_poss

def overlap(s1, s2):
    return [k for k in s1.map if k in s2.map]

    
def jaccard_compare_sem_sigs(s1, s2, topk=0):
    if topk > 0:
        s1.truncate(topk)
        s2.truncate(topk)
    p = len(overlap(s1, s2))
    return p * 1.0 / (len(s1.map) + len(s2.map) - p)
