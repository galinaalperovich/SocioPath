
# coding: utf-8

# In[31]:

import warnings
warnings.filterwarnings('ignore')


# In[32]:

from utils_all import *

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt


# In[33]:

get_ipython().magic('store -r data')


# In[34]:

css_prop = data.iloc[:,9:]


# In[35]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('name', forest, data)


# In[36]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('startDate', forest, data)


# In[37]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('location', forest, data)


# In[38]:

forest = RandomForestClassifier(n_estimators=100)
perform_analysis_of_field('description', forest, data)


# In[ ]:



