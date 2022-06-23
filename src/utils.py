import pandas as pd

def get_data(data_path):
    df = pd.read_csv(data_path, index_col=0)
    df[['Category', 'Category_name']] = df.apply(lambda x: x.Category.split('='), axis=1, result_type='expand')
    df = df.drop(columns=['ALB', 'CHOL', 'CHE', 'CREA', 'PROT'])
    df = df.replace({'Category': {'0': 0, '0s': 1, '1': 2, '2': 3, '3': 4}})
    return df