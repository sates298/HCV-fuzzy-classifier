from unicodedata import category
from matplotlib.pyplot import get
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def define_antecedents():
    alp = ctrl.Antecedent(np.arange(501), "alp")
    alt = ctrl.Antecedent(np.arange(401), "alt")
    ast = ctrl.Antecedent(np.arange(401), "ast")
    bil = ctrl.Antecedent(np.arange(301), "bil")
    ggt_male = ctrl.Antecedent(np.arange(701), "ggt_male")
    ggt_female = ctrl.Antecedent(np.arange(701), "ggt_female")

    return alp, alt, ast, bil, ggt_male, ggt_female

def define_antecedents_mfs(antecedents):
    def alp_mfs(alp):
        norm = 100
        alp["good"] = 1. - fuzz.sigmf(alp.universe, b=norm, c=0.2)
        alp["bad"] = fuzz.sigmf(alp.universe, b=norm, c=0.2)

    def bil_mfs(bil):
        norm = 12
        bil["good"] = 1. - fuzz.sigmf(bil.universe, b=norm, c=0.2)
        bil["bad"] = fuzz.sigmf(bil.universe, b=norm, c=0.2)

    def ggt_male_mfs(ggt_male):
        norm = 60
        ggt_male["good"] = 1. - fuzz.sigmf(ggt_male.universe, b=norm, c=0.2)
        ggt_male["bad"] = fuzz.sigmf(ggt_male.universe, b=norm, c=0.2)

    def ggt_female_mfs(ggt_female):
        norm = 35
        ggt_female["good"] = 1. - fuzz.sigmf(ggt_female.universe, b=norm, c=0.2)
        ggt_female["bad"] = fuzz.sigmf(ggt_female.universe, b=norm, c=0.2)

    def alt_mfs(alt):
        norm = 40
        alt["good"] = 1. - fuzz.sigmf(alt.universe, b=norm, c=0.2)
        alt["bad"] = fuzz.dsigmf(alt.universe, norm, 0.2, norm*2, 0.2)
        alt["vbad"] = fuzz.sigmf(alt.universe, b=norm*2, c=0.2)

    def ast_mfs(ast):
        norm = 40
        ast["good"] = 1. - fuzz.sigmf(ast.universe, b=norm, c=0.2)
        ast["bad"] = fuzz.dsigmf(ast.universe, norm, 0.2, norm*2, 0.2)
        ast["vbad"] = fuzz.sigmf(ast.universe, b=norm*2, c=0.2)
    
    def get_mfs_declaration(antecedent):
        return {
            "alp": alp_mfs,
            "alt": alt_mfs, 
            "ast": ast_mfs, 
            "bil": bil_mfs, 
            "ggt_male": ggt_male_mfs,
            "ggt_female": ggt_female_mfs
        }.get(antecedent, Exception("No antecedent like '{}'.".format(antecedent)))

    for antecedent in antecedents:
        antecedent_mfs = get_mfs_declaration(antecedent.label)
        antecedent_mfs(antecedent)

    return antecedents

def define_consequents():
    health = ctrl.Consequent(np.arange(0, 101), "health")
    return health

def define_consequents_mfs(consequent, binary=False):
    if binary:
        consequent["healthy"] = fuzz.trapmf(consequent.universe, abcd=[0, 0, 70, 80])
        consequent["sick"] = fuzz.trapmf(consequent.universe, abcd=[70, 80, 100, 100])

    else:
        consequent["donor"] = fuzz.trapmf(consequent.universe, abcd=[0, 0, 40, 50])
        consequent["suspect_donor"] = fuzz.trapmf(consequent.universe, abcd=[40, 50, 60, 70])
        consequent["hepatitis"] = fuzz.trapmf(consequent.universe, abcd=[50, 60, 70, 80])
        consequent["fibrosis"] = fuzz.trapmf(consequent.universe, abcd=[60, 70, 80, 90])
        consequent["cirrhosis"] = fuzz.trapmf(consequent.universe, abcd=[70, 80, 90, 100])

    return consequent

def define_rules(antecedents, consequent, binary=False):
    alp, alt, ast, bil, ggt_male, ggt_female = antecedents

    if binary:
        rule1 = ctrl.Rule(alp['good'], consequent['healthy'])
        rule2 = ctrl.Rule(alt['bad'], consequent['sick']) 
        rule3 = ctrl.Rule(ast['good'] & alt["vbad"], consequent['sick'])
        rule4 = ctrl.Rule(alt['vbad'] & ast['vbad'], consequent['sick'])
        rule5 = ctrl.Rule((alt['good'] & (ast['bad'] | ast['vbad'])) | (ast['vbad'] & alt['bad']), consequent['sick'])
        rule6 = ctrl.Rule(bil['good'], consequent['healthy'])
        rule7 = ctrl.Rule(bil['bad'], consequent['sick'])

        universal_rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7]

        def define_male_rules():
            rule8 = ctrl.Rule(ggt_male['good'], consequent['healthy'])
            rule9 = ctrl.Rule(ggt_male['bad'] & alp['bad'], consequent["sick"])

            return [rule8, rule9]

        def define_female_rules():
            rule8 = ctrl.Rule(ggt_female['good'], consequent['healthy'])
            rule9 = ctrl.Rule(ggt_female['bad'] & alp['bad'], consequent["sick"])

            return [rule8, rule9]

        male_ctrl = ctrl.ControlSystemSimulation(ctrl.ControlSystem(universal_rules + define_male_rules()))
        female_ctrl = ctrl.ControlSystemSimulation(ctrl.ControlSystem(universal_rules + define_female_rules()))

        return male_ctrl, female_ctrl

    else:
        rule1 = ctrl.Rule(alp['good'], consequent['donor'])
        rule2 = ctrl.Rule(alt['bad'], consequent['hepatitis']) 
        rule3 = ctrl.Rule(ast['good'] & alt["vbad"], consequent['hepatitis'])
        rule4 = ctrl.Rule(alt['vbad'] & ast['vbad'], consequent['cirrhosis'])
        rule5 = ctrl.Rule((alt['good'] & (ast['bad'] | ast['vbad'])) | (ast['vbad'] & alt['bad']), consequent['hepatitis'])
        rule6 = ctrl.Rule(bil['good'], consequent['donor'])
        rule7 = ctrl.Rule(bil['bad'], consequent['suspect_donor'])

        universal_rules = [rule1, rule2, rule3, rule4, rule5, rule6, rule7]

        def define_male_rules():
            rule8 = ctrl.Rule(ggt_male['good'], consequent['donor'])
            rule9 = ctrl.Rule(ggt_male['bad'] & alp['bad'], consequent["fibrosis"])

            return [rule8, rule9]

        def define_female_rules():
            rule8 = ctrl.Rule(ggt_female['good'], consequent['donor'])
            rule9 = ctrl.Rule(ggt_female['bad'] & alp['bad'], consequent["fibrosis"])

            return [rule8, rule9]

        male_ctrl = ctrl.ControlSystemSimulation(ctrl.ControlSystem(universal_rules + define_male_rules()))
        female_ctrl = ctrl.ControlSystemSimulation(ctrl.ControlSystem(universal_rules + define_female_rules()))

        return male_ctrl, female_ctrl



def create_mamdani_system(binary):
    antecedents = define_antecedents()
    consequents = define_consequents()

    antecedents = define_antecedents_mfs(antecedents)
    consequents = define_consequents_mfs(consequents, binary)

    male_ctrl, female_ctrl = define_rules(antecedents, consequents, binary)

    return male_ctrl, female_ctrl


def mamdani_value(sample, male_ctrl, female_ctrl):
    alt_value = sample.ALT
    alp_value = sample.ALP
    ast_value = sample.AST
    bil_value = sample.BIL
    ggt_value = sample.GGT
    
    if sample.Sex == "m":
        male_ctrl.input["alt"] = alt_value
        male_ctrl.input["alp"] = alp_value
        male_ctrl.input["ast"] = ast_value
        male_ctrl.input["bil"] = bil_value
        male_ctrl.input["ggt_male"] = ggt_value
        male_ctrl.compute()
        return male_ctrl.output["health"]

    else:
        female_ctrl.input["alt"] = alt_value
        female_ctrl.input["alp"] = alp_value
        female_ctrl.input["ast"] = ast_value
        female_ctrl.input["bil"] = bil_value
        female_ctrl.input["ggt_female"] = ggt_value
        female_ctrl.compute()
        return female_ctrl.output["health"]

def classify_sample(male_ctrl, female_ctrl, sample, thresholds, return_val):    
    value = mamdani_value(sample, male_ctrl, female_ctrl)
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

def classify(df, thresholds, return_val=False):
    binary = True if len(thresholds) == 1 else False

    male_ctrl, female_ctrl = create_mamdani_system(binary)
    df[['prediction', 'mamdani_value']] = df.apply(lambda x: classify_sample(male_ctrl, female_ctrl, x, thresholds, return_val), 
                                                          axis=1, result_type='expand')

    return df

