endpoint =  https://lov.linkeddata.es/dataset/lov/sparql
default_graph = http://purl.org/cwmo/# 
->  41: bissi mehr als 3 min
-> mit richtigem bnode check in function: cohesion=3: 3:53
-> mit vorzeitigem abbruch bei visited=all_nodes: cohesion=3 : 3:59

endpoint_url = https://lov.linkeddata.es/dataset/lov/sparql
default_graph = http://purl.org/wf4ever/ro
-> cohesion=23: 21 s
-> mit richtigem bnode check in function: cohesion=2: 23.3 s
-> mit vorzeitigem abbruch bei visited=all_nodes: cohesion=2: 20.0 s
-> neueste version mit bnodes mit all nodes abfangen: cohesion=2: 53.6 s

endpoint_url = "https://data.europa.eu/sparql"
default_graph = "http://data.europa.eu/88u/dataset/0800af55-8e56-49a0-8986-aa55151d0440"