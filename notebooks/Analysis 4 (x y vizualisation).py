
# coding: utf-8

# In[1]:

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from utils_all import *
get_ipython().magic('matplotlib inline')


# http://stackoverflow.com/questions/2369492/generate-a-heatmap-in-matplotlib-using-a-scatter-data-set

# In[93]:

get_ipython().magic('store -r df_1_final')


# In[94]:

data = df_1_final


# In[95]:

data_cl = clean_df(data)


# In[96]:

num_features = ['x_coords','y_coords']

data_cl = data_cl.dropna(axis=0)
data_num = data_cl[num_features]
data_num = data_num[data_num.applymap(lambda x: isinstance(x, (int, float)))]
data_cl[num_features] = data_num
data_cl = data_cl.dropna(axis=0)


# In[97]:

data_xy = data_cl[['meta_name','x_coords','y_coords']]


# In[98]:

from matplotlib.pyplot import hist2d, xlim, ylim


# In[99]:

smpl.head()


# In[101]:

import matplotlib.ticker as ticker


# In[102]:

def draw_hex(meta_name, df, ylim=(960,0), xlim=(0,1000)):
    dataXY = df[df.meta_name == meta_name]
    try:
        smpl = dataXY.sample(1000)
    except Exception as e:
        smpl = dataXY
    g = sns.jointplot(x=smpl.x_coords, y=smpl.y_coords, kind='scatter', ylim=ylim, xlim=xlim)

    g.ax_joint.xaxis.set_major_locator(ticker.MultipleLocator(100))
    g.ax_joint.yaxis.set_major_locator(ticker.MultipleLocator(100))

    plt.show()


# In[103]:

draw_hex('location', data_xy)


# In[104]:

draw_hex('startDate', data_xy)


# In[105]:

draw_hex('name', data_xy)


# In[106]:

draw_hex('description', data_xy)


# ## The center of rectangule

# In[107]:

data_rect = data_cl[['meta_name','x_coords','y_coords', 'block_height', 'block_width']]


# In[108]:

data_rect['x1'] = data_rect.x_coords
data_rect['y1'] = data_rect.y_coords


# In[109]:

data_rect['x2'] = data_rect.x_coords + data_rect.block_width
data_rect['y2'] = data_rect['y1']


# In[110]:

data_rect['x3'] = data_rect['x1']
data_rect['y3'] = data_rect['y1'] + data_rect.block_height


# In[111]:

data_rect['x4'] = data_rect['x3'] + data_rect.block_width
data_rect['y4'] = data_rect['y3']


# In[112]:

data_block_centers = pd.DataFrame()
data_block_centers['x_coords'] = data_rect.x1 + (data_rect.x2 - data_rect.x1)/2
data_block_centers['y_coords'] = data_rect.y1 + (data_rect.y3 - data_rect.y1)/2
data_block_centers['meta_name'] = data_rect.meta_name


# Dataframe with the centers of corresponding blocks

# If the average web page size is 960 pixels and the average screen width is 1024 pixel
# https://www.iteracy.com/blog/post/size-and-layout-of-a-web-page

# In[113]:

draw_hex('name', data_block_centers, ylim=(5000,0))


# In[114]:

draw_hex('description', data_block_centers, ylim=(5000,0))


# In[115]:

draw_hex('location', data_block_centers,  ylim=(5000,0))


# In[116]:

draw_hex('startDate', data_block_centers,  ylim=(5000,0))


# In[156]:

data_block_centers.columns = ['x_center', 'y_center', 'meta_name']


# In[157]:

xy_data = pd.concat(axis=1, objs=
          [
            data_cl[['x_coords','y_coords', 'block_height', 'block_width']],
            data_block_centers
          ])


# In[160]:

xy_data.groupby('meta_name').hist()


# In[166]:

xy_data.groupby('meta_name').block_width.plot(kind='hist', alpha=0.5)


# In[167]:

xy_data.groupby('meta_name').block_height.plot(kind='hist', alpha=0.5)


# In[169]:

xy_data.groupby('meta_name').x_center.plot(kind='hist', alpha=0.5)


# In[171]:

xy_data.groupby('meta_name').y_center.plot(kind='hist', alpha=0.4)


# In[172]:

xy_data.groupby('meta_name').x_coords.plot(kind='hist', alpha=0.5)


# In[173]:

xy_data.groupby('meta_name').y_coords.plot(kind='hist', alpha=0.5)


# In[131]:

xy_data.groupby('meta_name').describe()


# In[179]:

df_1_final[['url','meta_name','x_coords','y_coords', 'block_height', 'block_width']].values[:100,:]


# In[ ]:



