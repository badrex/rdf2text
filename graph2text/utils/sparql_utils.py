from SPARQLWrapper import SPARQLWrapper, JSON

def dbpedia_query(query_string, resource = False):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    
    if resource:    # we query dbpedia about a resource/entity (subject or object of a triple)
        try:
            results = sparql.query().convert()
            onto_classes = [x["x"]["value"][28:] for x in results["results"]["bindings"] if x["x"]["value"].startswith("http://dbpedia.org/ontology/")]   # we only consider the dbpedia:ontology results
            if len(onto_classes) == 0:
                return "NOT_FOUND"
            return onto_classes[0].upper() # the ontology class returned is the first result (arbitrary, to be changed)
            
        except Exception:
            return "INVALID_NAME"
    
    else:   # we query dbpedia about an ontology (property of a triple)
        try:
            results = sparql.query().convert()
            if len(results["results"]["bindings"]) == 0:
                return "NOT_FOUND"
            else:
                return results["results"]["bindings"][0]["x"]["value"][28:].upper() # there should be exactly one result
            
        except Exception:
            return "INVALID_NAME"

def get_property_range(property):
    query_string = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?x
        WHERE { <http://dbpedia.org/ontology/""" + property + """> rdfs:range ?x .}
    """
    
    return dbpedia_query(query_string)

def get_property_domain(property):
    query_string = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?x
        WHERE { <http://dbpedia.org/ontology/""" + property + """> rdfs:domain ?x .}
    """
    
    return dbpedia_query(query_string)

def get_resource_type(resource):
    query_string = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?x
        WHERE { <http://dbpedia.org/resource/""" + resource + """> rdf:type ?x .}
    """
    
    return dbpedia_query(query_string, resource = True)