from SPARQLWrapper import SPARQLWrapper, JSON
from helper import MongoHelper as db 
db.connect("solutions")
sparql = SPARQLWrapper("http://dbpedia.org/sparql")

properties = [
"birthPlace",
"deathPlace",
"headquarter",
"hometown",
"residence", 
"placeOfBirth"]

def get_resources():
    sparql.setQuery("""
         PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
 PREFIX dbr: <http://dbpedia.org/resource/>
 PREFIX dbc: <http://dbpedia.org/resource/classes#>

SELECT *
    WHERE {  ?entity dbo:country dbr:Haiti;
                dbo:abstract ?abstract;
                rdfs:label ?label
OPTIONAL {
        ?entity dbo:leaderName ?leader
}

OPTIONAL {
        ?entity dbo:leaderTitle ?title  
}

OPTIONAL {
        ?entity dbo:areaTotal ?area
}
OPTIONAL {
        ?entity dbo:areaMetro ?areaMetro
}
OPTIONAL {
        ?entity dbo:populationDensity ?populationDensity
}
OPTIONAL {
        ?entity dbo:populationTotal ?population
}
OPTIONAL {
        ?entity dbo:populationMetro ?populationMetro
}
FILTER (lang(?abstract)='fr')
FILTER (lang(?label)='fr')
} 
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    cities = []
    keys = ["entity", "abstract", "label", "leader", "title", "area", "aeraMetro", "population", "populationDensity", "populationMetro"]

    for result in results["results"]["bindings"]:
        city = {}
        for key in keys: 
            if key in result: 
                city[key] = result[key]['value']
        cities.append(city)
    #print(cities)
    for city in cities: 
        get_resource(city)

def get_resource(city):
    pattern = """
    PREFIX yago: <http://dbpedia.org/class/yago/>
            PREFIX db: <http://dbpedia.org/resource/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            select * 
            where {
            ?x dbp:PROP <URI>.
            ?x dbp:name ?name.
            ?x dbo:abstract ?abstract.
            OPTIONAL{
                ?x dbo:birthDate ?birth
            }
            OPTIONAL{
                ?x dbo:deathDate ?death
            }
            OPTIONAL{
                ?x dbo:thumbnail ?thumbnail
            }
            FILTER (lang(?abstract)='fr')
            }
    """
    for prop in properties:
        _pattern = pattern.replace("URI",city['entity'])
        _pattern = _pattern.replace("PROP",prop)
        sparql.setQuery(_pattern)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        persons = []
        person = {}
        for r in results["results"]["bindings"]:
            print(r)
            if 'uri' in person and person['uri'] == r['x']['value']: 
                if not 'names' in person: 
                    person['names'] = []
                person['names'].append(r['name']['value'])
            elif person:
                persons.append(person)
                person = {}
            else:
                person['uri'] = r['x']['value']
                person['abstract'] = r['abstract']['value']
                if 'thumbnail' in r:
                    person['thumbnail'] = r['thumbnail']['value']
                if 'death' in r:
                    person['death'] = r['death']['value']
                if 'birth' in r:
                    person['birth'] = r['birth']['value']
                person['names'] = [r['name']['value']]
        city[prop] = persons
    print("Inserting...", city['entity'])
    db.insert("cities",city)

get_resources()