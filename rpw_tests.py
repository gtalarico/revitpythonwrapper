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
from rpw.exceptions import RPW_ParameterNotFound, RPW_WrongStorageType
from rpw.logger import logger

from System.Collections.Generic import List

# logger.verbose(True)
logger.disable()

################################
# TODO:
# Finish Tests
# Set up elements for tests in code for consistency
################################


def setUpModule():
    logger.title('SETTING UP TESTS...')
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
    logger.debug('WALL CREATED.')
    logger.debug('TEST SETUP')


def tearDownModule():
    pass


######################
# COLLECTOR
######################


class CollectorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING COLLECTOR...')

    @staticmethod
    def collector_helper(filters, view=None):
        logger.debug('{}:{}'.format(filters, view))
        if not view:
            collector = Collector().filter(**filters)
        else:
            collector = Collector(view).filter(**filters)
        elements = collector.elements
        logger.debug(collector)
        logger.debug(collector.first)
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


######################
# SELECTION
######################
class SelectionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING SELECTION...')

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
        logger.debug('SELECTION TEST PASSED')


######################
# ELEMENT
######################

class ElementTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logger.title('TESTING ELEMENT...')

    def setUp(self):
        collector = Collector()
        self.wall = collector.filter(of_class='Wall').first
        self.wrapped_wall = Element(self.wall)

    def tearDown(self):
        collector = Collector()
        levels = collector.filter(of_class=DB.Level).elements
        with Transaction('Delete Test Levels'):
            for level in levels[1:]:
                doc.Delete(level.Id)

    def test_element_repr(self):
        self.wrapped_wall.__repr__()

    def test_element_id(self):
        assert isinstance(self.wrapped_wall.Id, DB.ElementId)
        assert isinstance(self.wrapped_wall.id_as_int, int)
        self.assertEqual(self.wrapped_wall.id_as_int, self.wall.Id.IntegerValue)

    def test_element_id(self):
        self.assertIsInstance(self.wrapped_wall, Element)

    def test_element_get_parameter_type(self):
        rv = self.wrapped_wall.parameters['Comments'].type
        self.assertEqual(rv, str)
        rv = self.wrapped_wall.parameters['Base Constraint'].type
        self.assertEqual(rv, DB.ElementId)
        rv = self.wrapped_wall.parameters['Unconnected Height'].type
        self.assertEqual(rv, float)
        rv = self.wrapped_wall.parameters['Room Bounding'].type
        self.assertEqual(rv, int)

    def test_element_get_parameter_name(self):
        rv = self.wrapped_wall.parameters['Comments'].name
        self.assertEqual(rv, 'Comments')

    def test_element_get_parameter(self):
        rv = self.wrapped_wall.parameters['Comments'].value
        self.assertEqual(rv, None)

    def tests_element_set_get_parameter_string(self):
        with Transaction('Set String'):
            self.wrapped_wall.parameters['Comments'].value = 'Test String'
        rv = self.wrapped_wall.parameters['Comments'].value
        self.assertEqual(rv, 'Test String')

    def tests_element_set_get_parameter_coerce_string(self):
        with Transaction('Set String'):
            self.wrapped_wall.parameters['Comments'].value = 5
        rv = self.wrapped_wall.parameters['Comments'].value
        self.assertEqual(rv, '5')

    def tests_element_set_get_parameter_float(self):
        with Transaction('Set Integer'):
            self.wrapped_wall.parameters['Unconnected Height'].value = 5.0
        rv = self.wrapped_wall.parameters['Unconnected Height'].value
        self.assertEqual(rv, 5.0)

    def tests_element_set_get_parameter_coerce_int(self):
        with Transaction('Set Coerce Int'):
            self.wrapped_wall.parameters['Unconnected Height'].value = 5
        rv = self.wrapped_wall.parameters['Unconnected Height'].value
        self.assertEqual(rv, 5.0)

    def tests_element_set_get_parameter_element_id(self):
        active_view = uidoc.ActiveView
        wrapped_view = Element(active_view)
        with Transaction('Create and Set Level'):
            try:
                new_level = DB.Level.Create(doc, 10)
            except:
                new_level = doc.Create.NewLevel(10)
            self.wrapped_wall.parameters['Top Constraint'].value = new_level.Id
        self.assertEqual(self.wrapped_wall.parameters['Top Constraint'].value.IntegerValue,
                         new_level.Id.IntegerValue)

    def test_element_get_builtin_parameter_by_strin(self):
        bip = self.wrapped_wall.parameters.builtins['WALL_KEY_REF_PARAM'].value
        self.assertIsInstance(bip, int)

    def test_element_set_get_builtin_parameter_by_strin(self):
        bip = self.wrapped_wall.parameters.builtins['WALL_KEY_REF_PARAM']
        with Transaction('Set Value'):
            bip.value = 3
        bip = self.wrapped_wall.parameters.builtins['WALL_KEY_REF_PARAM']
        self.assertEqual(bip.value, 3)

    def test_element_get_builtin_parameter_caster(self):
        bip = self.wrapped_wall.parameters.builtins['WALL_KEY_REF_PARAM'].value
        BIP_ENUM = DB.BuiltInParameter.WALL_KEY_REF_PARAM
        bip2 = self.wrapped_wall.parameters.builtins[BIP_ENUM].value
        self.assertEqual(bip, bip2)

    def tests_wrong_storage_type(self):
        with self.assertRaises(Exception) as context:
            with Transaction('Set String'):
                self.wrapped_wall.parameters['Unconnected Height'].value = 'Test'
        self.assertIsInstance(context.exception, RPW_WrongStorageType)

    def test_parameter_does_not_exist(self):
        with self.assertRaises(Exception) as context:
            self.wrapped_wall.parameters['Parameter Name']
        self.assertIsInstance(context.exception, RPW_ParameterNotFound)



# unittest.main(defaultTest='ElementTests')
unittest.main(verbosity=0, buffer=True)
sys.exit()
