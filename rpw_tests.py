import sys
import os
import unittest

repos = os.getenv('REPOS')
path = os.path.join(repos, 'revitpythonwrapper')
sys.path.append(path)

from rpw import DB, UI, doc, uidoc
from rpw.wrappers import Element
from rpw.selection import Selection
from rpw.transaction import Transaction
from rpw.collector import Collector
from rpw.exceptions import RPW_ParameterNotFound
from rpw.logger import logger

from System.Collections.Generic import List

################################
# TODO:
# Finish Tests
# Set up elements for tests in code for consistency
################################


def setUpModule():
    logger.title('SETTING UP TESTS')
    collector = Collector()
    walls = collector.filter(of_class='Wall').elements
    if walls:
        with Transaction('Delete Walls'):
            for wall in walls:
                doc.Delete(wall.Id)
    collector = Collector()
    level = collector.filter(of_class='Level').first
    pt1 = DB.XYZ(0, 0, 0)
    pt2 = DB.XYZ(20, 20, 0)
    wall_line = DB.Line.CreateBound(pt1, pt2)
    with Transaction('Add Wall'):
        wall = DB.Wall.Create(doc, wall_line, level.Id, False)
    global wall_id
    wall_id = wall.Id.IntegerValue
    logger.info('WALL CREATED.')
    logger.info('TEST SETUP')


def tearDownModule():
    pass


class CollectorTests(unittest.TestCase):

    @staticmethod
    def collector_helper(filters, view=None):
        logger.title('{}:{}'.format(filters, view))
        if not view:
            collector = Collector().filter(**filters)
        else:
            collector = Collector(view).filter(**filters)
        elements = collector.elements
        logger.info(collector)
        logger.info(collector.first)
        return collector

    def setUp(self):
        self.collector_helper = CollectorTests.collector_helper

    def test_collector_elements(self):
        x = self.collector_helper({'of_class': DB.View})
        assert isinstance(x.elements[0], DB.View)

    def test_collector_len(self):
        x = self.collector_helper({'of_class': DB.View})
        assert len(x) > 1

    def test_collector_first(self):
        x = self.collector_helper({'of_class': DB.View})
        assert isinstance(x.first, DB.View)

    def test_collector_caster(self):
        x = self.collector_helper({'of_class': DB.Wall}).elements[0]
        assert isinstance(x, DB.Wall)
        y = self.collector_helper({'of_class': 'Wall'}).elements[0]
        assert isinstance(y, DB.Wall)

    def test_collector_is_element(self):
        walls = self.collector_helper({'of_category': 'OST_Walls',
                                       'is_element': True})
        assert all([isinstance(x, DB.Wall) for x in walls.elements])

    def test_collector_is_element_type(self):
        walls = self.collector_helper({'of_category': 'OST_Walls',
                                       'is_element_type': True})
        assert all([isinstance(x, DB.WallType) for x in walls.elements])

    def test_collector_is_view_dependent(self):
        fregions = self.collector_helper({'of_category': 'OST_FilledRegion'})
        assert all([f.ViewSpecific for f in fregions.elements])
        view_dependent = self.collector_helper({'is_view_independent': True})
        assert not all([f.ViewSpecific for f in view_dependent.elements])

    def test_collector_chained_calls(self):
        wall_collector = self.collector_helper({'of_category': DB.BuiltInCategory.OST_Walls})
        walls_category = len(wall_collector)
        wall_collector.filter(is_element=True)
        walls_elements = len(wall_collector)
        wall_collector.filter(is_element_type=True)
        walls_element_type = len(wall_collector)
        assert walls_category > walls_elements > walls_element_type

    # TODO:
    # - Add Room Tests


logger.title('SELECTION')
class SelectionTests(unittest.TestCase):

    def setUp(self):

        collection = List[DB.ElementId]([DB.ElementId(wall_id)])
        uidoc.Selection.SetElementIds(collection)

    def tearDown(self):
        uidoc.Selection.SetElementIds(List[DB.ElementId]())

    def test_selection(self):
        selection = Selection()             # Instatiate Selection Class
        assert isinstance(selection.GetElementIds()[0], DB.ElementId)
        assert wall_id == selection[0].Id.IntegerValue
        assert len(selection) == 1
        assert isinstance(selection.elements[0], DB.Wall)
        print('SELECTION TEST PASSED')


unittest.main()
sys.exit()

######################
# ELEMENT
######################

logger.title('ELEMENT')

collector = Collector()
walls = collector.filter(of_class='Wall').elements

print(wall_id)
# wall = doc.GetElement(wall_id)
# wrapped_wall = Element(wall)
# wrapped_wall = Element(None)

sys.exit()
print(wrapped_wall)
assert wrapped_wall.id == wall.Id
assert wrapped_wall.Id == wall.Id
assert wrapped_wall.id_as_int == wall.Id.IntegerValue

logger.title('PARAMETERS')
print(element.parameters)
print(element.parameters['Comments'])
print(element.parameters['Comments'].builtin)
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
    logger.info('Parameter Not Found. Sweet.')


logger.title('SET PARAMETERS')
wall = Element(selection[0])
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
# Select a Wall and a Level to set wall top to level
if len(selection) > 1:
    wall = Element(selection[0])
    level = Element(selection[1])
    param = wall.parameters['Top Constraint']
    print(param)
    print(level)
    with Transaction('Change Parameter'):
        param.value = level.Id
        wall.parameters['Top Constraint'] = level.Id


logger.title('BUILT IN PARAMETER')
wall = Element(selection[0])
print(wall)
print(wall.parameters)
bip = wall.parameters.builtins['WALL_KEY_REF_PARAM']
print(bip)
print(bip.value)
with Transaction('Change BIP'):
    bip.value = 3
    wall.parameters.builtins['WALL_KEY_REF_PARAM'] = 0
print(wall.parameters.builtins)
print(bip.type)
print(wall.parameters.builtins)

bip_comments = wall.parameters['Comments'].builtin
print(bip_comments)
with Transaction('Comments as BIP'):
    wall.parameters.builtins[bip_comments].value = 'BIP Commment'
