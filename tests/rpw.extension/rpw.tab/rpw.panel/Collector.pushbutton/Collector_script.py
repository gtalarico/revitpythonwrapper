"""
Collector Tests

Passes:
 * 2017.1

Revit Python Wrapper
github.com/gtalarico/revitpythonwrapper
revitpythonwrapper.readthedocs.io

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

Copyright 2017 Gui Talarico

"""

import sys
import unittest
import os

parent = os.path.dirname

script_dir = parent(__file__)
panel_dir = parent(script_dir)
sys.path.append(script_dir)

import rpw
from rpw import revit, DB, UI

doc, uidoc = revit.doc, revit.uidoc

from rpw.utils.dotnet import List
from rpw.exceptions import RpwParameterNotFound, RpwWrongStorageType
from rpw.utils.logger import logger

import test_utils

def setUpModule():
    logger.title('SETTING UP COLLECTOR TESTS...')
    logger.title('REVIT {}'.format(revit.version))
    uidoc.Application.OpenAndActivateDocument(os.path.join(panel_dir, 'collector.rvt'))
    test_utils.delete_all_walls()
    test_utils.make_wall()

def tearDownModule():
    test_utils.delete_all_walls()

######################
# COLLECTOR
######################


class CollectorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING COLLECTOR...')
        collector = DB.FilteredElementCollector(doc)
        cls.family_loaded = collector.OfCategory(DB.BuiltInCategory.OST_Furniture).ToElements()

    @staticmethod
    def collector_helper(filters):
        logger.debug('{}'.format(filters))
        collector = rpw.db.Collector(**filters)
        elements = collector.elements
        logger.debug(collector)
        if collector:
            logger.debug(collector[0])
        return collector

    def setUp(self):
        self.collector_helper = CollectorTests.collector_helper

    def test_collector_elements(self):
        x = self.collector_helper({'of_class': DB.View})
        assert isinstance(x.elements[0], DB.View)

    def test_collector_elements_view_element(self):
        x = self.collector_helper({'of_class': DB.Wall, 'view': uidoc.ActiveView})
        self.assertEqual(len(x), 1)

    def test_collector_elements_view_element_another(self):
        # Id of view where everything is hidden
        view_hidden = doc.GetElement(DB.ElementId(12531))
        x = self.collector_helper({'of_class': DB.Wall, 'view': view_hidden})
        self.assertEqual(len(x), 0)

    def test_collector_elements_view_id(self):
        x = self.collector_helper({'of_class': DB.Wall, 'view': uidoc.ActiveView.Id})
        self.assertEqual(len(x), 1)

    def test_collector_len(self):
        x = self.collector_helper({'of_class': DB.View})
        assert len(x) > 1

    def test_collector_first(self):
        x = self.collector_helper({'of_class': DB.View})
        assert isinstance(x.get_first(wrapped=False), DB.View)

    def test_collector_caster(self):
        x = self.collector_helper({'of_class': DB.Wall}).elements[0]
        assert isinstance(x, DB.Wall)
        y = self.collector_helper({'of_class': 'Wall'}).elements[0]
        assert isinstance(y, DB.Wall)

    def test_collector_is_element(self):
        walls = self.collector_helper({'of_category': 'OST_Walls',
                                       'is_not_type': True})
        assert all([isinstance(x, DB.Wall) for x in walls.elements])

    def test_collector_is_element_false(self):
        walls = self.collector_helper({'of_category': 'OST_Walls',
                                       'is_not_type': False})
        assert all([isinstance(x, DB.WallType) for x in walls.elements])

    def test_collector_is_element_type(self):
        walls = self.collector_helper({'of_category': 'OST_Walls',
                                       'is_type': True})
        assert all([isinstance(x, DB.WallType) for x in walls.elements])

    def test_collector_is_element_type_false(self):
        walls = self.collector_helper({'of_category': 'OST_Walls',
                                       'is_type': False})
        assert all([isinstance(x, DB.Wall) for x in walls.elements])

    def test_collector_is_view_dependent(self):
        fregions = self.collector_helper({'of_category': 'OST_FilledRegion'})
        assert all([f.ViewSpecific for f in fregions.elements])
        view_dependent = self.collector_helper({'is_view_independent': True})
        assert not all([f.ViewSpecific for f in view_dependent.elements])

    # def test_collector_chained_calls(self):
    #     wall_collector = self.collector_helper({'of_category': DB.BuiltInCategory.OST_Walls})
    #     walls_category = len(wall_collector)
    #     wall_collector.filter(is_not_type=True)
    #     walls_elements = len(wall_collector)
    #     wall_collector.filter(is_type=True)
    #     walls_element_type = len(wall_collector)
    #     assert walls_category > walls_elements > walls_element_type

    def tests_collect_rooms(self):
        collector = rpw.db.Collector(of_category='OST_Rooms')
        if collector:
            self.assertIsInstance(collector.get_first(wrapped=False), DB.SpatialElement)
            collector = rpw.db.Collector(of_class='SpatialElement')
            self.assertIsInstance(collector.get_first(wrapped=False), DB.Architecture.Room)

    def test_collector_scope_elements(self):
        """ If Collector scope is list of elements, should not find View"""
        wall = rpw.db.Collector(of_class='Wall').get_first(wrapped=False)
        collector = rpw.db.Collector(elements=[wall], of_class='View')
        self.assertEqual(len(collector), 0)

    def test_collector_scope_element_ids(self):
        wall = rpw.db.Collector(of_class='Wall').get_first(wrapped=False)
        collector = rpw.db.Collector(element_ids=[wall.Id], of_class='View')
        self.assertEqual(len(collector), 0)

    def test_collector_symbol_filter(self):
        desk_types = rpw.db.Collector(of_class='FamilySymbol',
                                      of_category="OST_Furniture").elements
        self.assertEqual(len(desk_types), 3)

        all_symbols = rpw.db.Collector(of_class='FamilySymbol').elements
        self.assertGreater(len(all_symbols), 3)
        all_symbols = rpw.db.Collector(of_class='FamilySymbol').elements

        #Placed Twice
        first_symbol = rpw.db.Collector(symbol=desk_types[0]).elements
        self.assertEqual(len(first_symbol), 2)

        #Placed Once
        second_symbol = rpw.db.Collector(symbol=desk_types[1]).elements
        self.assertEqual(len(second_symbol), 1)

        second_symbol = rpw.db.Collector(of_class='Wall', symbol=desk_types[1]).elements
        self.assertEqual(len(second_symbol), 0)

##############################
# Built in Element Collector #
##############################

class BuiltInCollectorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING ELEMENT COLLECTOR...')

    def test_element_collector_wall(self):
        walls = rpw.db.Wall.collect()
        self.assertEqual(len(walls), 1)
        self.assertIsInstance(walls.get_first(wrapped=False), DB.Wall)

    def test_element_collector_wallsymbols(self):
        wallsymbols = rpw.db.WallType.collect()
        self.assertEqual(len(wallsymbols), 4)
        self.assertIsInstance(wallsymbols.get_first(wrapped=False), DB.WallType)

    def test_element_collector_Room(self):
        rooms = rpw.db.Room.collect()
        self.assertEqual(len(rooms), 2)
        self.assertIsInstance(rooms.get_first(wrapped=False), DB.Architecture.Room)

    def test_element_collector_Area(self):
        areas = rpw.db.Area.collect()
        self.assertEqual(len(areas), 1)
        self.assertIsInstance(areas.get_first(wrapped=False), DB.Area)

    def test_element_collector_AreaScheme(self):
        areas = rpw.db.AreaScheme.collect()
        self.assertEqual(len(areas), 2)
        self.assertIsInstance(areas.get_first(wrapped=False), DB.AreaScheme)


############################
# COLLECTOR PARAMETER FILTER
############################

class ParameterFilterTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logger.title('TESTING PARAMETER FILTER...')

    def setUp(self):
        self.wall = rpw.db.Collector(of_class='Wall').get_first(wrapped=False)
        self.wrapped_wall = rpw.db.Element(self.wall)
        with rpw.db.Transaction('Set Comment'):
            self.wrapped_wall.parameters['Comments'].value = 'Tests'
            self.wrapped_wall.parameters['Unconnected Height'].value = 12.0

        # BIP Ids

        self.param_id_height = rpw.db.builtins.BipEnum.get_id('WALL_USER_HEIGHT_PARAM')
        self.param_id_location = rpw.db.builtins.BipEnum.get_id('WALL_KEY_REF_PARAM')
        self.param_id_comments = rpw.db.builtins.BipEnum.get_id('ALL_MODEL_INSTANCE_COMMENTS')
        self.param_id_level_name = rpw.db.builtins.BipEnum.get_id('DATUM_TEXT')

    def tearDown(self):
        pass

    def test_param_filter_float_less_no(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_height, less=10.0)
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 0)

    def test_param_filter_float_less_yes(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_height, less=15.0)
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_filter_float_equal(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_height, equals=12.0)
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_filter_float_not_equal(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_height, not_equals=12.0)
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 0)

    def test_param_filter_float_greater(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_height, greater=10.0)
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_filter_float_multi_filter(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_height, greater=10.0, less=14.0)
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_filter_float_multi_filter(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_height, greater=10.0, not_less=14.0)
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 0)

    def test_param_filter_int_equal(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_location, equals=0)
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_filter_int_less(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_location, less=3)
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)

        self.assertEqual(len(col), 1)

    def test_param_comments_equals(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_comments, equals='Tests')
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_comments_not_equals(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_comments, equals='Blaa')
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 0)

    def test_param_comments_begins(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_comments, begins='Tes')
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_comments_not_begins(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_comments, equals='Bla bla')
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 0)

    def test_param_comments_not_begins(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_comments, not_begins='Bla bla')
        col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    # FAILS - CASE SENSITIVE FLAG IS NOT WORKING
    # def test_param_comments_equal_case(self):
        # parameter_filter = rpw.db.ParameterFilter(self.param_id_comments, contains='tests')
        # col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
        # self.assertEqual(len(col), 0)

    def tests_param_name_contains(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_level_name, contains='1')
        col = rpw.db.Collector(of_category="OST_Levels", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def tests_param_name_ends(self):
        parameter_filter = rpw.db.ParameterFilter(self.param_id_level_name, ends='1')
        col = rpw.db.Collector(of_category="OST_Levels", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def tests_param_id_coerce(self):
        """ Uses Param Name instead of Param Id. Works only for BIP """
        param_name = 'DATUM_TEXT'
        parameter_filter = rpw.db.ParameterFilter(param_name, ends='1')
        col = rpw.db.Collector(of_category="OST_Levels", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_from_parameter_name(self):
        """ Uses LooksUp Parameter from sample element """
        level = rpw.db.Collector(of_category="OST_Levels", is_type=False).get_first(wrapped=False)
        parameter_filter = rpw.db.ParameterFilter.from_element_and_parameter(level, 'Name', ends='1')
        col = rpw.db.Collector(of_category="OST_Levels", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)


class FilteredCollectorCompareTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING COLLECTOR...')

    def test_category(self):
        rv = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Levels).WhereElementIsElementType().ToElements()
        rv2 = rpw.db.Collector(of_category="Levels", is_type=True)
        self.assertEqual(len(rv), len(rv2))

    def test_category2(self):
        rv = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
        rv2 = rpw.db.Collector(of_category="Levels", is_type=False)
        self.assertEqual(len(rv), len(rv2))

    def test_class(self):
        rv = DB.FilteredElementCollector(doc).OfClass(DB.View).ToElements()
        rv2 = rpw.db.Collector(of_class="View")
        self.assertEqual(len(rv), len(rv2))

    def test_excludes(self):
        e = DB.FilteredElementCollector(doc).OfClass(DB.View).FirstElement()
        e = List[DB.ElementId]([e.Id])
        rv = DB.FilteredElementCollector(doc).OfClass(DB.View).Excluding(e).ToElements()

        e = rpw.db.Collector(of_class="View").wrapped_elements[0]
        rv2 = rpw.db.Collector(of_class="View", exclude=e)
        rv3 = rpw.db.Collector(of_class="View", exclude=[e])
        rv4 = rpw.db.Collector(of_class="View", exclude=e.unwrap())
        rv5 = rpw.db.Collector(of_class="View", exclude=[e.unwrap()])
        rv6 = rpw.db.Collector(of_class="View", exclude=e.Id)
        rv7 = rpw.db.Collector(of_class="View", exclude=[e.Id])

        self.assertEqual(len(rv), len(rv2))
        self.assertEqual(len(rv), len(rv3))
        self.assertEqual(len(rv), len(rv4))
        self.assertEqual(len(rv), len(rv5))
        self.assertEqual(len(rv), len(rv6))
        self.assertEqual(len(rv), len(rv7))

    def test_and(self):
        col1 = DB.FilteredElementCollector(doc).OfClass(DB.FamilySymbol)
        col2 = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Furniture).IntersectWith(col1)
        rv = col2.ToElements()

        e = rpw.db.Collector(of_class="FamilySymbol")
        rv2 = rpw.db.Collector(of_category='Furniture', and_collector=e)

        self.assertEqual(len(rv), len(rv2))
        self.assertEqual(rv[0].Id, rv2[0].Id)
        self.assertEqual(rv[1].Id, rv2[1].Id)
        self.assertEqual(rv[2].Id, rv2[2].Id)

    def test_or(self):
        col1 = DB.FilteredElementCollector(doc).OfClass(DB.View)
        col2 = DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_Furniture).UnionWith(col1)
        rv = col2.ToElements()

        e = rpw.db.Collector(of_class="View")
        rv2 = rpw.db.Collector(of_category='Furniture', or_collector=e)

        self.assertEqual(len(rv), len(rv2))
        self.assertEqual(rv[0].Id, rv2[0].Id)
        self.assertEqual(rv[1].Id, rv2[1].Id)
        self.assertEqual(rv[2].Id, rv2[2].Id)

    # TODO: Fo all FilteredElementCollector

def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)



if __name__ == '__main__':
    run()
