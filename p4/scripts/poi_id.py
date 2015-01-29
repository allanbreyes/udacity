#!/usr/bin/python

from copy import copy
import matplotlib.pyplot as plt
import sys
import pickle
sys.path.append("../tools/")

from feature_format import featureFormat
from feature_format import targetFeatureSplit

import enron

# features_list is a list of strings, each of which is a feature name
# first feature must be "poi", as this will be singled out as the label
target_label = 'poi'
email_features_list = [
    # 'email_address', # remit email address; informational label
    'from_messages',
    'from_poi_to_this_person',
    'from_this_person_to_poi',
    'shared_receipt_with_poi',
    'to_messages',
    ]
financial_features_list = [
    'bonus',
    'deferral_payments',
    'deferred_income',
    'director_fees',
    'exercised_stock_options',
    'expenses',
    'loan_advances',
    'long_term_incentive',
    'other',
    'restricted_stock',
    'restricted_stock_deferred',
    'salary',
    'total_payments',
    'total_stock_value',
]
features_list = [target_label] + financial_features_list + email_features_list

# load the dictionary containing the dataset
data_dict = pickle.load(open("../data/final_project_dataset.pkl", "r") )

# remove outliers
outlier_keys = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
enron.remove_keys(data_dict, outlier_keys)

# instantiate copies of dataset and features for grading purposes
my_dataset = copy(data_dict)
my_feature_list = copy(features_list)

# add two new features
enron.add_financial_aggregate(my_dataset, my_feature_list)
enron.add_poi_interaction(my_dataset, my_feature_list)

# get K-best features
best_features = enron.get_k_best(my_dataset, my_feature_list, 10).keys()
my_feature_list = [target_label] + best_features

# extract the features specified in features_list
data = featureFormat(my_dataset, my_feature_list)

# split into labels and features (this line assumes that the first
# feature in the array is the label, which is why "poi" must always
# be first in the features list
labels, features = targetFeatureSplit(data)

# machine learning goes here!
# please name your classifier clf for easy export below

clf = None # get rid of this line!  just here to keep code from crashing out-of-box


# dump your classifier, dataset and features_list so
# anyone can run/check your results
pickle.dump(clf, open("../data/my_classifier.pkl", "w"))
pickle.dump(data_dict, open("../data/my_dataset.pkl", "w"))
pickle.dump(features_list, open("../data/my_feature_list.pkl", "w"))
