
# coding: utf-8

# First look at the data, comparing feature importance from RandomForest classifier

# In[13]:

import warnings
warnings.filterwarnings('ignore')


# In[14]:

from utils_all import *

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt


# In[28]:

get_ipython().magic('store -r df_1_final')


# In[29]:

data = df_1_final


# In[30]:

css_prop = data.iloc[:,9:]


# In[31]:

data_cl = clean_df(data)


# In[32]:

data_cl.shape


# In[33]:

data_cl.url.unique().shape


# In[34]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('name', forest, data)


# In[ ]:




# In[35]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('startDate', forest, data)


# In[36]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('location', forest, data)


# In[37]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('description', forest, data)


# In[ ]:




# In[ ]:




# In[ ]:



