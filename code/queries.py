QUERY_AI = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    CONSTRUCT {
    dbr:Artificial_intelligence ?p1 ?o1 .
    ?o1 ?p2 ?o2 .
    ?o2 ?p3 ?o3 .
    ?o3 ?p4 ?o4 .
    ?o4 ?p5 ?o5 .
    }
    WHERE {
    dbr:Artificial_intelligence ?p1 ?o1 .
    OPTIONAL {
        ?o1 ?p2 ?o2 .
        OPTIONAL {
        ?o2 ?p3 ?o3 .
        OPTIONAL {
            ?o3 ?p4 ?o4 .
            OPTIONAL {
            ?o4 ?p5 ?o5 .
            }
        }
        }
    }
    }
    LIMIT 100000
    """
QUERY_PERSON = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    CONSTRUCT {
    ?person rdf:type dbo:Person .
    ?person rdfs:label ?label .
    ?person dbo:birthPlace ?birthPlace .
    ?person dbo:occupation ?occupation .
    ?person dbo:knownFor ?knownFor .
    ?person dbo:spouse ?spouse .
    ?person dbo:child ?child .
    ?birthPlace rdfs:label ?birthPlaceLabel .
    ?occupation rdfs:label ?occupationLabel .
    }
    WHERE {
    ?person rdf:type dbo:Person .
    OPTIONAL { ?person rdfs:label ?label . FILTER(lang(?label) = "en") }
    OPTIONAL { ?person dbo:birthPlace ?birthPlace .
                OPTIONAL { ?birthPlace rdfs:label ?birthPlaceLabel . FILTER(lang(?birthPlaceLabel) = "en") } }
    OPTIONAL { ?person dbo:occupation ?occupation .
                OPTIONAL { ?occupation rdfs:label ?occupationLabel . FILTER(lang(?occupationLabel) = "en") } }
    OPTIONAL { ?person dbo:knownFor ?knownFor . }
    OPTIONAL { ?person dbo:spouse ?spouse . }
    OPTIONAL { ?person dbo:child ?child . }
    }
    LIMIT 10000
    """

QUERY_FILM = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    CONSTRUCT {
    ?film a dbo:Film ;
            rdfs:label ?title ;
            dbo:country dbr:Germany ;
            dbo:director ?director ;
            dbo:releaseDate ?releaseDate ;
            dbo:genre ?genre .
    }
    WHERE {
    ?film a dbo:Film ;
            dbo:country dbr:Germany ;
            rdfs:label ?title ;
            dbo:director ?director ;
            dbo:releaseDate ?releaseDate .
    OPTIONAL { ?film dbo:genre ?genre . }

    #FILTER (lang(?title) = "en")
    }
    ORDER BY DESC(?releaseDate)
    LIMIT 100
    """

QUERY_NAMED_GRAPHS = """
    SELECT ?g (COUNT(*) AS ?triples)
    WHERE {
    GRAPH ?g { ?s ?p ?o }
    }
    GROUP BY ?g
    ORDER BY ASC(?triples)
    LIMIT 50
"""