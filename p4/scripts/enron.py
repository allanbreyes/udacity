#!/usr/bin/python
import csv
import matplotlib.pyplot as plt
import pickle
import sys
sys.path.append("../tools/")

from feature_format import featureFormat
from feature_format import targetFeatureSplit

from sklearn.feature_selection import SelectKBest

def remove_keys(dict_object, keys):
    """ removes a list of keys from a dict object """
    for key in keys:
        dict_object.pop(key, 0)

def make_csv(data_dict):
    """ generates a csv file from a data set """
    fieldnames = ['name'] + data_dict.itervalues().next().keys()
    with open('data.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in data_dict:
            person = data_dict[record]
            person['name'] = record
            assert set(person.keys()) == set(fieldnames)
            writer.writerow(person)

def visualize(data_dict, feature_x, feature_y):
    """ generates a plot of feature y vs feature x, colors poi """

    data = featureFormat(data_dict, [feature_x, feature_y, 'poi'])

    for point in data:
        x = point[0]
        y = point[1]
        poi = point[2]
        color = 'red' if poi else 'blue'
        plt.scatter(x, y, color=color)
    plt.xlabel(feature_x)
    plt.ylabel(feature_y)
    plt.show()

def get_k_best(data_dict, features_list, k):
    """ runs scikit-learn's SelectKBest feature selection
        returns dict where keys=features, values=scores
    """
    data = featureFormat(data_dict, features_list)
    labels, features = targetFeatureSplit(data)

    k_best = SelectKBest(k=k)
    k_best.fit(features, labels)
    scores = k_best.scores_
    unsorted_pairs = zip(features_list[1:], scores)
    sorted_pairs = list(reversed(sorted(unsorted_pairs, key=lambda x: x[1])))
    k_best_features = dict(sorted_pairs[:k])
    print "{0} best features: {1}".format(k, k_best_features.keys())
    return k_best_features

if __name__ == '__main__':
    data_dict = pickle.load(open("../data/final_project_dataset.pkl", "r"))
    outliers = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
    remove_keys(data_dict, outliers)
    # make_csv(data_dict)
    # visualize(data_dict, 'salary', 'bonus')
    # visualize(data_dict, 'from_poi_to_this_person', 'from_this_person_to_poi')

    features_list = ['poi',
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
                     'from_messages',
                     'from_poi_to_this_person',
                     'from_this_person_to_poi',
                     'shared_receipt_with_poi',
                     'to_messages']