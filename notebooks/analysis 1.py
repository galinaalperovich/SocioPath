
# coding: utf-8

# First look at the data, comparing feature importance from RandomForest classifier

# In[1]:

import warnings
warnings.filterwarnings('ignore')


# In[8]:

from utils_all import *

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt


# In[3]:

get_ipython().magic('store -r data')


# In[4]:

css_prop = data.iloc[:,9:]


# In[17]:

df_pos = clean_df(data[data['meta_name'] == 'name'])
# df_neg = clean_df(data[data['meta_name'] != field_name])


# In[9]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('name', forest, data)


# In[ ]:




# In[6]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('startDate', forest, data)


# In[7]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('location', forest, data)


# In[8]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('description', forest, data)


# In[ ]:




# In[ ]:




# In[ ]:



