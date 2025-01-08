import pandas as pd

def crosstab_summary(df, truth, test):
    t = pd.crosstab(df[truth], df[test], dropna=False)

    
    try:
        t.loc['yes', 'yes']
    except:
        t.loc['yes','yes'] = 0

    try:
        t.loc['yes', 'no']
    except:
        t.loc['yes','no'] = 0

    try:
        t.loc['no', 'no']
    except:
        t.loc['no','no'] = 0

    try:
        t.loc['no', 'yes']
    except:
        t.loc['no','yes'] = 0


    # Calculate sensitivity
    sensitivity = specificity = accuracy = ppv = npv = None
    if t.loc['yes','yes'] > 0 or t.loc['yes','no'] > 0:
        sensitivity = t.loc['yes', 'yes'] / (t.loc['yes', 'yes'] + t.loc['yes', 'no'])

    # Calculate specificity
    if t.loc['no','no'] > 0 or t.loc['no','yes'] > 0:
        specificity = t.loc['no', 'no'] / (t.loc['no', 'no'] + t.loc['no', 'yes'])
    # Calculate accuracy
    accuracy = (t.loc['no', 'no'] + t.loc['yes', 'yes']) / t.sum().sum()
    # Calculate ppv
    if t.loc['yes','yes'] > 0 or t.loc['no','yes'] > 0:
        ppv = t.loc['yes', 'yes']/ (t.loc['yes', 'yes'] + t.loc['no', 'yes'])
    # Calculate npv
    if t.loc['no','no'] > 0 or t.loc['yes','no'] > 0:
        npv = t.loc['no', 'no'] / (t.loc['no', 'no'] + t.loc['yes', 'no'])


    summary_output = {'Sensitivity' : sensitivity, 'Specificity' : specificity, 'Accuracy' : accuracy, 'ppv' : ppv, 'npv' : npv}

    # Return sensitivity, specificity, accuracy, ppv, and npv as a dictionary
    return pd.DataFrame.from_dict(summary_output, orient='index').T

    


