
# coding: utf-8

# In[1]:

import warnings
warnings.filterwarnings('ignore')


# In[2]:

from utils_all import *

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt


# In[3]:

get_ipython().magic('store -r data_t')


# In[4]:

data_t.shape


# In[10]:

n_estim = 1000


# In[11]:

forest = RandomForestClassifier(n_estimators=n_estim)
perform_analysis_of_field2('name', forest, data_t)


# In[12]:

forest = RandomForestClassifier(n_estimators=n_estim)
perform_analysis_of_field2('startDate', forest, data_t)


# In[13]:

forest = RandomForestClassifier(n_estimators=n_estim)
perform_analysis_of_field2('location', forest, data_t)


# In[14]:

forest = RandomForestClassifier(n_estimators=n_estim)
perform_analysis_of_field2('description', forest, data_t)


# In[ ]:



