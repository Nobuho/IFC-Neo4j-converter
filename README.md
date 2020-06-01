# ifc-neo4j-converter

converting ifc model to neo4j graph datadbase

## Reference

ifc2cypher.py byysangkok
https://gist.github.com/ysangkok/8aa7ab1c3207536518f3c3bf5f664880

## How it works

1. Load ifc file
1. Make node and edge list inside python
1. Initialize neo4j database
1. Node creat in the database with py2neo
1. Edge creat in the database with py2neo

    Note: Node and Edge creation take so long time depends on ifc file size

## Requirement

### Python ver

- Python 3.8.0

### library

- IfcOpenShell-python 0.6.0 latest for python 3.8 64bit Windows
http://ifcopenshell.org/python
- py2neo

### Graph database

- Neo4j

## Usage

1. Start your Neo4j database
1. input yout Neo4j database username and password
    ```
    graph = Graph(auth=('username', 'password'))
    ```
1. Input yout ifc file path then run