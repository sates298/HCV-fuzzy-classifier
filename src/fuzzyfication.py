from scipy.stats import norm


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
        mean = 1.15*bord if type_=='good' else 0.85*bord
        std = 0.2*bord
        dist = norm(loc=mean, scale=std)
        distmax = dist.pdf(mean)
        tmp = lambda a: dist.pdf(a)/distmax
        if type_=='good':
            val = x.GGT if x.GGT < mean else mean
        else:
            val = x.GGT if x.GGT > mean else mean
        return tmp(val)
    good = lambda x: 1. - ggt_help(x, 'good')
    bad = lambda x: 1. - ggt_help(x, 'bad')
    return good, bad

# fuzyfikacja ALT oraz AST
def fuzzy_alt_ast(feature):
    def help(x, type_):
        bord = 40
        if type_=='good':
            mean = 1.15*bord
        elif type_=='bad':
            mean = 0.85*bord
        else:
            mean = 2.85*bord
        std = 0.2*bord
        dist = norm(loc=mean, scale=std)
        distmax = dist.pdf(mean)
        tmp = lambda a: dist.pdf(a)/distmax
        if type_=='good':
            val = x[feature] if x[feature] < mean else mean
        else:
            val = x[feature] if x[feature] > mean else mean
        return tmp(val)
    good = lambda x: 1. - help(x, 'good')
    bad = lambda x: 1. - help(x, 'bad')
    vbad = lambda x: 1. - help(x, 'vbad')
    return good, bad, vbad

#fuzyfikacja dla BIL oraz ALP
def fuzzy_bil_alp(feature):
    def help(x, type_):
        if feature == 'BIL':
            bord = 12
        else:
            bord = 120

        if type_=='good':
            mean = 1.15*bord
        elif type_=='bad':
            mean = 0.85*bord
            
        std = 0.2*bord
        dist = norm(loc=mean, scale=std)
        distmax = dist.pdf(mean)
        tmp = lambda a: dist.pdf(a)/distmax
        if type_=='good':
            val = x[feature] if x[feature] < mean else mean
        else:
            val = x[feature] if x[feature] > mean else mean
        return tmp(val)
    good = lambda x: 1. - help(x, 'good')
    bad = lambda x: 1. - help(x, 'bad')
    return good, bad