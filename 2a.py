import copy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from pickle import dump
import os
# 加载数据
file_path = "/Users/xuechendawn/IdeaProjects/robot/SCFP2009panel.xlsx"
dataset = pd.read_excel(file_path)

# 查看数据结构
print(dataset.shape)
print(dataset.head())

##计算

# 定义风险资产列
dataset['Risky_Assets_2007'] = dataset['NMMF07']+dataset['STOCKS07']+dataset['BOND07']
dataset['Risky_Assets_2009'] = dataset['NMMF09']+dataset['STOCKS09']+dataset['BOND09']

# 定义无风险资产列
dataset['Risk_Free_Assets_2007'] = dataset['LIQ07']+dataset['CDS07']+dataset['SAVBND07']+dataset['CASHLI07']
dataset['Risk_Free_Assets_2009'] = dataset['LIQ09']+dataset['CDS09']+dataset['SAVBND09']+dataset['CASHLI09']


# 计算风险容忍度（Risk Tolerance）
# 使用给定的 S&P500 指数进行标准化
sp500_2007 = 1478
sp500_2009 = 948

dataset['Risk_Tolerance_2007'] = (dataset['Risky_Assets_2007'] / (dataset['Risk_Free_Assets_2007']+ dataset['Risky_Assets_2007'])) 
dataset['Risk_Tolerance_2009'] = (dataset['Risky_Assets_2009'] / (dataset['Risky_Assets_2009']+dataset['Risk_Free_Assets_2009'])) * (sp500_2009/sp500_2007)


# 计算风险容忍度变化的百分比
dataset['Risk_Tolerance_Change'] = abs((dataset['Risk_Tolerance_2009'] - dataset['Risk_Tolerance_2007']) / dataset['Risk_Tolerance_2007']) * 100

# 筛选聪明投资者：风险容忍度变化小于 10%
intelligent_investors = dataset[dataset['Risk_Tolerance_Change'] < 10]

#np.abs(rt09/rt07-1)

print("Null Values =", dataset.isnull().values.any())
dataset.dropna(inplace=True)
print("Null Values =", dataset.isnull().values.any())

#hist=True,ked=True,bins=int(100/5)
# 绘制 2007 年风险容忍度分布
plt.hist(dataset['Risk_Tolerance_2007'], bins=50, color='blue', alpha=0.7)
plt.xlabel('Risk Tolerance 2007')
plt.ylabel('Frequency')
plt.title('Risk Tolerance Distribution (2007)')
plt.show()

# 绘制 2009 年风险容忍度分布
plt.hist(dataset['Risk_Tolerance_2009'], bins=50, color='red', alpha=0.7)
plt.xlabel('Risk Tolerance 2009')
plt.ylabel('Frequency')
plt.title('Risk Tolerance Distribution (2009)')
plt.show()


# 定义需要保留的变量
selected_columns = [
    'AGE07', 'EDCL07', 'MARRIED07', 'KIDS07', 
    'OCCAT107', 'INCOME07','RISK07', 'NETWORTH07',   
    'Risk_Tolerance_2007'
]

# 筛选数据集
selected_dataset = intelligent_investors[selected_columns]

# 检查选定特征与目标变量的相关性
correlation_matrix_selected = selected_dataset.corr()

# 绘制热图
plt.figure(figsize=(15, 15))
sns.heatmap(correlation_matrix_selected, annot=True, cmap='cubehelix')
plt.title('Correlation Matrix (Selected Features)')
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt

# Assuming 'selected_dataset' is your DataFrame containing the selected features
# Remove any non-numeric columns if present
numeric_cols = selected_dataset.select_dtypes(include=[np.number]).columns.tolist()
numeric_dataset = selected_dataset[numeric_cols]

# Generate the scatterplot matrix
sns.pairplot(numeric_dataset)
plt.suptitle('Scatterplot Matrix of Selected Features', y=1.02)
plt.show()



#from pickle import dump
#from pickle import load

#dump(dataset,open('build_lab2a.sav'),'wb')


