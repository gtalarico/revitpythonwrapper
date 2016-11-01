import sys

p = r"D:\Dropbox\Shared\dev\repos\revitpythonwrapper"
sys.path.append(p)

from rpw.db_wrappers import Element, ElementId
from rpw.ui_wrappers import Selection
from rpw.transaction import Transaction

print('=====================')
selection = Selection()             # Instatiate Selection Class
print(selection)                    # repr
print(selection.GetElementIds())    # original method
print(len(selection))               # len method
print(selection.element_ids)        # custom method
print(selection.elements)           # custom method
if len(selection) > 0:
    print(selection[0])             # getitem method

print('=====================')
print('ELEMENT')
if len(selection) > 0:
    element = Element(selection[0])
    print(element)
    element.id
    print(element.Id)
    print(element.id)
    # import sys; sys.exit()
    print('=====================')
    print('PARAMETERS')
    print(element.parameters)
    print(element.parameters['Commentss'])      # Non-existing returns None
    print(element.parameters['Comments'])
    print(element.parameters['Comments'].value)
    print(element.parameters['Comments'].type)
    print(element.parameters['Volume'])
    print(element.parameters['Volume'].value)
    print(element.parameters['Volume'].type)
    print(element.parameters['Base Constraint'])
    print(element.parameters['Base Constraint'].value)
    print(element.parameters['Base Constraint'].type)
    print('=====================')         # Element Id
    print('ELEMENT ID')
    print(element.Id)
    print(element.id)
    eid = element.id
    print(repr(eid))
    print(eid)
    print(int(eid))
    print('=====================')         # BuiltIn
    print('BUILT IN PARAMETER')
    wall = element
    print(wall)
    print(wall.parameters)
    bip = wall.parameters.builtins['WALL_KEY_REF_PARAM']
    print(bip)
    print(bip.value)
    print(bip.type)
    print(wall.parameters.builtins)
    print('=====================')         # BuiltIn
    print('UNWRAP')
    print(wall.unwrapped)                  # Get Revit Element
    print('=====================')         # BuiltIn
    print('SET VARIABLE')

    param = wall.parameters['Comments']
    with Transaction('Change Parameter'):
        param.value = 'Gui'
        # param.value = 156
        # param.value = None
        # param.value = eid.Id

    # Coerces Int and flots as needed for Double and Integer Type
    param = wall.parameters['Base Offset']
    with Transaction('Change Parameter'):
        param.value = 0

    # Sets Element Id to None
    param = wall.parameters['Top Constraint']
    with Transaction('Change Parameter'):
        param.value = None

    print('=====================')         # BuiltIn
    print('SET VARIABLE')



#
# # Tests
# # try:
# #     assert len(selection) == 0
# # except AssertionError:
# #     raise AssertionError('len(Selection)')
#
# print('Done!')
