#!/usr/bin/python
import matplotlib.pyplot as plt
import sys
import pickle
import csv
sys.path.append("../tools/")

from feature_format import featureFormat
from feature_format import targetFeatureSplit

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

if __name__ == '__main__':
    data_dict = pickle.load(open("final_project_dataset.pkl", "r"))
    outliers = ['TOTAL', 'THE TRAVEL AGENCY IN THE PARK', 'LOCKHART EUGENE E']
    remove_keys(data_dict, outliers)
    #make_csv(data_dict)
    # visualize(data_dict, 'salary', 'bonus')
    visualize(data_dict, 'from_poi_to_this_person', 'from_this_person_to_poi')
