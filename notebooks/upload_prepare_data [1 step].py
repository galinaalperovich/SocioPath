
# coding: utf-8

# In[1]:

import warnings
warnings.filterwarnings('ignore')


# In[2]:

import matplotlib.pyplot as plt


# In[3]:

import pandas as pd
import numpy as np
import os


# In[4]:

from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, LabelEncoder


# In[5]:

import paramiko


# ### Upload new data from MetaCentrum

# In[7]:

def load_remote_data():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('skirit.metacentrum.cz', username='shchegal', password='Intend1@12')
    local_dir = 'data_parsed'
    local_files = os.listdir(local_dir)
    remote_dir = '/storage/brno2/home/shchegal/Diploma/parser/data_parsed'
    sftp = ssh.open_sftp()
    dir_items = sftp.listdir_attr(remote_dir)
    for item in dir_items:
        file_name = item.filename
        if item.filename not in local_files:
            local_path = os.path.join(local_dir, file_name)
            remote_path = remote_dir + '/' + file_name
            sftp.get(remote_path, local_path)


# In[8]:

# Do it only if you have a new data
load_remote_data()


# ### Data loading and first cleaning
# 

# In[9]:

# DATA_PATH = '/Users/jetbrains/Yandex.Disk.localized/Diploma/data_parsed/'
DATA_PATH_REMOTE = 'data_parsed/'
# files = os.listdir(DATA_PATH)[1:]
files_remote = os.listdir(DATA_PATH_REMOTE)[1:]


# In[10]:

with open("DATA.csv", "wb") as outfile:
#     for f in files:
#         with open(DATA_PATH + f, "rb") as infile:
#             outfile.write(infile.read())
    for f in files_remote:
        with open(DATA_PATH_REMOTE + f, "rb") as infile:
            outfile.write(infile.read())


# In[11]:

data_from_many = pd.read_csv('DATA.csv', delimiter='\t')


# In[12]:

data_from_many.head()


# In[13]:

# without id
data1 = pd.read_csv('/Users/jetbrains/PycharmProjects/SocioPath/data/data.csv', )

# with id, filtered type
data2 = pd.read_csv('/Users/jetbrains/PycharmProjects/SocioPath/data/data1.csv')
data3 = pd.read_csv('/Users/jetbrains/PycharmProjects/SocioPath/data/data2.csv')
data2 = data2.drop('id', 1)
data3 = data3.drop('id', 1)
data_from_first = pd.concat((data1, data2, data3), axis=0)
data_from_first.head(50)


# In[14]:

data_from_many.columns = data_from_first.columns


# In[15]:

# data = pd.concat((data_from_many, data_from_first), axis=0)
data = data_from_many


# In[16]:

data.shape


# In[17]:

data.url.unique().size


# In[18]:

get_ipython().magic('store data')


# In[ ]:



