from collections import defaultdict
import csv
import os
import sys

maxInt = sys.maxsize

while True:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


def load_data(data_folder):
    nodes_path = os.path.join(data_folder, "nodes_neo4j.csv")
    edges_path = os.path.join(data_folder, "edges_neo4j.csv")
    group_by_semmantic_dict = defaultdict(list)
    id_type_mapping = {}
    with open(nodes_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for _item in csv_reader:
            group_by_semmantic_dict[_item[-2]].append(_item[-1])
            id_type_mapping[_item[-1]] = {'type': _item[-2], 'name': _item[1]}
    chemical_related = {}
    unique_assocs = set()
    with open(edges_path) as f:
        csv_reader = csv.reader(f, delimiter=',')
        next(csv_reader)
        for _item in csv_reader:
            if _item[4] in group_by_semmantic_dict['chemical_substance']:
                if _item[4] not in chemical_related:
                    chemical_related[_item[4]] = {'_id': _item[4][5:],
                                                  'umls': _item[4][5:],
                                                  'name': id_type_mapping[_item[4]]['name']}
                pred = _item[0].lower()
                semantic_type = id_type_mapping[_item[5]]['type']
                if pred not in chemical_related[_item[4]]:
                    chemical_related[_item[4]][pred] = {}
                if semantic_type not in chemical_related[_item[4]][pred]:
                    chemical_related[_item[4]][pred][semantic_type] = []
                assoc = _item[4] + pred + str(_item[1]) + _item[5]
                if assoc not in unique_assocs:
                    unique_assocs.add(assoc)
                    gene_related[_item[4]][pred][semantic_type].append({'pmid': _item[1].split(';'), 'umls': _item[5][5:]})
            elif _item[5] in group_by_semmantic_dict['chemical_substance']:
                if _item[5] not in chemical_related:
                    chemical_related[_item[5]] = {'_id': _item[5][5:],
                                                  'umls': _item[5][5:],
                                                  'name': id_type_mapping[_item[5]]['name']}
                pred = _item[0].lower() + '_reverse'
                semantic_type = id_type_mapping[_item[4]]['type']
                if pred not in chemical_related[_item[5]]:
                    chemical_related[_item[5]][pred] = {}
                if semantic_type not in chemical_related[_item[5]][pred]:
                    chemical_related[_item[5]][pred][semantic_type] = []
                assoc = _item[5] + pred + str(_item[1]) + _item[4]
                if assoc not in unique_assocs:
                    unique_assocs.add(assoc)
                    gene_related[_item[5]][pred][semantic_type].append({'pmid': _item[1].split(';'), 'umls': _item[4][5:]})
    for v in chemical_related.values():
        yield v
