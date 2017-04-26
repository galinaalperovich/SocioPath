
# coding: utf-8

# In[1]:

from utils_all import *
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.manifold import TSNE
import seaborn as sns
get_ipython().magic('matplotlib inline')
import inspect
from sklearn.decomposition import IncrementalPCA
from sklearn import manifold


# In[2]:

from time import time
from matplotlib import offsetbox
from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)


# In[287]:

get_ipython().magic('store -r data')
get_ipython().magic('store -r data_t')


# In[288]:

data_t


# In[243]:

data_cl = clean_df(data)


# In[284]:

def prepare_num_XY(data_cl, num_features):
    data_cl = data_cl.dropna(axis=0)
    data_num = data_cl[num_features]
    data_num = data_num[data_num.applymap(lambda x: isinstance(x, (int, float)))]
    data_cl[num_features] = data_num
    data_cl = data_cl.dropna(axis=0)
    y = data_cl['meta_name']
    X = data_cl.drop('meta_name', 1)
    le = LabelEncoder()
    le_tag = le.fit_transform(X.tag.values)
    X.loc[:,'tag'] = le_tag
    return X, y, le_tag


# In[285]:

data_cl = data_cl[['meta_name','x_coords','y_coords','block_height','block_width','num_siblings', 'tag']]
num_features = ['x_coords','y_coords','block_height','block_width','num_siblings']
X, y, le_tag = prepare_num_XY(data_cl, num_features)


# In[368]:

def run_dim_reduction_and_draw(data, labels, model, title):
    X_model = model.fit_transform(data)
    tsne = pd.DataFrame({'x1': X_model[:, 0], 'x2': X_model[:, 1], 'meta_name': labels, })
    tsne_lim = tsne[tsne['meta_name'].isin(['location', 'name', 'description', 'startDate'])]
    tsne_smpl = tsne_lim.sample(n=4000)
    g = sns.lmplot('x1', 'x2', tsne_smpl, hue='meta_name', fit_reg=False, size=8,scatter_kws={'alpha':0.7,'s':60})
    g.axes.flat[0].set_title(title)
    return X_model


# In[272]:

perplexity=20
learning_rate=1000.0
model = TSNE(n_components=2,
           random_state=0,
           perplexity=perplexity,
           learning_rate=learning_rate)
title = 'Method: {}, perplexity: {}, learning_rate: {}'.format(method, perplexity, learning_rate)
run_dim_reduction_and_draw(X, y, model, title)


# In[277]:

model = IncrementalPCA(n_components=2, batch_size=3)
title = 'Method: PCA'
run_dim_reduction_and_draw(X, y, model, title)


# In[281]:

model = manifold.MDS(n_components=2, max_iter=100, n_init=1)
title = 'Method: MDS'
run_dim_reduction_and_draw(data=X, labels=y, model, title)


# Dimensionality reduction did not show clear clusters, that means that either the fieatures are not well saparable or these methods don't shoe the structure and we need more complicated methods and classifiers for the data. 
# Good exmplanations are here: 
# 
# http://distill.pub/2016/misread-tsne/
# https://www.quora.com/Is-it-indistinguishable-if-t-SNE-method-does-not-show-clear-two-clusters-for-2-class-classification-problem-1

# In[107]:

def get_XY_tsne(field_name, data):
    df_pos = data[data['meta_name'] == field_name]
    df_neg = data[data['meta_name'] != field_name]
    
    no_field_smpl = df_neg.sample(n = df_pos.shape[0], random_state=0)
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

# fields = ['location', 'name', 'description', 'startDate']
# for field_name in fields:
#     forest = RandomForestClassifier(n_estimators=100)
#     X, y, real_meta = get_XY_tsne(field_name, tsne)
#     perform_analysis_tsne(X, y, forest, field_name)


# ### Dim reduction for X with additional text features

# Let's do the same dim reduction but with additional text features from notebook "Analysis 3". We will see if the result differs from the first try. 

# In[289]:

data_cl = clean_df(data_t)


# In[290]:

data_cl


# In[291]:

data_cl = data_cl[['meta_name','x_coords','y_coords','block_height','block_width',
                   'num_siblings', 'tag', 'text_len', 'num_punctuation','num_digits',
                   'digits_share','num_upper','num_space']]
num_features = ['x_coords','y_coords','block_height','block_width',
                   'num_siblings', 'text_len', 'num_punctuation','num_digits',
                   'digits_share','num_upper','num_space']
X, y, le_tag = prepare_num_XY(data_cl, num_features)


# In[295]:

run_dim_reduction_and_draw(X, y, 50.0, 1000.0)


# In[297]:

run_dim_reduction_and_draw(X, y, method='pca')


# We see that description is already looks more or less like a cluster. Probably the important field was a text length.

# ## t-sne only for text-related fields

# In[305]:

perplexity=20
learning_rate=1000.0

model = TSNE(n_components=2,
           random_state=0,
           perplexity=perplexity,
           learning_rate=learning_rate, n_iter=200)
title = 'Method: t-SNE, perplexity: {}, learning_rate: {}'.format(perplexity, learning_rate)
run_dim_reduction_and_draw(X.iloc[:,5:], y, model, title)


# ### PCA

# In[306]:

model = IncrementalPCA(n_components=2, batch_size=3)
title = 'Method: PCA'
run_dim_reduction_and_draw(X, y, model, title)


# In[308]:

model = manifold.MDS(n_components=2, max_iter=300, n_init=1)
title = 'Method: MDS'
run_dim_reduction_and_draw(X, y, model, title)


# In[344]:

get_ipython().magic('store -r X_t')


# ### Dimensionality reduction for TF-IDF feature (sparse matrix)

# In[345]:

X_t_df = pd.DataFrame(X_t.toarray(), columns=range(28738))


# In[346]:

X_t_df.shape


# In[347]:

data_t.shape


# In[355]:

data_t.index = range(6140)
X_t_df.index = range(6140)


# In[356]:

X_text = pd.concat([X_t_df, data_t], axis=1)


# In[359]:

X_text_cl = clean_df(X_text)


# In[364]:

X_t = X_text_cl.iloc[:,:28738]


# In[365]:

y_t = X_text['meta_name']


# #### PCA for tf-idf

# In[366]:

model = IncrementalPCA(n_components=2, batch_size=3)
title = 'Method: PCA'
run_dim_reduction_and_draw(X_t, y_t, model, title)


# #### t-SNE for tf-idf

# In[369]:

perplexity=30
learning_rate=1000.0

model = TSNE(n_components=4,
           random_state=0,
           perplexity=perplexity,
           learning_rate=learning_rate, n_iter=200)
title = 'Method: t-SNE, perplexity: {}, learning_rate: {}'.format(perplexity, learning_rate)
X_model = run_dim_reduction_and_draw(X_t, y_t, model, title)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



