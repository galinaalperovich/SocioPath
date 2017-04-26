
# coding: utf-8

# In[81]:

from utils_all import *
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.manifold import TSNE


# In[82]:

from time import time
from matplotlib import offsetbox
from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)


# In[1]:

get_ipython().magic('store -r data')


# In[2]:

data


# In[160]:

data_cl = clean_df(data)


# In[161]:

y = data_cl['meta_name']
X = data_cl.drop('meta_name', 1)
X = X.replace('none', 'NA')
X_lim = X[['x_coords','y_coords','block_height','block_width','num_siblings']]
le = LabelEncoder()
le_tag = le.fit_transform(X.tag.values)
X_lim.loc[:,'tag'] = le_tag


# In[162]:

X = X_lim


# In[164]:

X.applymap(lambda x: isinstance(x, (int, float)))


# In[165]:

X


# In[180]:

X1 = X[X.applymap(lambda x: isinstance(x, (int, float)))]


# In[183]:

model = TSNE(n_components=2, random_state=0)
X_tsne = model.fit_transform(X1) 


# In[70]:

vis_x = X_tsne[:, 0]
vis_y = X_tsne[:, 1]
tsne = pd.DataFrame({'x1': X_tsne[:, 0], 'x2': X_tsne[:, 1], 'meta_name': y, })


# In[71]:

tsne.head()


# In[157]:

tsne_lim = tsne[tsne['meta_name'].isin(['location', 'name', 'description', 'startDate'])]

tsne_smpl = tsne_lim.sample(n=200)
groups = tsne_smpl.groupby('meta_name')
fig, ax = plt.subplots()
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling
for name, group in groups:
    ax.plot(group.x1, group.x2, marker='o', linestyle='', ms=12, label=name)
ax.legend()

plt.show()


# In[125]:

import seaborn as sns
get_ipython().magic('matplotlib inline')


# In[158]:

tsne_smpl = tsne_lim.sample(n=1000)

g = sns.lmplot('x1', 'x2', tsne_smpl, hue='meta_name', fit_reg=False, size=8
                ,scatter_kws={'alpha':0.7,'s':60})
g.axes.flat[0].set_title('Scatterplot of a 50D dataset reduced to 2D using t-SNE')


# In[129]:

from sklearn.decomposition import IncrementalPCA


# In[155]:

ipca = IncrementalPCA(n_components=2, batch_size=3)


# In[156]:

pca = ipca.fit_transform(X)
x_pca = pd.DataFrame({'x1': x_pca[:, 0], 'x2': x_pca[:, 1], 'meta_name': y, })


# In[ ]:

pca_smpl = x_pca.sample(n=1000)

g = sns.lmplot('x1', 'x2', pca_smpl, hue='meta_name', fit_reg=False, size=8
                ,scatter_kws={'alpha':0.7,'s':60})
g.axes.flat[0].set_title('Scatterplot of a 50D dataset reduced to 2D using t-SNE')


# In[107]:

def get_XY_tsne(field_name, data):
    df_pos = data[data['meta_name'] == field_name]
    df_neg = data[data['meta_name'] != field_name]
    
    no_field_smpl = df_neg.sample(n = df_pos.shape[0], random_state=7)
    real_meta = no_field_smpl.meta_name 
    no_field_smpl = no_field_smpl.drop('meta_name', 1)
    no_field_smpl.insert(1, 'meta_name', 'no_'+ field_name)
    X_field = pd.concat((df_pos, no_field_smpl), axis=0)
    y = X_field['meta_name']
    X_field = X_field.drop('meta_name', 1)
    X_field = X_field.replace('none', 'NA')
    
    X = X_field
    
    X['y'] = y
    X = X.convert_objects(convert_numeric=True).dropna()
    y = X['y']
    X = X.drop('y', 1)
    return X, y, real_meta


# In[119]:

def perform_analysis_tsne(X, y, clf, field_name):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=7)
    clf.fit(X_train, y_train)
    print('{} prediction'.format(field_name))
    print("train: {}, test: {}".format(clf.score(X_train, y_train), clf.score(X_test, y_test)))
    draw_feature_importance(clf, X_train, field_name)


# In[120]:

fields = ['location', 'name', 'description', 'startDate']
for field_name in fields:
    forest = RandomForestClassifier(n_estimators=100)
    X, y, real_meta = get_XY_tsne(field_name, tsne)
    perform_analysis_tsne(X, y, forest, field_name)


# In[ ]:



