# import re
import json
import itertools
import ifcopenshell
import sys
from py2neo import Graph, Node, Relationship

graph = Graph(auth=('neo4j', 'Neo4j'))  # http://localhost:7474
graph.delete_all()

def chunks2(iterable, size, filler=None):
    it = itertools.chain(iterable, itertools.repeat(filler, size - 1))
    chunk = tuple(itertools.islice(it, size))
    while len(chunk) == size:
        yield chunk
        chunk = tuple(itertools.islice(it, size))


class IfcTypeDict(dict):
    def __missing__(self, key):
        value = self[key] = ifcopenshell.create_entity(
            key).wrapped_data.get_attribute_names()
        return value


typeDict = IfcTypeDict()

assert typeDict["IfcWall"] == (
    'GlobalId',
    'OwnerHistory',
    'Name',
    'Description',
    'ObjectType',
    'ObjectPlacement',
    'Representation',
    'Tag')

nodes = []
edges = []

# wallid = None

ourLabel = 'test'

f = ifcopenshell.open("nmodel.ifc")

for el in f:
    tid = el.id()
    cls = el.is_a()
    pairs = []
    keys = []
    try:
        keys = [x for x in el.get_info() if x not in ["type", "id"]]
    except RuntimeError:
        # we actually can't catch this, but try anyway
        pass
    for key in keys:
        val = el[key]
        if any(hasattr(val, "is_a") and val.is_a(thisTyp)
               for thisTyp in ["IfcBoolean", "IfcLabel", "IfcText", "IfcReal"]):
            val = val.wrappedValue
        if type(val) not in (str, bool, float):
            continue
        pairs.append((key, val))

    nodes.append((tid, cls, pairs))
    for i in range(len(el)):
        try:
            el[i]
        except RuntimeError as e:
            if str(e) != "Entity not found":
                print("ID", tid, e, file=sys.stderr)
            continue
        if isinstance(el[i], ifcopenshell.entity_instance):
            if el[i].id() != 0:
                edges.append((tid, el[i].id(), typeDict[cls][i]))
                continue
            # else:
            #     print(
            #         "attribute ",
            #         typeDict[cls][i],
            #         " of ",
            #         str(tid),
            #         " is zero",
            #         file=sys.stderr)
        try:
            iter(el[i])
        except TypeError:
            continue
        destinations = [
            x.id() for x in el[i] if isinstance(
                x, ifcopenshell.entity_instance)]
        for connectedTo in destinations:
            edges.append((tid, connectedTo, typeDict[cls][i]))
if len(nodes) == 0:
    print("no nodes in file", file=sys.stderr)
    sys.exit(1)

indexes = set(["nid", "cls"])

# nobuho added

NodesCreates = []
IndexCreates = []
EdgesMatches = []
EdgesCreates = []

NodesCreates_txt = []

####################

for chunk in chunks2(nodes, 100):
    one_node = None
    idx = 0
    # NodesCreates.append("CREATE ")
    for i in chunk:
        if i is None:
            continue
        nId, cls, pairs = i
        if idx != 0:
            NodesCreates.append(",")
        idx = idx + 1

        one_node = Node(cls, nid=nId)

        for k, v in pairs:
            one_node[k] = v
            indexes.add(k)

        graph.create(one_node)

# for idxName in indexes:
#     IndexCreates.append("CREATE INDEX on :" + ourLabel + "(" + idxName + ");")

for (nId1, nId2, relType) in edges:
    # rel1 = graph.find(property_key="nid", property_value=nId1)
    # rel2 = graph.find(property_key="nid", property_value=nId2)
    graph.run(
        "MATCH (a),(b) WHERE a.nid = {:d} AND b.nid = {:d} CREATE (a)-[r:{:s}]->(b)".format(
            nId1,
            nId2,
            relType))

    # graph.create(Relationship(rel1, relType, rel2))