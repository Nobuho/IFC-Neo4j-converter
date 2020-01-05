import itertools
import IfcOpenShell
import sys
from py2neo import Graph, Node
import time
import csv


kkk = "nobuho"
kkk += ":INT"

ppp = [[2, 4, "", 5],["","","","",5555]]

with open("kkk.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows(ppp)

graph = Graph(auth=('neo4j', 'Neo4j'))  # http://localhost:7474
# graph.delete_all()

graph.run("CREATE(:User{name:{name1}})-[:FRIEND]->(:User{name:{name2}})", {"name1": "kokijiu", "name2": "lololo"})

a = 1