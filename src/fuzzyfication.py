from scipy.stats import norm
from membership_functions import dsigmf, sigmf

"""

3 funkcje:
fuzyfikacja dla GGT względem płci. zwraca 2 funkcje
fuzyfikacja dla ALT oraz AST, jako argument przyjmuje odpowiednią cechę, zwraca 3 funkcje
fuzyfikacja dla BIL oraz ALP, jako argument przyjmuje odpowiednią cechę, zwraca 2 funkcje

zwracane funkcje przyjmują jako argument obiekt klasy pandas.Series, który jest jednym wierszem w danych

bord - górna granica ustalona przez normy medyczne

"""


# fuzyfikacja dla GGT
def fuzzy_ggt():
    def ggt_help(x, type_):
        bord = 35 if x['Sex'] == 'f' else 60
        mean = 1.0 * bord
        tmp = lambda a: sigmf(a, mean, 0.2)
        return tmp(x.GGT)

    good = lambda x: 1. - ggt_help(x, 'good')
    bad = lambda x: ggt_help(x, 'bad')
    return good, bad

# fuzyfikacja ALT oraz AST
def fuzzy_alt_ast(feature):
    def help(x, type_):
        bord = 40
        if type_=='good':
            mean = 1.0 * bord
            tmp = lambda a: sigmf(a, mean, 0.2)
        elif type_=='bad':
            mean_1 = 1.0 * bord
            mean_2 = 2.0 * bord
            tmp = lambda a: dsigmf(a, mean_1, 0.2, mean_2, 0.2)
        else:
            mean = 2.0* bord
            tmp = lambda a: sigmf(a, mean, 0.2)
        return tmp(x[feature])

    good = lambda x: 1. - help(x, 'good')
    bad = lambda x: help(x, 'bad')
    vbad = lambda x: help(x, 'vbad')
    return good, bad, vbad

#fuzyfikacja dla BIL oraz ALP
def fuzzy_bil_alp(feature):
    def help(x, type_):
        if feature == 'BIL':
            bord = 12
        else:
            bord = 100

        mean = 1.0 * bord
        tmp = lambda a: sigmf(a, mean, 0.2)
        return tmp(x[feature])

    good = lambda x: 1. - help(x, 'good')
    bad = lambda x: help(x, 'bad')
    return good, bad