
# coding: utf-8

# In[1]:

get_ipython().magic('matplotlib inline')


# In[2]:

import warnings
warnings.filterwarnings('ignore')

import seaborn as sns
from utils_all import *


# ## Load and clean data

# In[3]:

get_ipython().magic('store -r data')


# In[50]:

data.shape


# In[52]:

data[data.meta_name == 'startDate'].shape


# In[4]:

data.head()


# Clean data (remove rows with mets tag, ZERO width, height, x and y coordinates)

# In[5]:

df = clean_df(data)


# In[53]:

df.shape


# In[54]:

df[df.meta_name == 'startDate'].shape


# In[7]:

df.columns


# ## Pages with one event

# Number of unique urls

# In[8]:

len(df.url.unique())


# Number of events per one url

# In[9]:

df_sdate = df[df.meta_name == 'startDate']


# In[10]:

df_sdate.head()


# In[11]:

sdate_unique = df_sdate.url.value_counts().reset_index()
sdate_unique.columns = ['url', 'count_dates']


# In[12]:

sns.distplot(sdate_unique.count_dates)


# Number of pages with 1 event

# In[13]:

len(sdate_unique[sdate_unique.count_dates == 1])


# Number of events with more than 1 events

# In[14]:

len(sdate_unique[sdate_unique.count_dates > 1])


# Urls only with one event

# In[15]:

urls_1 = sdate_unique[sdate_unique.count_dates == 1].url


# In[16]:

urls_1.head()


# Sub dataframe with only one event

# In[17]:

df_1 = df[df.url.isin(urls_1)]


# Compare the shape of original dataframe and filtered urls

# In[18]:

df.shape


# In[19]:

df_1.shape


# In[20]:

get_ipython().magic('store df_1')


# ### About URLs and domains

# Number of originally unique urls

# In[21]:

data.url.unique().size


# Number of unique urls in one-event pages (=> number of different events)

# In[22]:

df_1.url.unique().size


# In[23]:

url = df_1.url.iloc[4]


# In[24]:

def get_domain(url):
    parts = url.split('//', 1)
    return parts[1].split('/', 1)[0].replace('www.','')


# In[25]:

df['domain'] = df.url.apply(get_domain)
df_1['domain'] = df_1.url.apply(get_domain)


# ###  Number of domains

# Number of unique domains for original datasets

# In[26]:

df.domain.unique().size


# Number of unique domains for urls with one event

# In[27]:

df_1.domain.unique().size


# That means there are around 17 pages per one domain.

# In[28]:

df_1.url.unique().size/df_1.domain.unique().size


# In[29]:

# return the number of domain with the cut
def get_df_dom_count(df_1):
    df_1_dom_count = df_1.domain.value_counts().reset_index()
    df_1_dom_count.columns = ['domain', 'count_domain']
    df_1_dom_count.count_domain[df_1_dom_count.count_domain > 100] = 100
    return df_1_dom_count


# In[30]:

df_1_dom_count = df_1.domain.value_counts().reset_index()
df_1_dom_count.columns = ['domain', 'count_domain']


# In[31]:

sns.distplot(df_1_dom_count.count_domain)


# We will cut the number of pages per domain, we need to decide by what value.

# In[32]:

df_1_dom_count.count_domain[df_1_dom_count.count_domain >= 100].hist()


# In[33]:

df_1_dom_count.count_domain[df_1_dom_count.count_domain > 10][df_1_dom_count.count_domain < 500].hist()


# In[34]:

df_1_dom_count.count_domain[df_1_dom_count.count_domain > 100] = 100


# In[35]:

df_1_dom_count.count_domain.sum()


# In[36]:

df_1_dom_count.count_domain.hist()


# In[37]:

df_1_dom_count.count_domain.hist()


# In[38]:

df_1_dom_count = get_df_dom_count(df_1)


# In[39]:

df_1_dom_count.head()


# ### Remove those domains which are too frequent

# In[40]:

df_1_dom_count_100 = df_1_dom_count.domain[df_1_dom_count.count_domain == 100]

def is_kept(s):
    global df_1_dom_count_100
    c = df_1_dom_count.count_domain[df_1_dom_count.domain == s].values[0]
    if c != 0:
        df_1_dom_count.count_domain[df_1_dom_count.domain == s] = c - 1
        return 1
    else:
        return 0


# In[41]:

df_1_100 = df_1[df_1.domain.isin(df_1_dom_count_100)]
df_1_not_100 = df_1[~df_1.domain.isin(df_1_dom_count_100)]

df_1_100.shape, df_1_not_100.shape


# In[42]:

# WARNING: time-consuming procedure, we keep the globabl variable df_1_dom_count 
# and stop when there is a limit for this particular domain

df_1_100['keep'] = df_1_100.domain.apply(is_kept)
df_1_not_100['keep'] = 1


# In[43]:

df_1_all = pd.concat(axis=0, objs=[df_1_100, df_1_not_100])


# In[44]:

df_1_final = df_1_all[df_1_all['keep'] == 1]


# In[45]:

df_1_final


# In[46]:

df_1_dom_count_final = get_df_dom_count(df_1_final)


# In[56]:

df_1_final.shape


# In[47]:

df_1_final[df_1_final.meta_name == 'startDate'].shape


# In[57]:

get_ipython().magic('store df_1_final')


# Properties of the df_1_final dataset:
#   * It is cleaned (without zero - x, y, width, heigt vlues, without meta tags)
#   * It containes at most 100 different urls for one domain
#   * Every page contains only 1 event, the rest is removed
#   * Doesn't contain duplicates by numeric features

# In[58]:

df_1_final


# In[ ]:



