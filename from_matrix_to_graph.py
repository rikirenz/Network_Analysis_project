# -*- coding: utf-8 -*-
# This set of functions given a monomodal matrix in a single column file
# is able to plot the  graph that represents the number of occurrences for
# each value present in the matrix excepts the 0 value.

from chart import print_chart
import operator
import json


def _sort_dictionary(unsorted_dict):
    sorted_list = sorted(unsorted_dict.items(), key=operator.itemgetter(0))
    keys = []
    counter = []
    for item in sorted_list:
        keys.append(item[0])
        counter.append(item[1])

    return keys, counter


def _convert_file_to_json(file):
    """ Given a file where each line is composed by one number. It
    returns the list where each line is a list value """
    json1_file = open(file, 'r')
    json1_str = json1_file.read()
    json1_data = json.loads(json1_str)
    return json1_data


def _occurrences_counter(dict_matrix):
    """ Given a list where each value represents an entry in a monomodal
    matrix. It returns the number of occurrences for the given matrix.
    It does not count the 0 occurrences"""
    counter = {}
    matrix_list_without_0 = _remove_zero_from_monomodal_matrix(dict_matrix)
    for value in matrix_list_without_0:
        try:
            counter[value] += 1
        except Exception:
            counter[value] = 1

    sorted_dictionary = _sort_dictionary(counter)
    return sorted_dictionary


def _remove_zero_from_monomodal_matrix(dict_matrix):
    """Given a list where each line represents an entry in a monomodal
    matrix. It returns a list without 0. """
    final_list = []
    for entry in dict_matrix:
        for value in dict_matrix[entry]:
            com = dict_matrix[entry][value]
            if com:
                final_list.append(com)
    return final_list


dict_matrix = _convert_file_to_json('data/general_matrix_backup.json')
occurrences = _occurrences_counter(dict_matrix)
# X -> number_of_collaborations; Y -> occurrences
print_chart(number_of_collaborations=occurrences[0], occurrences=occurrences[1])
