import json
import xml.etree.ElementTree as ET

threshold = 1000

with open('metadata/ontology_ponderated_occurences.json', encoding="utf8") as f:
    ontology_ponderated_occurences = json.load(f)

system = dict()
genealogy = 10*[""]

def walker(elem, level):
    valid_relative = genealogy[level//2-1]
    try:
        text = elem.text
        if (text[0].isalpha()) & (text != "edit"):
            if text.upper() in ontology_ponderated_occurences:
                occurences = ontology_ponderated_occurences[text.upper()]
            else:
                occurences = 0
            if occurences > threshold or valid_relative == "":
                valid_relative = text
            system[text] = (level//2, valid_relative)
            genealogy[level//2] = valid_relative
            print('-'*level+'o '+text+'     * '+valid_relative)
    except Exception:
        pass

    for child in elem.getchildren():
        walker(child, level+1)

root = ET.parse('metadata/OntologyClasses.xml')
walker(root.getroot(), 0)

with open('metadata/onto_classes_system.json', 'w') as f:
    json.dump(system, f, ensure_ascii=False, indent=3, sort_keys=True)
