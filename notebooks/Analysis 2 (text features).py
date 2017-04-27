
# coding: utf-8

# In[20]:

from utils_all import *
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.manifold import TSNE
import seaborn as sns
get_ipython().magic('matplotlib inline')
import inspect
from sklearn.decomposition import IncrementalPCA
from sklearn import manifold


# In[21]:

get_ipython().magic('store -r data')
get_ipython().magic('store -r df_1_final')


# In[22]:

data = df_1_final


# In[23]:

data_cl = clean_df(data)


# In[24]:

len(list(filter(lambda x: x,data_cl.text.isnull())))


# In[25]:

data_cl.shape


# First of all, let's create several obviouse features: 
# - len of the text
# - number of punctuation
# - number of digits
# - #numbers/len
# - number of upper case
# 
# Links: https://www.quora.com/Natural-Language-Processing-What-are-the-possible-features-that-can-be-extracted-from-text
# 

# In[26]:

import re
import string


# In[27]:

data_cl['text_str'] = data_cl.text.apply(str).replace('nan','')


# In[28]:

data_cl['text_len'] = data_cl.text_str.apply(len)


# In[29]:

count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))


# In[30]:

data_cl['num_punctuation'] = data_cl.text_str.apply(lambda x: count(x, string.punctuation))


# In[31]:

data_cl['num_digits'] = data_cl.text_str.apply(lambda x: count(x, string.digits))


# In[32]:

data_cl['digits_share'] = data_cl.num_digits/data_cl.text_len


# In[33]:

data_cl['num_upper'] = data_cl.text_str.apply(lambda x: count(x, string.ascii_uppercase))


# In[34]:

data_cl['num_upper'] = data_cl.text_str.apply(lambda x: count(x, string.whitespace))


# In[35]:

data_cl


# In[36]:

data_t = data_cl


# In[37]:

get_ipython().magic('store data_t')


# ## TF-IDF matrix

# In[64]:

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer


# In[65]:

vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.7)
X_t = vectorizer.fit_transform(data_t.text_str)


# In[70]:

get_ipython().magic('store X_t')


# In[ ]:




# In[ ]:



