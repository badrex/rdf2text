import os
import random
import re
import json
import sys
import getopt
from collections import defaultdict
from benchmark_reader import Benchmark

from SPARQLWrapper import SPARQLWrapper, JSON
import nltk
from nltk.tokenize import word_tokenize
import re

ONLINE = False

# pre-compile regexes for the CamelCase converting function
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

# each ontology class is given a "semantic precision" score (according to http://mappings.dbpedia.org/server/ontology/classes/)
with open('onto_classes_hierarchy.json', encoding="utf8") as f:
    onto_classes_hierarchy = json.load(f)

# dictionary which links an entity with its semantic type / ontology class (ex: Alan_Bean -> ASTRONAUT), used for the delexicalisation
if ONLINE:  # in this case we directly use results from sparql queries on dbpedia (and we build the dictionary)
    delex_dict_dbpd = dict()
else:
    with open('delex_dict_dbpd.json', encoding="utf8") as f:    # in this case we load the dict from a json file
        delex_dict_dbpd = json.load(f)



def CamelCase_to_regular(expr):
    s1 = first_cap_re.sub(r'\1 \2', expr)
    return all_cap_re.sub(r'\1 \2', s1).lower()


def select_files(topdir, category='', size=(1, 8)):
    """
    Collect all xml files from a benchmark directory.
    :param topdir: directory with benchmark
    :param category: specify DBPedia category to retrieve texts for a specific category (default: retrieve all)
    :param size: specify size to retrieve texts of specific size (default: retrieve all)
    :return: list of tuples (full path, filename)
    """
    finaldirs = [topdir+'/'+str(item)+'triples' for item in range(size[0], size[1])]
    finalfiles = []
    for item in finaldirs:
        finalfiles += [(item, filename) for filename in os.listdir(item)]
    if category:
        finalfiles = []
        for item in finaldirs:
            finalfiles += [(item, filename) for filename in os.listdir(item) if category in filename]
    return finalfiles


def dbpedia_ontology_query(entity):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?type
        WHERE { <http://dbpedia.org/resource/""" + entity + """> rdf:type ?type .}
    """)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        onto_classes = [x["type"]["value"][28:] for x in results["results"]["bindings"] if x["type"]["value"].startswith("http://dbpedia.org/ontology/")]   # we only consider the dbpedia:ontology results
        
        bestScore = 0
        bestType = "NOT_FOUND"
        for type in onto_classes:
            if type in onto_classes_hierarchy:
                if onto_classes_hierarchy[type] > bestScore:
                    bestType = type
                    bestScore = onto_classes_hierarchy[type]
        return bestType.upper() # the ontology class returned is the one with the highest 'semantic precision' score
        
    except Exception:
        return "INVALID_NAME"


def triple_delexicalisation(subj, prop, obj, rplc_dict, index):
    if subj not in delex_dict_dbpd:
        delex_dict_dbpd[subj] = dbpedia_ontology_query(subj)
        index += 1
    subj_delex = delex_dict_dbpd[subj]
    
    if not(obj[0].isalpha()):   # we avoid to search '25.0' or '"Bread, almonds, garlic, water, olive oil"' on dbpedia
        obj_delex = prop.upper()    # so we just take property to delexicalize the object
        index += 1
    else:
        if obj not in delex_dict_dbpd:
            delex_dict_dbpd[obj] = dbpedia_ontology_query(obj)
            index += 1
        obj_delex = delex_dict_dbpd[obj]
    
    rplc_dict[subj.replace('_', ' ')] = subj_delex
    rplc_dict[obj.replace('_', ' ').replace('"', '')] = obj_delex
    
    return subj_delex, obj_delex, index


def sentence_delexicalisation(sentence, rplc_dict):
    sentTokens = word_tokenize(sentence)
    sentTokensLow = [t.lower() for t in sentTokens]
    
    for entity in rplc_dict:
        entTokensLow = [t.lower() for t in word_tokenize(entity)]
        n = len(sentTokens)
        m = len(entTokensLow)
    
        i=0
        while (i < n - m):
            if entTokensLow == sentTokensLow[i:i+m]:
                sentTokensLow = sentTokensLow[:i]+['X']+sentTokensLow[i+m:]
                sentTokens = sentTokens[:i]+[rplc_dict[entity]]+sentTokens[i+m:]
                i = n - m
            i += 1
    
    sentence_delex = ' '.join(sentTokens)
    return sentence_delex


def delexicalisation(out_src, out_trg, category, properties_objects):
    """
    Perform delexicalisation.
    :param out_src: source string
    :param out_trg: target string
    :param category: DBPedia category
    :param properties_objects: dictionary mapping properties to objects
    :return: delexicalised strings of the source and target; dictionary containing mappings of the replacements made
    """
    with open('delex_dict.json', encoding="utf8") as data_file:
        data = json.load(data_file)
        
    # replace all occurrences of Alan_Bean to ASTRONAUT in input
    delex_subj = data[category]
    delex_src = out_src
    delex_trg = out_trg
    
    # for each instance, we save the mappings between nondelex and delex
    replcments = {}
    
    for subject in delex_subj:
        clean_subj = ' '.join(re.split('(\W)', subject.replace('_', ' ')))
        if clean_subj in out_src:
            delex_src = out_src.replace(clean_subj + ' ', category.upper() + ' ')
            replcments[category.upper()] = ' '.join(clean_subj.split())   # remove redundant spaces
        if clean_subj in out_trg:
            delex_trg = out_trg.replace(clean_subj + ' ', category.upper() + ' ')
            replcments[category.upper()] = ' '.join(clean_subj.split())

    # replace all occurrences of objects by PROPERTY in input
    for pro, obj in sorted(properties_objects.items()):
        obj_clean = ' '.join(re.split('(\W)', obj.replace('_', ' ').replace('"', '')))
        if obj_clean in delex_src:
            delex_src = delex_src.replace(obj_clean + ' ', pro.upper() + ' ')
            replcments[pro.upper()] = ' '.join(obj_clean.split())   # remove redundant spaces
        if obj_clean in delex_trg:
            delex_trg = delex_trg.replace(obj_clean + ' ', pro.upper() + ' ')
            replcments[pro.upper()] = ' '.join(obj_clean.split())

    # possible enhancement for delexicalisation:
    # do delex triple by triple
    # now building | location | New_York_City New_York_City | isPartOf | New_York
    # is converted to
    # BUILDING location ISPARTOF City ISPARTOF City isPartOf ISPARTOF
    return delex_src, delex_trg, replcments


def create_source_target(b, options, dataset, delex=True):
    """
    Write target and source files, and reference files for BLEU.
    :param b: instance of Benchmark class
    :param options: string "delex" or "notdelex" to label files
    :param dataset: dataset part: train, dev, test
    :param delex: boolean; perform delexicalisation or not
    :return: if delex True, return list of replacement dictionaries for each example
    """
    source_out = []
    target_out = []
    rplc_list = []  # store the dict of replacements for each example
    
    index = 0
    
    for entr in b.entries:
        tripleset = entr.modifiedtripleset
        lexics = entr.lexs
        category = entr.category
        
        triples = ''
        rplc_dict = dict()
        
        for triple in tripleset.triples:
            subj, prop, obj = triple.s, triple.p, triple.o
            if delex:
                subj, obj, index = triple_delexicalisation(subj, prop, obj, rplc_dict, index)
            else:
                subj = ' '.join(word_tokenize(subj.replace('_', ' ')))  # we must be careful with the writing convention, in particulary, punct signs have to be separated from the text
                obj = ' '.join(word_tokenize(obj.replace('_', ' ').replace('"', '')))
            prop = CamelCase_to_regular(prop)
            
            triples += subj + ' ' + prop + ' ' + obj + ' '
        
        for lex in lexics:
            if delex:
                sentence = sentence_delexicalisation(lex.lex, rplc_dict)
                rplc_list.append(rplc_dict)
            else:
                sentence = ' '.join(word_tokenize(lex.lex)) # separate punct signs from text
            
            source_out.append(triples)
            target_out.append(sentence)
#            triples = ''
#            properties_objects = {}    #tag0
            
#            for triple in tripleset.triples:
#                triples += triple.s + ' ' + triple.p + ' ' + triple.o + ' '
#                properties_objects[triple.p] = triple.o    #tag0
            
#            triples = triples.replace('_', ' ').replace('"', '')
            
            # separate punct signs from text
#            out_src = ' '.join(re.split('(\W)', triples))
#            out_trg = ' '.join(re.split('(\W)', lex.lex))
            
#            if delex:  #tag0
#                out_src, out_trg, rplc_dict = delexicalisation(out_src, out_trg, category, properties_objects)
#                rplc_list.append(rplc_dict)

            # delete white spaces
#            source_out.append(' '.join(out_src.split()))
#            target_out.append(' '.join(out_trg.split()))

    # shuffle two lists in the same way
    random.seed(10)
    
    if delex:
        corpus = list(zip(source_out, target_out, rplc_list))
        random.shuffle(corpus)
        source_out, target_out, rplc_list = zip(*corpus)
    else:
        corpus = list(zip(source_out, target_out))
        random.shuffle(corpus)
        source_out, target_out = zip(*corpus)

    with open(dataset + '-webnlg-' + options + '.triple', 'w+', encoding="utf8") as f:
        f.write('\n'.join(source_out))
    with open(dataset + '-webnlg-' + options + '.lex', 'w+', encoding="utf8") as f:
        f.write('\n'.join(target_out))
    
    # create separate files with references for multi-bleu.pl for dev set
    scr_refs = defaultdict(list)
    if dataset == 'dev' and not delex:
        for src, trg in zip(source_out, target_out):
            scr_refs[src].append(trg)
        # length of the value with max elements
        max_refs = sorted(scr_refs.values(), key=len)[-1]
        keys = [key for (key, value) in sorted(scr_refs.items())]
        values = [value for (key, value) in sorted(scr_refs.items())]
        # write the source file not delex
        with open(options + '-source.triple', 'w+', encoding="utf8") as f:
            f.write('\n'.join(keys))
        # write references files
        for j in range(0, len(max_refs)):
            with open(options + '-reference' + str(j) + '.lex', 'w+', encoding="utf8") as f:
                out = ''
                for ref in values:
                    try:
                        out += ref[j] + '\n'
                    except:
                        out += '\n'
                f.write(out)

    return rplc_list


def relexicalise(predfile, rplc_list):
    """
    Take a file from seq2seq output and write a relexicalised version of it.
    :param rplc_list: list of dictionaries of replacements for each example (UPPER:not delex item)
    :return: list of predicted sentences
    """
    relex_predictions = []
    with open(predfile, 'r', encoding="utf8") as f:
        predictions = [line for line in f]
    for i, pred in enumerate(predictions):
        # replace each item in the corresponding example
        rplc_dict = rplc_list[i]
        relex_pred = pred
        for key in rplc_dict:
            relex_pred = relex_pred.replace(rplc_dict[key], key)
        relex_predictions.append(relex_pred)
    # with open('relexicalised_predictions_full.txt', 'w+') as f:
        # f.write(''.join(relex_predictions))

    # create a mapping between not delex triples and relexicalised sents
    with open('dev-webnlg-all-notdelex.triple', 'r', encoding="utf8") as f:
        dev_sources = [line.strip() for line in f]
    src_gens = {}
    for src, gen in zip(dev_sources, relex_predictions):
        src_gens[src] = gen  # need only one lex, because they are the same for a given triple

    # write generated sents to a file in the same order as triples are written in the source file
    with open('all-notdelex-source.triple', 'r', encoding="utf8") as f:
        triples = [line.strip() for line in f]
    with open('relexicalised_predictions.txt', 'w+', encoding="utf8") as f:
        for triple in triples:
            f.write(src_gens[triple])

    return relex_predictions


def input_files(path, filepath=None, relex=False):
    """
    Read the corpus, write train and dev files.
    :param path: directory with the WebNLG benchmark
    :param filepath: path to the prediction file with sentences (for relexicalisation)
    :param relex: boolean; do relexicalisation or not
    :return:
    """
    parts = ['train', 'dev']
    options = ['all-delex', 'all-notdelex']  # generate files with/without delexicalisation
    for part in parts:
        for option in options:
            files = select_files(path + part, size=(1, 8))
            b = Benchmark()
            b.fill_benchmark(files)
            if option == 'all-delex':
                rplc_list = create_source_target(b, option, part, delex=True)
                print('Total of {} files processed in {} with {} mode'.format(len(files), part, option))
            elif option == 'all-notdelex':
                rplc_list = create_source_target(b, option, part, delex=False)
                print('Total of {} files processed in {} with {} mode'.format(len(files), part, option))
            if relex and part == 'dev' and option == 'all-delex':
                relexicalise(filepath, rplc_list)
    
    if ONLINE:
        with open('delex_dict_dbpd.json', 'w') as f:
            json.dump(delex_dict_dbpd, f)
    
    print('Files necessary for training/evaluating are written on disc.')


def main(argv):
    usage = 'usage:\npython3 webnlg_baseline_input.py -i <data-directory>' \
           '\ndata-directory is the directory where you unzipped the archive with data'
    try:
        opts, args = getopt.getopt(argv, 'i:', ['inputdir='])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    input_data = False
    for opt, arg in opts:
        if opt in ('-i', '--inputdir'):
            inputdir = arg
            input_data = True
        else:
            print(usage)
            sys.exit()
    if not input_data:
        print(usage)
        sys.exit(2)
    print('Input directory is ', inputdir)
    input_files(inputdir)


if __name__ == "__main__":
    main(sys.argv[1:])
