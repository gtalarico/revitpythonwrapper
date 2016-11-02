import sys
import os
repos = os.getenv('REPOS')
path = os.path.join(repos, 'revitpythonwrapper')
sys.path.append(path)

from rpw import DB, UI
from rpw.db_wrappers import Element, ElementId
from rpw.ui_wrappers import Selection
from rpw.transaction import Transaction
from rpw.exceptions import RPW_ParameterNotFound
from rpw.logger import logger

import unittest

logger.title('SELECTION')
selection = Selection()             # Instatiate Selection Class
print(selection)                    # repr
print(selection.GetElementIds())    # original method
print(len(selection))               # len method
print(selection.element_ids)        # custom method
print(selection.elements)           # custom method
if len(selection) > 0:
    print(selection[0])             # getitem method

logger.title('ELEMENT')
if len(selection) > 0:
    element = Element(selection[0])
    print(element)
    element.id
    print(element.Id)
    print(element.id)

    logger.title('PARAMETERS')
    print(element.parameters)
    print(element.parameters['Comments'])
    print(element.parameters['Comments'].value)
    print(element.parameters['Comments'].type)
    print(element.parameters['Volume'])
    print(element.parameters['Volume'].value)
    print(element.parameters['Volume'].type)
    print(element.parameters['Base Constraint'])
    print(element.parameters['Base Constraint'].value)
    print(element.parameters['Base Constraint'].type)
    try:
        print(element.parameters['Commentss'])      # Non-existing returns None
    except RPW_ParameterNotFound:
        logger.info('Parameter Not Found. Sweed.')

    logger.title('ELEMENT ID')
    print(element.Id)
    print(element.id)
    eid = element.id
    print(repr(eid))
    print(eid)
    print(int(eid))

    logger.title('BUILT IN PARAMETER')
    wall = element
    print(wall)
    print(wall.parameters)
    bip = wall.parameters.builtins['WALL_KEY_REF_PARAM']
    print(bip)
    print(bip.value)
    with Transaction('Change BIP'):
        bip.value = 3
        wall.parameters.builtins['WALL_KEY_REF_PARAM'] = 0
    print(bip.type)
    print(wall.parameters.builtins)


    logger.title('SET PARAMETERS')
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

    logger.title('INTEGRATION - SET LEVEL')
    # Select a Wall and a Level
    if len(selection) > 1:
        wall = Element(selection[0])
        level = Element(selection[1])
        param = wall.parameters['Top Constraint']
        print(param)
        print(level)
        with Transaction('Change Parameter'):
            param.value = level.Id
            wall.parameters['Top Constraint'] = level.Id
