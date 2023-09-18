#!/usr/bin/env python3
#
# Description: POST service for exploration of
# data of Lung Cancer in the iASiS KG.
#

import sys
import os
from flask import Flask, abort, request, make_response
import json
from SPARQLWrapper import SPARQLWrapper, JSON
import logging
from urllib.parse import unquote,quote
import ast
import re

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


LIMIT=10

KG = os.environ["ENDPOINT"]
#KG="http://node2.research.tib.eu:8893/sparql"



app = Flask(__name__)



############################
#
# Query constants
#
############################

QUERY_PUBLICATIONS_RANKED_1 ="""
SELECT DISTINCT ?id  ?score ?title ?journal  ?year ?type  ?hindex  ?authors ?sjrstr ?cui ?cite
WHERE{
{SELECT DISTINCT ?id SUM(distinct xsd:float(?c)) as ?score MIN(?a) as ?cui (GROUP_CONCAT(DISTINCT ?author; separator=";") as ?authors)
WHERE {
?o <http://research.tib.eu/p4-lucat/vocab/annotates>  ?s.
                            ?o <http://research.tib.eu/p4-lucat/vocab/hasCUIAnnotation> ?a.
"""


QUERY_PUBLICATIONS_RANKED_2 ="""
?o <http://research.tib.eu/p4-lucat/vocab/confidence>  ?c.
                            ?o a <http://research.tib.eu/p4-lucat/vocab/HAS_TOPIC> .   
                            ?s <http://purl.org/ontology/bibo/pmid> ?id.
						    ?s <http://purl.org/dc/terms/creator> ?author.
                            ?s <http://research.tib.eu/p4-lucat/vocab/journal> ?journal.
                            ?s <http://research.tib.eu/p4-lucat/vocab/hasPublicationType> ?p_type.

"""


QUERY_PUBLICATIONS_RANKED_2_LC ="""
?o <http://research.tib.eu/p4-lucat/vocab/confidence>  ?c.
                            ?o a <http://research.tib.eu/p4-lucat/vocab/HAS_TOPIC> .   
                            ?s <http://purl.org/ontology/bibo/pmid> ?id.
                            ?s <http://research.tib.eu/p4-lucat/vocab/publication_isRelatedTo_Disease> <http://research.tib.eu/p4-lucat/entity/LungCancer>.
			    ?s <http://purl.org/dc/terms/creator> ?author.
                            ?s <http://research.tib.eu/p4-lucat/vocab/journal> ?journal.
                            ?s <http://research.tib.eu/p4-lucat/vocab/hasPublicationType> ?p_type.

"""


QUERY_PUBLICATIONS_RANKED_2_AD ="""
?o <http://research.tib.eu/p4-lucat/vocab/confidence>  ?c.
                            ?o a <http://research.tib.eu/p4-lucat/vocab/HAS_TOPIC> .   
                            ?s <http://purl.org/ontology/bibo/pmid> ?id.
                            ?s <http://research.tib.eu/p4-lucat/vocab/publication_isRelatedTo_Disease> <http://research.tib.eu/p4-lucat/entity/Alzheimer>.
						    ?s <http://purl.org/dc/terms/creator> ?author.
                            ?s <http://research.tib.eu/p4-lucat/vocab/journal> ?journal.
                            ?s <http://research.tib.eu/p4-lucat/vocab/hasPublicationType> ?p_type.

"""


QUERY_PUBLICATIONS_RANKED_3="""
} GROUP BY ?id}
?s <http://purl.org/ontology/bibo/pmid> ?id.
?s <http://research.tib.eu/p4-lucat/vocab/publicationType> ?type.
?s <http://research.tib.eu/p4-lucat/vocab/rankingScore_hIndex> ?hindex.
?s <http://purl.org/dc/terms/title> ?title.  
?s <http://research.tib.eu/p4-lucat/vocab/journal> ?journal.
?s <http://research.tib.eu/p4-lucat/vocab/year> ?year.
?s <http://research.tib.eu/p4-lucat/vocab/citedBy> ?cite.
?s <http://research.tib.eu/p4-lucat/vocab/rankingScore_SJR> ?sjr.
BIND (xsd:string(?sjr) as ?sjrstr)
} """


QUERY_PUBLICATIONS_RANKED_NUMBER_RESULTS="""
SELECT DISTINCT COUNT(DISTINCT  ?id) as ?number
WHERE {
?o a <http://research.tib.eu/p4-lucat/vocab/HAS_TOPIC> .  
?o <http://research.tib.eu/p4-lucat/vocab/annotates>  ?s.
?o <http://research.tib.eu/p4-lucat/vocab/hasCUIAnnotation> ?a.
?s <http://purl.org/ontology/bibo/pmid> ?id.
?s <http://research.tib.eu/p4-lucat/vocab/journal> ?journal.
?s <http://research.tib.eu/p4-lucat/vocab/hasPublicationType> ?p_type.
?s <http://purl.org/dc/terms/creator> ?author.
"""

QUERY_PUBLICATIONS_JOURNALS="""
SELECT DISTINCT ?journal AS ?name COUNT(DISTINCT ?id) AS ?results
WHERE {
?o a <http://research.tib.eu/p4-lucat/vocab/HAS_TOPIC> .  
?o <http://research.tib.eu/p4-lucat/vocab/annotates>  ?s.
?o <http://research.tib.eu/p4-lucat/vocab/hasCUIAnnotation> ?a.
?s <http://purl.org/ontology/bibo/pmid> ?id.
?s <http://research.tib.eu/p4-lucat/vocab/journal> ?journal.

"""

QUERY_PUBLICATIONS_TYPES ="""
SELECT DISTINCT MIN(?name) AS ?name COUNT(DISTINCT ?id) AS ?results
WHERE {
?o a <http://research.tib.eu/p4-lucat/vocab/HAS_TOPIC> .  
?o <http://research.tib.eu/p4-lucat/vocab/annotates>  ?s.
?o <http://research.tib.eu/p4-lucat/vocab/hasCUIAnnotation> ?a.
?s <http://purl.org/ontology/bibo/pmid> ?id.
?s <http://research.tib.eu/p4-lucat/vocab/hasPublicationType> ?p_type.
?p_type <http://research.tib.eu/p4-lucat/vocab/publicationTypeName> ?name.
                     
"""

QUERY_PUBLICATIONS_AUTHORS ="""
SELECT DISTINCT MIN(?name) AS ?name COUNT(DISTINCT ?id) AS ?results
WHERE {
?o a <http://research.tib.eu/p4-lucat/vocab/HAS_TOPIC> .  
?o <http://research.tib.eu/p4-lucat/vocab/annotates>  ?s.
?o <http://research.tib.eu/p4-lucat/vocab/hasCUIAnnotation> ?a.
?s <http://purl.org/ontology/bibo/pmid> ?id.
?s <http://purl.org/dc/terms/creator> ?name.

"""

############################
#
# Query generation
#
############################


def execute_query(query):
    #print(query)
    sparql_ins = SPARQLWrapper(KG)
    sparql_ins.setQuery(query)
    sparql_ins.setReturnFormat(JSON)
    return sparql_ins.query().convert()['results']['bindings']

def build_query_with_cuis(cuis, limit , page , sort, filters,query1,query2,query3,group,do_sort=True,topic=0):
   
    ######################################
    query1+="FILTER(?a in ("
    for cui in cuis:
        query1+="<http://research.tib.eu/p4-lucat/entity/"+cui+">,"
    query1=query1[:-1]
    query1+="))"
    ######################################
    if len(filters["journals"]) >0:
        query2+="FILTER ("
        for journal in filters["journals"]:
            query2+='?journal="'+journal+'" || '
        query2=query2[:-3]
        query2+=")"
    ##########################################
    if len(filters["publication_types"]) > 0:
        query2 += "FILTER (?p_type in ("
        for p_type in filters["publication_types"]:
            p_type_encoded = quote(p_type.strip(), safe='')
            query2 += "<http://research.tib.eu/p4-lucat/entity/" + p_type_encoded + ">,"
        query2 = query2[:-1]
        query2 += "))"

    ##########################################

    ##########################################
    if len(filters["authors"]) > 0:
        query2 += "FILTER (?author in ("
        for author in filters["authors"]:
            # Encoding the author string using UTF-8
            author_encoded_utf8 = author.encode('utf-8').decode('latin-1')

            # URL encoding the UTF-8 encoded author string
            author_encoded = quote(author_encoded_utf8, safe='')
            query2 += "<http://research.tib.eu/p4-lucat/entity/" + author_encoded + ">,"
        query2 = query2[:-1]
        query2 += "))"

    ##########################################
    '''if len(filters["affiliations"]) >0:
        query+="FILTER ("
        for aff in filters["affiliations"]:
            query+='contains(?affiliation,"'+aff+'") || '
        query=query[:-3]
        query+=")"'''
    ##########################################   
    if sort==0 or sort=="year":
        query3+=" ORDER BY DESC(?year) DESC (?score)"
    elif sort=="sjr":
        query3+=" ORDER BY DESC(?sjr)"
    elif sort=="hindex":
        query3+=" ORDER BY DESC(?hindex)"
    elif sort=="citation":
        query3+=" ORDER BY DESC(?cite)"

        
    return query1+query2+query3+" LIMIT "+str(limit)+" OFFSET "+str(page*limit)
    


############################
#
# Processing results
#
############################


def get_publications_ranked_data(cuis, limit , page , sort, filters,topic):
    query1=QUERY_PUBLICATIONS_RANKED_1
    if topic=="lc":
        query2=QUERY_PUBLICATIONS_RANKED_2_LC
    elif topic=="ad":
        query2=QUERY_PUBLICATIONS_RANKED_2_AD
    else:
        query2=QUERY_PUBLICATIONS_RANKED_2
    query3=QUERY_PUBLICATIONS_RANKED_3
    query = build_query_with_cuis(cuis,limit,page,sort,filters,query1,query2,query3,"pubs",True,topic)
    #print (query)
    qresults = execute_query(query)
    #print(qresults)
    return qresults




def process_journal_type_string(journal_type):
    # Use a temporary replacement for the single quote
    journal_type = journal_type.replace("\\'", "<TEMP_QUOTE>")

    # Remove unwanted characters
    journal_type = journal_type.replace("[", "").replace("]", "").replace("'", "")

    # Replace temporary string back to a single quote
    journal_type = journal_type.replace("<TEMP_QUOTE>", "'")
    return journal_type





def get_number_of_results(cuis,filters,topic):
    query=QUERY_PUBLICATIONS_RANKED_NUMBER_RESULTS
    if topic=="lc":
        query+="?s <http://research.tib.eu/p4-lucat/vocab/publication_isRelatedTo_Disease> <http://research.tib.eu/p4-lucat/entity/LungCancer>."
    elif topic=="ad":
        query+="?s <http://research.tib.eu/p4-lucat/vocab/publication_isRelatedTo_Disease> <http://research.tib.eu/p4-lucat/entity/Alzheimer>."

        
    query+="FILTER(?a in ("
    for cui in cuis:
        query+="<http://research.tib.eu/p4-lucat/entity/"+cui+">,"
    query=query[:-1]
    query+="))"
    ######################################
    if len(filters["journals"]) >0:
        query+="FILTER ("
        for journal in filters["journals"]:
            query+='?journal="'+journal+'" || '
        query=query[:-3]
        query+=")"
    ##########################################       
    if len(filters["publication_types"]) > 0:
        query += "FILTER (?p_type in ("
        for p_type in filters["publication_types"]:
            p_type_encoded = quote(p_type.strip(), safe='')
            query += "<http://research.tib.eu/p4-lucat/entity/" + p_type_encoded + ">,"
        query = query[:-1]
        query += "))"

    if len(filters["authors"]) > 0:
        query += "FILTER (?author in ("
        for author in filters["authors"]:
            # Encoding the author string using UTF-8
            author_encoded_utf8 = author.encode('utf-8').decode('latin-1')

            # URL encoding the UTF-8 encoded author string
            author_encoded = quote(author_encoded_utf8, safe='')
            query += "<http://research.tib.eu/p4-lucat/entity/" + author_encoded + ">,"
        query = query[:-1]
        query += "))"
    query+="}"
    #print(query)
    qresults = execute_query(query)
    return qresults[0]["number"]["value"]


def get_publications_filters_journals(cuis,topic):
    query=QUERY_PUBLICATIONS_JOURNALS
    if topic=="lc":
        query+="?s <http://research.tib.eu/p4-lucat/vocab/publication_isRelatedTo_Disease> <http://research.tib.eu/p4-lucat/entity/LungCancer>."
    elif topic=="ad":
        query+="?s <http://research.tib.eu/p4-lucat/vocab/publication_isRelatedTo_Disease> <http://research.tib.eu/p4-lucat/entity/Alzheimer>."

        
    query+="FILTER(?a in ("
    for cui in cuis:
        query+="<http://research.tib.eu/p4-lucat/entity/"+cui+">,"
    query=query[:-1]
    query+="))} GROUP BY ?journal"
    #print(query)
    qresults = execute_query(query)
    return [{"name":x["name"]["value"] , "results":x["results"]["value"]} for x in qresults]

def get_publications_filters_types(cuis,topic):
    query=QUERY_PUBLICATIONS_TYPES
    if topic=="lc":
        query+="?s <http://research.tib.eu/p4-lucat/vocab/publication_isRelatedTo_Disease> <http://research.tib.eu/p4-lucat/entity/LungCancer>."
    elif topic=="ad":
        query+="?s <http://research.tib.eu/p4-lucat/vocab/publication_isRelatedTo_Disease> <http://research.tib.eu/p4-lucat/entity/Alzheimer>."

        
    query+="FILTER(?a in ("
    for cui in cuis:
        query+="<http://research.tib.eu/p4-lucat/entity/"+cui+">,"
    query=query[:-1]
    query+="))} GROUP BY ?p_type"
    #print(query)
    qresults = execute_query(query)
    return [{"name":process_journal_type_string(x["name"]["value"]) , "results":x["results"]["value"]} for x in qresults]




def proccesing_response(input_dicc, limit, page, sort,topic):
    codicc=dict()
    cuis=dict()
    for elem in input_dicc["data"]:
        lcuis = input_dicc["data"][elem]
        for item in lcuis:
            cuis[item]=elem

    if len(cuis)==0:
        return []
    number_cuis=len(cuis)
        
    filters={}
    filters["journals"]=input_dicc["filter"]["journals"]
    filters["publication_types"]=input_dicc["filter"]["publication_types"]
    filters["authors"]=input_dicc["filter"]["authors"]
    
   
    #for f in filters["publication_types"]:
        #filters["publication_types"][filters["publication_types"].index(f)]=f.replace(',','')
    #for f in filters["authors"]:
        #filters["authors"][filters["authors"].index(f)]=f.replace(',','')



    codicc['resultsTotal'] = get_number_of_results(list(cuis.keys()),filters,topic)

    pubs = []
    results_pub_ranked = get_publications_ranked_data(list(cuis.keys()), limit , page , sort, filters,topic)
    for result in results_pub_ranked:
        pub1 = {}
        pub1['title'] =  result["title"]["value"]
        pub1['url'] = "https://www.ncbi.nlm.nih.gov/pubmed/"+result["id"]["value"]
        pub1['authors'] = [
            unquote(x.replace("http://research.tib.eu/p4-lucat/entity/", "")).encode('latin1').decode('utf-8')
            for x in result['authors']["value"].split(";")
        ]
        #pub1['affiliation'] = process_journal_type_string(result["affiliation"]["value"])
        pub1['journal'] = result['journal']["value"]
        pub1['year'] = int(result["year"]["value"])
        pub1['score'] = float(result["score"]["value"])/number_cuis*100
        pub1['sjr'] = float(result["sjrstr"]["value"])
        pub1['type'] = process_journal_type_string(result["type"]["value"]).replace("'","")
        pub1['hindex'] = int(result["hindex"]["value"])
        pub1['citations'] = float(result["cite"]["value"])
        pub1['group'] = cuis[result["cui"]["value"][result["cui"]["value"].rfind("/")+1:]]
        pubs.append(pub1)
        #################

    
    codicc['publications'] = pubs

    
        ######################################################################################    
    results_filters_journals = get_publications_filters_journals(list(cuis.keys()),topic)
    results_filters_types = get_publications_filters_types(list(cuis.keys()),topic)
  

        
    codicc['filter']={"journals":results_filters_journals, "publication_types": results_filters_types}

    
    
    return codicc

    


@app.route('/get_publications', methods=['POST'])
def run_exploration_api():
    if (not request.json):
        abort(400)
    if 'limit' in request.args:
        limit = int(request.args['limit'])
    else:
        limit = LIMIT
    if 'page' in request.args:
        page = int(request.args['page'])
    else:
        page = 0
    if 'sort' in request.args:
        sort = request.args['sort']
    else:
        sort = 0
    if 'topic' in request.args:
        topic = request.args['topic']
    else:
        topic = 0

    input_list = request.json
    if len(input_list) == 0:
        logger.info("Error in the input format")
        r = "{results: 'Error in the input format'}"
    else:
        response = proccesing_response(input_list, limit, page, sort,topic)
        r = json.dumps(response, indent=4)            
    logger.info("Sending the results: ")
    response = make_response(r, 200)
    response.mimetype = "application/json"
    return response

def main(*args):
    if len(args) == 1:
        myhost = args[0]
    else:
        myhost = "0.0.0.0"
    app.run(debug=False, host=myhost)
    
if __name__ == '__main__':
    main(*sys.argv[1:])
     
    
