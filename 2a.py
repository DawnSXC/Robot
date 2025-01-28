import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from pickle import dump
import os

file_path = "SCFP2009panel.xlsx"
dataset = pd.read_excel(file_path)

print(dataset.shape)
print(dataset.head())

# Asserts
dataset['Risky_Assets_2007'] = dataset['NMMF07']+dataset['STOCKS07']+dataset['BOND07']
dataset['Risky_Assets_2009'] = dataset['NMMF09']+dataset['STOCKS09']+dataset['BOND09']

dataset['Risk_Free_Assets_2007'] = dataset['LIQ07']+dataset['CDS07']+dataset['SAVBND07']+dataset['CASHLI07']
dataset['Risk_Free_Assets_2009'] = dataset['LIQ09']+dataset['CDS09']+dataset['SAVBND09']+dataset['CASHLI09']

sp500_2007 = 1478
sp500_2009 = 948

dataset['Risk_Tolerance_2007'] = (dataset['Risky_Assets_2007'] / (dataset['Risk_Free_Assets_2007']+ dataset['Risky_Assets_2007'])) 
dataset['Risk_Tolerance_2009'] = (dataset['Risky_Assets_2009'] / (dataset['Risky_Assets_2009']+dataset['Risk_Free_Assets_2009'])) * (sp500_2009/sp500_2007)

import copy
dataset2 = copy.deepcopy(dataset)


dataset2['Risk_Tolerance_Change'] = abs(dataset2['Risk_Tolerance_2009']/dataset2['Risk_Tolerance_2007']-1)*100

#check null value
print('Null Values = ',dataset2.isnull().values.any())

# Risk Tolerance 2007
plt.hist(dataset2['Risk_Tolerance_2007'], bins=int(180/5), color='blue', alpha=0.7)
plt.xlabel('Risk Tolerance 2007')
plt.ylabel('Frequency')
plt.title('Risk Tolerance Distribution (2007)')
plt.show()

#Risk Tolerance 2009
plt.hist(dataset2['Risk_Tolerance_2009'], bins=int(180/5), color='red', alpha=0.7)
plt.xlabel('Risk Tolerance 2009')
plt.ylabel('Frequency')
plt.title('Risk Tolerance Distribution (2009)')
plt.show()

intelligent_investors = dataset2[dataset2['Risk_Tolerance_Change'] < 10]
selected_columns = [
    'AGE07', 'EDCL07', 'MARRIED07', 'KIDS07', 
    'OCCAT107', 'INCOME07','RISK07', 'NETWORTH07',   
    'Risk_Tolerance_2007'
]
selected_dataset = intelligent_investors[selected_columns]

#heatmap
correlation = selected_dataset.corr()
plt.figure(figsize=(15,15))
plt.title('Correlation Matrix')
sns.heatmap(correlation,vmax=1,square=True,annot=True,cmap='cubehelix')

#scatterplots
from pandas.plotting import scatter_matrix
plt.figure(figsize=(15,15))
scatter_matrix(selected_dataset,figsize=(12,12))
plt.show()

#model save
from pickle import dump
from pickle import load

dump(selected_dataset,open('build_lab2a.sav','wb'))