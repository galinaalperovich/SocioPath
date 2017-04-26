
# coding: utf-8

# In[106]:

import warnings
warnings.filterwarnings('ignore')


# In[107]:

import matplotlib.pyplot as plt


# In[108]:

import pandas as pd
import numpy as np
import os


# In[109]:

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


# ### Data loading and first cleaning
# 

# In[110]:

DATA_PATH = '/Users/jetbrains/Yandex.Disk.localized/Diploma/data_parsed/'
files = os.listdir(DATA_PATH)[1:]


# In[111]:

with open("DATA.csv", "wb") as outfile:
    for f in files:
        with open(DATA_PATH + f, "rb") as infile:
            outfile.write(infile.read())


# In[112]:

data_from_many = pd.read_csv('DATA.csv', delimiter='\t')


# In[113]:

data_from_many.head()


# In[114]:

# without id
data1 = pd.read_csv('/Users/jetbrains/PycharmProjects/SocioPath/data/data.csv', )

# with id, filtered type
data2 = pd.read_csv('/Users/jetbrains/PycharmProjects/SocioPath/data/data1.csv')
data3 = pd.read_csv('/Users/jetbrains/PycharmProjects/SocioPath/data/data2.csv')
data2 = data2.drop('id', 1)
data3 = data3.drop('id', 1)
data_from_first = pd.concat((data1, data2, data3), axis=0)
data_from_first.head(50)


# In[115]:

data_from_many.columns = data_from_first.columns


# In[116]:

data = pd.concat((data_from_many, data_from_first), axis=0)


# In[117]:

data_from_many.columns


# In[118]:

data.shape


# In[119]:

data.url.unique().size


# In[120]:

get_ipython().magic('store data')


# In[ ]:



