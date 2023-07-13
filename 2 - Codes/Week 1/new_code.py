# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 10:57:59 2023

@author: ahmed.torky
"""

import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('iris.csv', index_col=0)
sns.pairplot(df, hue="target", diag_kind="hist")
sns.pairplot(df, hue='target')
sns.pairplot(df, kind="kde")

df = pd.read_csv('sample.csv', encoding='Shift-JIS', index_col=0)

plt.figure(figsize=(16, 10))
plt.plot(df.loc[:, ['item2', 'item3']])
plt.xlabel('item2')
plt.ylabel('item3')