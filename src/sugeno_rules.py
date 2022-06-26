from enum import Enum
import fuzzyfication as fz
import numpy as np


class Chance(Enum):
    LOW = 0.1
    ANY = 0.8
    MEDIUM = 1.5
    HIGH = 3
    VERY_HIGH = 5

# ALP
def low_alp(sample):
    good, _ = fz.fuzzy_bil_alp('ALP')
    z = Chance.LOW.value
    w = good(sample)
    return z, w

# ALT
def high_alt(sample):
    _, bad, _ = fz.fuzzy_alt_ast('ALT')
    w = bad(sample)
    z = Chance.MEDIUM.value
    return z, w

# AST & ALP
def normal_ast_very_high_alt(sample):
    good_ast, bad_ast, _ = fz.fuzzy_alt_ast('AST')
    *_, vbad_alt = fz.fuzzy_alt_ast('ALT')
    z = Chance.MEDIUM.value
    w = min(vbad_alt(sample), max(good_ast(sample), bad_ast(sample)))
    return z, w

# AST & ALP
def very_high_alt_ast(sample):
    *_, vbad_alt = fz.fuzzy_alt_ast('ALT')
    *_, vbad_ast = fz.fuzzy_alt_ast('AST')
    z = Chance.VERY_HIGH.value
    w = min(vbad_alt(sample), vbad_ast(sample))
    return z, w

# AST & ALP
def long_rule_alt_ast(sample):
    _, bad_ast, vbad_ast = fz.fuzzy_alt_ast('AST')
    good_alt, bad_alt, _ = fz.fuzzy_alt_ast('ALT')
    z = Chance.VERY_HIGH.value
    w = max(
        min(good_alt(sample), max(bad_ast(sample), vbad_ast(sample))),
        min(vbad_ast(sample), bad_alt(sample))
    )
    return z, w

# BIL
def low_bil(sample):
    good, _ = fz.fuzzy_bil_alp('BIL')
    z = Chance.LOW.value
    w = good(sample)
    return z, w

# BIL
def high_bil(sample):
    _, bad = fz.fuzzy_bil_alp('BIL')
    w = bad(sample)
    z = Chance.ANY.value
    return z, w

# GGT
def low_ggt(sample):
    good, _ = fz.fuzzy_ggt()
    z = Chance.LOW.value
    w = good(sample)
    return z, w

# GGT & ALP
def high_ggt(sample):
    _, bad_ggt = fz.fuzzy_ggt()
    _, bad_alp = fz.fuzzy_bil_alp('ALP')
    z = Chance.HIGH.value
    w = min(bad_ggt(sample), bad_alp(sample))
    return z, w


def get_sugeno_rules():
    return [
        low_alp,
        low_ggt,
        low_bil,
        high_ggt,
        high_bil,
        high_alt,
        normal_ast_very_high_alt,
        very_high_alt_ast,
        long_rule_alt_ast
    ]

def sugeno_value(sample):
    rules = get_sugeno_rules()
    wzs = np.array([rule(sample) for rule in rules])  
    values = wzs.prod(axis=1).sum()
    weights = wzs[:, 1].sum()
    return values/weights

def classify(sample, thresholds, return_val=False):
    value = sugeno_value(sample)
    category = -1 
    for i, threshold in enumerate(thresholds):
        if value < threshold:
            category = i
            break
    if category < 0:
        category = len(thresholds)
    if return_val:
        return category, value
    return category