import IfcOpenShell
import sys
import time
import csv


class IfcTypeDict(dict):
    def __missing__(self, key):
        value = self[key] = IfcOpenShell.create_entity(
            key).wrapped_data.get_attribute_names()
        return value


start = time.time()  # Culculate time to process

ifc_path = "ifc_files/IfcOpenHouse_original.ifc"
# ifc_path = "ifc_files/191225_TE-Bld_zone_GEO.ifc"
# ifc_path = "ifc_files/191225_TE-Bld_arch_GEO.ifc"
start = time.time()  # Culculate time to process
print("Start!")
print(time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime())))
log1 = str(time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime()))) + " Start "


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

f = IfcOpenShell.open(ifc_path)

for el in f:
    if el.is_a() == "IfcOwnerHistory":
        continue
    tid = el.id()
    cls = el.is_a()
    nod = {"nid:ID": tid, ":LABEL": cls}
    keys = []
    try:
        keys = [x for x in el.get_info() if x not in ["type", "id", "OwnerHistory"]]
    except RuntimeError:
        # we actually can't catch this, but try anyway
        pass
    for key in keys:
        val = el[key]
        if any(hasattr(val, "is_a") and val.is_a(thisTyp)
               for thisTyp in ["IfcBoolean", "IfcLabel", "IfcText", "IfcReal"]):
            val = val.wrappedValue
        if val and type(val) is tuple and type(val[0]) in (str, bool, float, int):
            val = ",".join(str(x) for x in val)
        if type(val) not in (str, bool, float, int):
            continue
        nod[key] = val
    nodes.append(nod)

    for i in range(len(el)):
        try:
            el[i]
        except RuntimeError as e:
            if str(e) != "Entity not found":
                print("ID", tid, e, file=sys.stderr)
            continue
        if isinstance(el[i], IfcOpenShell.entity_instance):
            if el[i].is_a() == "IfcOwnerHistory":
                continue
            if el[i].id() != 0:
                edges.append([tid, el[i].id(), typeDict[cls][i]])
                continue
        try:
            iter(el[i])
        except TypeError:
            continue
        destinations = [
            x.id() for x in el[i] if isinstance(
                x, IfcOpenShell.entity_instance)]
        for connectedTo in destinations:
            # edges.append({"from": tid, "to": connectedTo, "reltype": typeDict[cls][i]})
            edges.append([tid, connectedTo, typeDict[cls][i]])

if len(nodes) == 0:
    print("no nodes in file", file=sys.stderr)
    sys.exit(1)

cls_list = set([i[":LABEL"] for i in nodes])

nodes_final = {}

for s_cls in cls_list:
    ccc = [i for i in nodes if i[":LABEL"] == s_cls]
    nodes_final[s_cls] = ccc
    
    # for header in headers:
    #     val_type = set([type(p[header]) for p in ccc])
    #     if header == "nid:ID" or len(val_type) >= 2:
    #         continue
    #     if val_type is {str} or val_type is  {float}:
    #         print("NUM")
    #         header[header.index(i)] += ":int"
    # rows = [[v if v is not None else "" for v in p.values()] for p in ccc] 
    # csv_path = "importer_csv/" + s_cls + ".csv"
    # with open(csv_path, 'w', newline="") as f:
    #     writer = csv.writer(f)
    #     writer.writerow(header)
    #     writer.writerows(rows)

print("List creat prosess done. Take for ", round(time.time() - start))
print(time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime())))
log2 = str(round(time.time() - start)) + "sec.\n" + str(time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime()))) + " List creat prosess done"

# Initialize neo4j database
# graph = Graph(auth=('neo4j', 'Neo4j'))  # http://localhost:7474
# graph.delete_all()

# for node in nodes:
#     nId, cls, pairs = node
#     one_node = Node(cls, nid=nId)
#     for k, v in pairs:
#         one_node[k] = v
#     graph.create(one_node)

# print("Node creat prosess done. Take for ", round(time.time() - start))
# print(time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime())))
# log2 = str(round(time.time() - start)) + "sec.\n" + str(time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime()))) + " Node creat prosess done"

# query_rel = """
# MATCH (a:{cls1})
# WHERE a.nid = {id1}
# MATCH (b:{cls2})
# WHERE b.nid = {id2}
# CREATE (a)-[:{relType}]->(b)
# """

# for (id1, cls1, id2, cls2, relType) in edges:
#     graph.run(query_rel.format(cls1=cls1, cls2=cls2, id1=id1, id2=id2, relType=relType))
# print("All done. Take for ", round(time.time() - start))
# print(time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime())))
# log3 = str(round(time.time() - start)) + "sec.\n" + str(time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time.ctime()))) + " All done"

# with open("log.text", mode="a") as f:
#     f.write(ifc_path + "\n" )
#     f.write("Nodes_" + str(len(nodes)) + " ,Edges_" + str(len(edges)) + "\n")
#     f.write(log1 + "\n")
#     f.write(log2 + "\n")
#     f.write(log3 + "\n\n")