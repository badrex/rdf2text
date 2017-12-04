"""
For each property in the dataset, get its domain and range.
"""

from collections import defaultdict

#from NLG import graph2text
from graph2text import utils


import utils

with open('metadata/properties.list', encoding="utf8") as f:
    rdf_prop_list = [prop.strip() for prop in f.readlines()]

prop_schema = []

for prop in rdf_prop_list:
    prop_domain = sparql_utils.get_property_domain(prop)
    prop_range = sparql_utils.get_property_range(prop)

    prop_schema.append((prop, domain, range))

for (p, d, r) in prop_schema:
    print(p, d, r)
