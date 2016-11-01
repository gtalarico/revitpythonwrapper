import sys

p = r"D:\Dropbox\Shared\dev\repos\revitpythonwrapper"
sys.path.append(p)

from rpw import doc, uidoc
from rpw.wrappers import BaseWrapper, Selection, Element, ElementId

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
    print(element.Id)
    print(element.id)
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
    eid = element.id
    print(repr(eid))
    print(eid)
    print(int(eid))
    print('=====================')         # BuiltIn
    wall = element
    print(wall)
    print(wall.parameters)
    bip = wall.parameters.builtins['WALL_KEY_REF_PARAM']
    print(bip)
    print(bip.value)
    print(bip.type)
    print(wall.parameters.builtins)
# # __window__.Close()
#
# # Tests
# # try:
# #     assert len(selection) == 0
# # except AssertionError:
# #     raise AssertionError('len(Selection)')
#
# print('Done!')
