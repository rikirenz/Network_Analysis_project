# -*- coding: utf-8 -*-
# This set of functions given a monomodal matrix in a single column file
# is able to plot the  graph that represents the number of occurrences for
# each value present in the matrix excepts the 0 value.

import json, sys, types, unicodedata, requests

core_set_alma_mater_professor = []


def _prof_has_less_then_2_collaborations_with_core_set(prof):
    counter = 0
    data = _query_author_papers(prof)
    try:
        if 'hit' in data['result']['hits']:
            for i in data['result']['hits']['hit']:
                authors = i['info']['authors']['author']
                if isinstance(authors, types.StringTypes):
                    if authors in core_set_alma_mater_professor:
                        counter += 1
                else:
                    for j in authors:
                        if j in a:
                            counter += 1

                if counter >= 2:
                    break
    except Exception:
        pass

    return counter < 2


def _query_author_papers(prof):
    try:
        url = 'http://dblp.uni-trier.de/search/publ/api'
        params = dict(q=prof, h='1000', format='json')
        resp = requests.get(url=url, params=params)
        decoded_response = unicodedata.normalize('NFKD', resp.text).encode('ascii', 'ignore')
        return json.loads(decoded_response)
    except Exception:
        print('author error:' + prof)


def _increment_collaboration(prof_collaborations, list_all_professors, author, current_prof):
    """author: the author that we have used to interrogate the database
        current_prof: the coauthor that we are analysing """
    if current_prof not in list_all_professors:
        return

    if sorted(current_prof.split(' ', 1)) == sorted(author.split(' ', 1)):
        return

    if author in prof_collaborations:
        prof_collaborations[author] += 1
    else:
        prof_collaborations[author] = 1


def _increment_professor_list(professors_list, prof):
    for professor in professors_list:
        if sorted(professor.split(' ', 1)) == sorted(prof.split(' ', 1)):
            return

    if _prof_has_less_then_2_collaborations_with_core_set(prof):
        return
    import pdb; pdb.set_trace()
    professors_list.append(prof)


def _print_list(file_name, list):
    out_file = open(file_name, 'w')
    out_file.write('","'.join(list))
    out_file.close()


def _print_json(file_name, json_obj):
    out_file = open(file_name, 'w')
    json.dump(json_obj, out_file)
    out_file.close()


def _select_authors():
    # site
    authors = core_set_alma_mater_professor
    professors_list = core_set_alma_mater_professor
    for prof in authors:
        print('-------\n' + prof + '\n-------')
        _increment_professor_list(professors_list, prof)
        data = _query_author_papers(prof)
        try:
            if 'hit' in data['result']['hits']:
                for i in data['result']['hits']['hit']:
                    collaborators = i['info']['authors']['author']
                    if isinstance(authors, types.StringTypes):
                        _increment_professor_list(professors_list, collaborators)
                    else:
                        for j in collaborators:
                            _increment_professor_list(professors_list, j)
        except Exception:
            import ipdb; ipdb.set_trace()
        print('-------\n' + ', '.join(professors_list) + '\n-------')
    _print_list('data/authors_general_list.out', professors_list)


def _count_collaborations(output_file_name):
        # site
        inFile = 'data/authors_general_list.json'
        with open(inFile) as data_file:
            authors = json.load(data_file)

        collaborations = {}
        for prof in authors['authors']:
            collaborations[prof] = {}
            data = _query_author_papers(prof)
            try:
                if 'hit' in data['result']['hits']:
                    for i in data['result']['hits']['hit']:
                        if 'authors' in i['info'] and 'author' in i['info']['authors']:
                            coauthors = i['info']['authors']['author']
                            if isinstance(coauthors, types.StringTypes):
                                _increment_collaboration(collaborations[prof], authors['authors'], coauthors, prof)
                            else:
                                for j in coauthors:
                                    _increment_collaboration(collaborations[prof], authors['authors'], j, prof)
            except Exception:
                import pdb; pdb.set_trace()
        _print_json(output_file_name, collaborations)


def _produce_monomodal_matrix(input_file_name):

    def _check_if_collaborator_in_occurences(collaborator, professors):
        for professor in professors:
            if sorted(collaborator.split(' ', 1)) == sorted(professor.split(' ', 1)):
                return professor
        return ''

    inFile = 'data/authors_general_list.json'
    # inFile = 'data/dummy_authors.json'
    with open(inFile) as data_file:
        authors = json.load(data_file)

    with open(input_file_name) as data_file:
        occurences = json.load(data_file)

    out_file = open("excel_matrix.dat","w")

    i = 0
    for prof in authors['authors']:
        out_file.write(prof + '|')
        i += 1
        print(i)
        for collaborator in authors['authors']:
            if sorted(collaborator.split(' ', 1)) != sorted(prof.split(' ', 1)):
                collaborator_name = _check_if_collaborator_in_occurences(collaborator, occurences[prof])
                if collaborator_name:
                    out_file.write(str(occurences[prof][collaborator_name]) + '|')
                else:
                    out_file.write('0|')
            else:
                out_file.write('0|')
        out_file.write('\n')
    out_file.close()

# _select_authors() -> this functions should be changed 
# in order to collect only coauthors that have at least 2 
# collaborations with 2 different professor core set of the department

# this should lead to a smaller final professors set!
with open('data/authors_unibo.json') as data_file:
    core_set_alma_mater_professor = json.load(data_file)['authors']
_select_authors()
output_file_name = 'data/general_matrix.json'
_count_collaborations(output_file_name)
print('check the file ' + output_file_name)
_produce_monomodal_matrix('data/general_matrix.json')


