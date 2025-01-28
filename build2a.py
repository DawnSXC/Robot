import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from pickle import dump
import os
from pandas.plotting import scatter_matrix


file_path = "SCFP2009panel.xlsx"
dataset = pd.read_excel(file_path)
print(type(dataset))
print(dataset.shape)

# Asserts
dataset['Risky_Assets_2007'] = dataset['NMMF07']+dataset['STOCKS07']+dataset['BOND07']
dataset['Risky_Assets_2009'] = dataset['NMMF09']+dataset['STOCKS09']+dataset['BOND09']

# Free Asserts
dataset['Risk_Free_Assets_2007'] = dataset['LIQ07']+dataset['CDS07']+dataset['SAVBND07']+dataset['CASHLI07']
dataset['Risk_Free_Assets_2009'] = dataset['LIQ09']+dataset['CDS09']+dataset['SAVBND09']+dataset['CASHLI09']


# Risk Tolerance
sp500_2007 = 1478
sp500_2009 = 948

dataset['Risk_Tolerance_2007'] = dataset['Risky_Assets_2007'] / (dataset['Risk_Free_Assets_2007']+ dataset['Risky_Assets_2007'])
dataset['Risk_Tolerance_2009'] = dataset['Risky_Assets_2009'] / (dataset['Risky_Assets_2009']+dataset['Risk_Free_Assets_2009']) * (sp500_2009/sp500_2007)

sns.histplot(
    data=dataset,
    x='Risk_Tolerance_2007',
    bins=int(180/5),
    color='blue',
    edgecolor='black'
)
plt.show()

