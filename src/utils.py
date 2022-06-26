import pandas as pd

def get_data(data_path, binary=False):
    df = pd.read_csv(data_path, index_col=0)
    df[['Category', 'Category_name']] = df.apply(lambda x: x.Category.split('='), axis=1, result_type='expand')
    df = df.drop(columns=['ALB', 'CHOL', 'CHE', 'CREA', 'PROT'])

    if binary:
        df = df.replace({'Category': {'0': 0, '0s': 0, '1': 1, '2': 1, '3': 1}})
        df = df.replace({'Category_name': {'Blood Donor': "Healthy", 'suspect Blood Donor': "Healthy",
                         'Hepatitis': "Sick", 'Fibrosis': "Sick", 'Cirrhosis': "Sick"}})
    else:
        df = df.replace({'Category': {'0': 0, '0s': 1, '1': 2, '2': 3, '3': 4}})

    return df