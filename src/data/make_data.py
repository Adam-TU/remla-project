from ast import literal_eval
import pandas as pd

"""
In this task you will deal with a dataset of post titles from StackOverflow. 
You are provided a split to 3 sets: train, validation and test. All corpora (except for test) contain titles of the posts and 
corresponding tags (100 tags are available). The test set doesn’t contain answers.
"""


def _read_data(filename):
    """
    filename: Input filename

    :return: pandas dataframe of the file
    """
    data = pd.read_csv(filename, sep='\t')
    data['tags'] = data['tags'].apply(literal_eval)
    return data


def _split_data():
    """
    :return: Dataframe split into train, validation and test set.
    """
    train = _read_data('../../data/raw/train.tsv')
    validation = _read_data('../../data/raw/validation.tsv')
    test = pd.read_csv('../../data/raw/test.tsv', sep='\t')
    return train, validation, test


def init_data():
    """
    :return: For a more comfortable usage, returns an initialized X_train, X_val, X_test, y_train, y_val.
    """
    train, validation, test = _split_data()
    X_train, y_train = train['title'].values, train['tags'].values
    X_val, y_val = validation['title'].values, validation['tags'].values
    X_test = test['title'].values
    return X_train, X_val, X_test, y_train, y_val
