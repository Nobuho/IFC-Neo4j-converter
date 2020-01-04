import json
from py2neo import Graph


# replace 'foobar' with your password
graph = Graph(auth=('neo4j', 'Neo4j'))

with open('categories.json') as data_file:
    json = json.load(data_file)

query = """
WITH {json} AS document
UNWIND document.categories AS category
UNWIND category.sub_categories AS subCategory
CALL apoc.create.node([category.name], {name:subCategory.code​}) YIELD node
RETURN *
"""
# MERGE (c:CrimeCategory {name: category.name})
# MERGE (sc:SubCategory {code: subCategory.code})
# ON CREATE SET sc.description = subCategory.description
# MERGE (c)-[:CHILD]->(sc)



# Send Cypher query.
graph.run(query, json=json)