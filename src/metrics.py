import plotly.express as px
from numpy import average
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


def count_metrics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='macro')
    rec = recall_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')
    return acc, prec, rec, f1

def print_metrics(name, acc, prec, rec, f1):
    print(f'{name}')
    print('accuracy:\t', acc)
    print('precision:\t', prec)
    print('recall:\t\t', rec)
    print('f1 score:\t', f1)

def confussion_matrix(y_true, y_pred, binary=False):
    cf_matrix = confusion_matrix(y_true, y_pred, normalize='pred')

    fig = px.imshow(cf_matrix,
                    labels=dict(x="Ground truth", y="Predictions", color="F1 score"),
                    x=["Healthy", "Sick"] if binary else ["Blood donor", "Suspect blood donor", "Hepatitis", "Fibrosis", "Cirrhosis"],
                    y=["Healthy", "Sick"] if binary else ["Blood donor", "Suspect blood donor", "Hepatitis", "Fibrosis", "Cirrhosis"])
    fig.show()
