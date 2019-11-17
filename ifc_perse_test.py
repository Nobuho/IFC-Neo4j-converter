import ifcopenshell

ifc_file = ifcopenshell.open('tebuilding_original.ifc')

products = ifc_file.by_type('IfcProduct')

# for product in products:
#     print(product)
#     print(product.is_a())

# wall = ifc_file.by_type('IfcWall')[0]
# print(wall.GlobalId)
# print(wall.Name)

# wall = ifc_file.by_type('IfcWall')[0]
# for definition in wall.IsDefinedBy:
#     property_set = definition.RelatingPropertyDefinition
#     for property in property_set.HasProperties:
#         if property.is_a('IfcPropertySingleValue'):
#             print(property.Name)
#             print(property.NominalValue.wrappedValue)


def print_element_quantities(element_quantity):
    for quantity in element_quantity.Quantities:
        print(quantity.Name)
        if quantity.is_a('IfcQuantityLength'):
            print(quantity.LengthValue)

def print_element_type(element_Type):
    for Type in element_Type.Quantities:
        print(Type.Name)
        if Type.is_a('IfcTypeLength'):
            print(Type.LengthValue)


wall = ifc_file.by_type('IfcWall')[0]
for definition in wall.IsDefinedBy:

    if definition.is_a("IfcRelDefinesByProperties"):
        related_data = definition.RelatingPropertyDefinition
        if related_data.is_a('IfcPropertySet'):
            pass
        elif related_data.is_a('IfcElementQuantity'):
            print_element_quantities(related_data)

    elif definition.is_a("IfcRelDefinesByType"):
        print("IfcType is ", definition.RelatingType.Name)
