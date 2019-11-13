from py2neo import Graph, Node, Relationship

graph = Graph(auth=('neo4j', 'Neo4j'))  # http://localhost:7474

graph.delete_all()

graph.create(
    Node('IfcPerson', nid=1, FamilyName="\u672a\u5b9a\u7fa9")
    | Node('IfcOrganization', nid=3, Name="\u672a\u5b9a\u7fa9")
    | Node('IfcPersonAndOrganization', nid=7)
    | Node('IfcOrganization', nid=10, Id="GS", Description="GRAPHISOFT", Name="GRAPHISOFT")
    | Node('IfcApplication', nid=11, ApplicationIdtifier="IFC add-on version=5009 JPN FULL", Version="22.0.0", ApplicationFullName="ARCHICAD-64")
    | Node('IfcOwnerHistory', nid=12, ChangeAction="ADDED")
    | Node('IfcSIUnit', nid=13, UnitType="LENGTHUNIT", Name="METRE", Prefix="MILLI")
    | Node('IfcSIUnit', nid=14, UnitType="AREAUNIT", Name="SQUARE_METRE")
    | Node('IfcSIUnit', nid=15, UnitType="VOLUMEUNIT", Name="CUBIC_METRE")
    | Node('IfcSIUnit', nid=16, UnitType="PLANEANGLEUNIT", Name="RADIAN")
    | Node('IfcMeasureWithUnit', nid=17)
    | Node('IfcDimensionalExponents', nid=18)
    | Node('IfcConversionBasedUnit', nid=19, UnitType="PLANEANGLEUNIT", Name="DEGREE")
    | Node('IfcSIUnit', nid=20, UnitType="SOLIDANGLEUNIT", Name="STERADIAN")
    | Node('IfcMonetaryUnit', nid=21, Currency="JPY")
    | Node('IfcSIUnit', nid=22, UnitType="TIMEUNIT", Name="SECOND")
)

##############################################################

# tx = graph.begin()

# a = | Node("Person", name="Alice")

# tx.create(a)

# b = | Node("Person", name="Bob")
# ab = Relationship(a, "KNOWS", b)

# tx.create(ab)
# tx.commit()
# print(graph.exists(ab))

##############################################################

# nicole = | Node("Person", name="Nicole", age=24)
# drew = | Node("Person", name="Drew", age=20)

# mtdew = | Node("Drink", name="Mountain Dew", calories=9000)
# cokezero = | Node("Drink", name="Coke Zero", calories=0)

# coke = | Node("Manufacturer", name="Coca Cola")
# pepsi = | Node("Manufacturer", name="Pepsi")

# graph.create(nicole | drew | mtdew | cokezero | coke | pepsi)

# graph.create(Relationship(nicole, "LIKES", cokezero))
# graph.create(Relationship(nicole, "LIKES", mtdew))
# graph.create(Relationship(drew, "LIKES", mtdew))
# graph.create(Relationship(coke, "MAKES", cokezero))
# graph.create(Relationship(pepsi, "MAKES", mtdew))
