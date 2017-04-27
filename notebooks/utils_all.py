# coding: utf-8

# In[16]:

import warnings
warnings.filterwarnings('ignore')


# In[17]:

from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder

import pandas as pd
import numpy as np

# In[18]:

import matplotlib.pyplot as plt


# In[19]:

def clean_df(df):
    new_df = df.drop_duplicates(subset=['meta_name','x_coords','y_coords', 'block_height', 'block_width'])
    new_df = new_df[new_df['tag'] != 'meta']
    new_df = new_df[new_df['x_coords'] != 0]
    new_df = new_df[new_df['block_height'] != 0]
    new_df = new_df[new_df['block_width'] != 0]
    new_df.url = new_df.url.apply(lambda x: x.replace('\n',''))
    return new_df


# In[20]:

def get_XY(field, no_field, no_column_name):
    no_field_smpl = no_field.sample(n = field.shape[0], random_state=7)
    real_train_meta_name = no_field_smpl.meta_name 
    no_field_smpl = no_field_smpl.drop('meta_name', 1)
    no_field_smpl.insert(1, 'meta_name', no_column_name)
    X_field = pd.concat((field, no_field_smpl), axis=0)
    y_field = X_field['meta_name']
    X_field = X_field.drop('meta_name', 1)
    X_field = X_field.replace('none', 'NA')
    le = LabelEncoder()
    le_tag = le.fit_transform(X_field.tag.values)
    X_field.loc[:,'tag'] = le_tag
    return X_field, y_field, real_train_meta_name, le


# In[21]:

def draw_feature_importance(clf_forest, X_train, field_name):
    importances = clf_forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in clf_forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]

    # Print the feature ranking
    print("Feature ranking:")

    for f in range(X_train.shape[1]):
        print("%d. feature '%s' (%f)" % (indices[f], X_train.columns[indices[f]], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances for {}".format(field_name))
    plt.bar(range(X_train.shape[1]), importances[indices],
           color="r", yerr=std[indices], align="center")
    plt.xticks(range(X_train.shape[1]), indices)
    plt.xlim([-1, X_train.shape[1]])
    plt.show()


# In[22]:

def perform_analysis_of_field(field_name, clf, data, clean=False):
    # choose field and no_field for negative examples and clean
    df_pos = clean_df(data[data['meta_name'] == field_name])
    df_neg = clean_df(data[data['meta_name'] != field_name])
    X, y, real_meta, tag_le = get_XY(df_pos, df_neg, 'no_' + field_name)
    X = X[['x_coords','y_coords','block_height','block_width','num_siblings']]
    X['y'] = y
    X = X.convert_objects(convert_numeric=True).dropna()
    y = X['y']
    X = X.drop('y', 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=7)
    clf.fit(X_train, y_train)
    print("train: {}, test: {}".format(clf.score(X_train, y_train), clf.score(X_test, y_test)))
    draw_feature_importance(clf, X_train, field_name)

def perform_analysis_tsne(field_name, clf, data):
    # choose field and no_field for negative examples and clean
    df_pos = data[data['label'] == field_name]
    df_neg = data[data['label'] != field_name]
    X, y, real_meta, tag_le = get_XY(df_pos, df_neg, 'no_' + field_name)
    X['y'] = y
    X = X.convert_objects(convert_numeric=True).dropna()
    y = X['y']
    X = X.drop('y', 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=7)
    clf.fit(X_train, y_train)
    print("train: {}, test: {}".format(clf.score(X_train, y_train), clf.score(X_test, y_test)))
    draw_feature_importance(clf, X_train, field_name)

    
def perform_analysis_of_field2(field_name, clf, data, clean=False):
    # choose field and no_field for negative examples and clean
    df_pos = clean_df(data[data['meta_name'] == field_name])
    df_neg = clean_df(data[data['meta_name'] != field_name])
    X, y, real_meta, tag_le = get_XY(df_pos, df_neg, 'no_' + field_name)
    X = X[['x_coords','y_coords','block_height','block_width',
           'num_siblings', 'num_punctuation', 'num_digits',
          'digits_share', 'num_upper', 'num_upper']]
    X['y'] = y
    X = X.convert_objects(convert_numeric=True).dropna()
    y = X['y']
    X = X.drop('y', 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=7)
    clf.fit(X_train, y_train)
    print("train: {}, test: {}".format(clf.score(X_train, y_train), clf.score(X_test, y_test)))
    draw_feature_importance(clf, X_train, field_name)
# In[ ]:




# In[ ]: