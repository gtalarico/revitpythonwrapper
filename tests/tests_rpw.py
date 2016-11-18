""" Revit Python Wrapper Tests

Passes:

    * Revit:
        * Revit 2015
        * Revit 2016
"""

# TODO: Add Forms Tests
# TODO: Add independent complex Collector Tests.

import sys
import unittest
import os

test_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(test_dir)
sys.path.append(root_dir)

import rpw
from rpw import DB, UI, doc, uidoc, version
from rpw import List
from rpw.exceptions import RPW_ParameterNotFound, RPW_WrongStorageType
from rpw.utils.logger import logger

# sys.exit()rr
# TODO: Finish wall specific handler
# TODO: Add tests to symbol collector
# TODO: Instance Tests
# TODO: Symbols Tests
# TODO: Family Tests
# TODO: Category Tests

# from rpw.instance import Instance
#
# for element in rpw.Selection():
#     instance = Instance(element)
#     print(element)
#
#     logger.title('Instance:')
#     print(instance)
#     logger.title('Symbol:')
#     print(instance.symbol)
#     logger.title('Instances:')
#     print(instance.symbol.instances)
#     logger.title('Symbol Name:')
#     print(instance.symbol.name)
#     logger.title('Family:')
#     print(instance.symbol.family)
#     logger.title('Family Name:')
#     print(instance.symbol.family.name)
#     logger.title('Symbol Siblings:')
#     print(instance.symbol.siblings)
#     logger.title('Familly Siblings (Other Symbols):')
#     print(instance.symbol.family.symbols)
#     logger.title('Category:')
#     print(instance.symbol.family.category)
#     logger.title('Category Name:')
#     print(instance.symbol.family.category.name)
#
# sys.exit()

def setUpModule():
    logger.title('SETTING UP TESTS...')
    logger.title('REVIT {}'.format(version))
    collector = rpw.Collector()
    walls = collector.filter(of_class='Wall').elements
    if walls:
        with rpw.Transaction('Delete Walls'):
            for wall in walls:
                doc.Delete(wall.Id)
    collector = rpw.Collector()
    level = collector.filter(of_class='Level').first
    pt1 = DB.XYZ(0, 0, 0)
    pt2 = DB.XYZ(20, 20, 0)
    wall_line = DB.Line.CreateBound(pt1, pt2)

    with rpw.Transaction('Add Wall'):
        wall = DB.Wall.Create(doc, wall_line, level.Id, False)
    global wall_int
    wall_int = wall.Id.IntegerValue
    logger.debug('WALL CREATED.')
    logger.debug('TEST SETUP')


def tearDownModule():
    pass


######################
# TRANSACTIONS
######################


class TransactionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.title('TESTING TRANSACTIONS...')

    def setUp(self):
        self.wall = rpw.Element.from_int(wall_int)
        with rpw.Transaction('Reset Comment') as t:
            self.wall.parameters['Comments'] = ''

    def test_transaction_instance(self):
        with rpw.Transaction('Test Is Instance') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertIsInstance(t, DB.Transaction)

    def test_transaction_started(self):
        with rpw.Transaction('Has Started') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertTrue(t.HasStarted())

    def test_transaction_has_ended(self):
        with rpw.Transaction('Add Comment') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertFalse(t.HasEnded())

    def test_transaction_get_name(self):
        with rpw.Transaction('Named Transaction') as t:
            self.assertEqual(t.GetName(), 'Named Transaction')

    def test_transaction_commit_status_success(self):
        with rpw.Transaction('Set String') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertEqual(t.GetStatus(), DB.TransactionStatus.Started)
        self.assertEqual(t.GetStatus(), DB.TransactionStatus.Committed)

    # Rollback Works but fails on exception
    # def test_transaction_commit_status_rollback(self):
    #     with rpw.Transaction('Set String') as t:
    #         with self.assertRaises(Exception):
    #         self.wall.parameters['Top Constraint'].value = DB.ElementId('a')
    #     logger.critical('>>>' + str(t.GetStatus()))
    #     self.assertEqual(t.GetStatus(), DB.TransactionStatus.RolledBack)

    def test_transaction_group(self):
        with rpw.TransactionGroup('Multiple Transactions') as tg:
            self.assertEqual(tg.GetStatus(), DB.TransactionStatus.Started)
            with rpw.Transaction('Set String') as t:
                self.assertEqual(t.GetStatus(), DB.TransactionStatus.Started)
                self.wall.parameters['Comments'].value = '1'
            self.assertEqual(t.GetStatus(), DB.TransactionStatus.Committed)
        self.assertEqual(tg.GetStatus(), DB.TransactionStatus.Committed)

    def test_transaction_decorator(self):
        @rpw.Transaction.ensure('Transaction Name')
        def somefunction():
            param = self.wall.parameters['Comments'].value = '1'
            return param
        self.assertTrue(somefunction())

######################
# COLLECTOR
######################


class CollectorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING COLLECTOR...')

    @staticmethod
    def collector_helper(filters):
        logger.debug('{}'.format(filters))
        collector = rpw.Collector(**filters)
        elements = collector.elements
        logger.debug(collector)
        logger.debug(collector.first)
        return collector

    def setUp(self):
        self.collector_helper = CollectorTests.collector_helper

    def test_collector_elements(self):
        x = self.collector_helper({'of_class': DB.View})
        assert isinstance(x.elements[0], DB.View)

    def test_collector_elements_view(self):
        x = self.collector_helper({'of_class': DB.Wall, 'view': uidoc.ActiveView})
        self.assertEqual(len(x), 1)

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
                                       'is_not_type': True})
        assert all([isinstance(x, DB.Wall) for x in walls.elements])

    def test_collector_is_element_type(self):
        walls = self.collector_helper({'of_category': 'OST_Walls',
                                       'is_type': True})
        assert all([isinstance(x, DB.WallType) for x in walls.elements])

    def test_collector_is_view_dependent(self):
        fregions = self.collector_helper({'of_category': 'OST_FilledRegion'})
        assert all([f.ViewSpecific for f in fregions.elements])
        view_dependent = self.collector_helper({'is_view_independent': True})
        assert not all([f.ViewSpecific for f in view_dependent.elements])

    def test_collector_chained_calls(self):
        wall_collector = self.collector_helper({'of_category': DB.BuiltInCategory.OST_Walls})
        walls_category = len(wall_collector)
        wall_collector.filter(is_not_type=True)
        walls_elements = len(wall_collector)
        wall_collector.filter(is_type=True)
        walls_element_type = len(wall_collector)
        assert walls_category > walls_elements > walls_element_type

    def tests_collect_rooms(self):
        collector = rpw.Collector(of_category='OST_Rooms')
        if collector:
            self.assertIsInstance(collector.first, DB.SpatialElement)
            collector = rpw.Collector(of_class='SpatialElement')
            self.assertIsInstance(collector.first, DB.Architecture.Room)

    def test_collector_scope_elements(self):
        """ If Collector scope is list of elements, should not find View"""
        wall = rpw.Collector(of_class='Wall').first
        collector = rpw.Collector(elements=[wall], of_class='View')
        self.assertEqual(len(collector), 0)

    def test_collector_scope_element_ids(self):
        wall = rpw.Collector(of_class='Wall').first
        collector = rpw.Collector(element_ids=[wall.Id], of_class='View')
        self.assertEqual(len(collector), 0)

######################
# SELECTION
######################


class SelectionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING SELECTION...')

    def setUp(self):
        self.selection = rpw.Selection([wall_int])

    def tearDown(self):
        self.selection.clear()
        logger.debug('SELECTION TEST PASSED')

    def test_selection_element_ids(self):
        ids = self.selection.element_ids
        self.assertTrue(all(
                        [isinstance(eid, DB.ElementId) for eid in ids]
                        ))

    def test_selection_elements(self):
        elements = self.selection.elements
        self.assertTrue(all(
                        [isinstance(e, DB.Element) for e in elements]
                        ))

    def test_selection_by_index(self):
        wall = self.selection[0]
        self.assertIsInstance(wall, DB.Wall)

    def test_selection_length(self):
        self.assertEqual(len(self.selection), 1)

    def test_selection_boolean(self):
        self.assertTrue(self.selection)

    def test_selection_clear(self):
        self.selection.clear()
        self.assertEqual(len(self.selection), 0)
        self.selection = rpw.Selection([wall_int])

    def test_selection_add(self):
        selection = rpw.Selection()
        selection.add([wall_int])
        self.assertIsInstance(selection[0], DB.Wall)

######################
# ELEMENT
######################


class ElementTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logger.title('TESTING ELEMENT...')

    def setUp(self):
        self.wall = rpw.Collector(of_class='Wall').first
        self.wrapped_wall = rpw.Element(self.wall)

    def tearDown(self):
        collector = rpw.Collector()
        levels = rpw.Collector(of_class=DB.Level).elements
        with rpw.Transaction('Delete Test Levels'):
            for level in levels[1:]:
                doc.Delete(level.Id)

    def test_element_repr(self):
        self.wrapped_wall.__repr__()

    def test_element_id(self):
        assert isinstance(self.wrapped_wall.Id, DB.ElementId)
        assert isinstance(self.wrapped_wall.id_as_int, int)
        self.assertEqual(self.wrapped_wall.id_as_int, self.wall.Id.IntegerValue)

    def test_element_from_id(self):
        element = rpw.Element.from_id(DB.ElementId(wall_int))
        self.assertIsInstance(element, rpw.Element)

    def test_element_from_int(self):
        element = rpw.Element.from_int(wall_int)
        self.assertIsInstance(element, rpw.Element)

    def test_element_id(self):
        self.assertIsInstance(self.wrapped_wall, rpw.Element)

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
        with rpw.Transaction('Set String'):
            self.wrapped_wall.parameters['Comments'].value = 'Test String'
        rv = self.wrapped_wall.parameters['Comments'].value
        self.assertEqual(rv, 'Test String')

    def tests_element_set_get_parameter_coerce_string(self):
        with rpw.Transaction('Set String'):
            self.wrapped_wall.parameters['Comments'].value = 5
        rv = self.wrapped_wall.parameters['Comments'].value
        self.assertEqual(rv, '5')

    def tests_element_set_get_parameter_float(self):
        with rpw.Transaction('Set Integer'):
            self.wrapped_wall.parameters['Unconnected Height'].value = 5.0
        rv = self.wrapped_wall.parameters['Unconnected Height'].value
        self.assertEqual(rv, 5.0)

    def tests_element_set_get_parameter_coerce_int(self):
        with rpw.Transaction('Set Coerce Int'):
            self.wrapped_wall.parameters['Unconnected Height'].value = 5
        rv = self.wrapped_wall.parameters['Unconnected Height'].value
        self.assertEqual(rv, 5.0)

    def tests_element_set_get_parameter_element_id(self):
        active_view = uidoc.ActiveView
        wrapped_view = rpw.Element(active_view)
        with rpw.Transaction('Create and Set Level'):
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
        with rpw.Transaction('Set Value'):
            bip.value = 0
        bip = self.wrapped_wall.parameters.builtins['WALL_KEY_REF_PARAM']
        self.assertEqual(bip.value, 0)

    def test_element_get_builtin_parameter_caster(self):
        bip = self.wrapped_wall.parameters.builtins['WALL_KEY_REF_PARAM'].value
        BIP_ENUM = DB.BuiltInParameter.WALL_KEY_REF_PARAM
        bip2 = self.wrapped_wall.parameters.builtins[BIP_ENUM].value
        self.assertEqual(bip, bip2)

    def tests_wrong_storage_type(self):
        with self.assertRaises(RPW_WrongStorageType) as context:
            with rpw.Transaction('Set String'):
                self.wrapped_wall.parameters['Unconnected Height'].value = 'Test'

    def test_parameter_does_not_exist(self):
        with self.assertRaises(RPW_ParameterNotFound) as context:
            self.wrapped_wall.parameters['Parameter Name']

    def test_built_in_parameter_exception_raised(self):
        with self.assertRaises(RPW_ParameterNotFound) as context:
            self.wrapped_wall.parameters.builtins['PARAMETERD_DOES_NOT_EXIST']


######################
# Parameter Independent
######################

    def tests_param_class(self):
        param = self.wall.LookupParameter('Comments')
        self.assertIsInstance(param, DB.Parameter)
        wrapped_param = rpw.Parameter(param)
        self.assertIs(wrapped_param.type, str)
        self.assertEqual(wrapped_param.builtin, DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)


############################
# COLLECTOR PARAMETER FILTER
############################

class ParameterFilterTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logger.title('TESTING PARAMETER FILTER...')

    def setUp(self):
        collector = rpw.Collector()
        self.wall = collector.filter(of_class='Wall').first
        self.wrapped_wall = rpw.Element(self.wall)
        with rpw.Transaction('Set Comment'):
            self.wrapped_wall.parameters['Comments'].value = 'Tests'
            self.wrapped_wall.parameters['Unconnected Height'].value = 12.0

        # BIP Ids
        self.param_id_height = rpw.BipEnum.get_id('WALL_USER_HEIGHT_PARAM')
        self.param_id_location = rpw.BipEnum.get_id('WALL_KEY_REF_PARAM')
        self.param_id_comments = rpw.BipEnum.get_id('ALL_MODEL_INSTANCE_COMMENTS')
        self.param_id_level_name = rpw.BipEnum.get_id('DATUM_TEXT')

    def tearDown(self):
        pass

    def test_param_filter_float_less_no(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_height, less=10.0)
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 0)

    def test_param_filter_float_less_yes(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_height, less=15.0)
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_filter_float_equal(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_height, equals=12.0)
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_filter_float_not_equal(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_height, not_equals=12.0)
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 0)

    def test_param_filter_float_greater(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_height, greater=10.0)
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_filter_float_multi_filter(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_height, greater=10.0, less=14.0)
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_filter_float_multi_filter(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_height, greater=10.0, not_less=14.0)
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 0)

    def test_param_filter_int_equal(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_location, equals=0)
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_filter_int_less(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_location, less=3)
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)

        self.assertEqual(len(col), 1)

    def test_param_comments_equals(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_comments, equals='Tests')
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_comments_not_equals(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_comments, equals='Blaa')
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 0)

    def test_param_comments_begins(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_comments, begins='Tes')
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def test_param_comments_not_begins(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_comments, equals='Bla bla')
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 0)

    def test_param_comments_not_begins(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_comments, not_begins='Bla bla')
        col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    # FAILS - CASE SENSITIVE FLAG IS NOT WORKING
    # def test_param_comments_equal_case(self):
        # parameter_filter = rpw.ParameterFilter(self.param_id_comments, contains='tests')
        # col = rpw.Collector(of_class="Wall", parameter_filter=parameter_filter)
        # self.assertEqual(len(col), 0)

    def tests_param_name_contains(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_level_name, contains='1')
        col = rpw.Collector(of_category="OST_Levels", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

    def tests_param_name_ends(self):
        parameter_filter = rpw.ParameterFilter(self.param_id_level_name, ends='1')
        col = rpw.Collector(of_category="OST_Levels", parameter_filter=parameter_filter)
        self.assertEqual(len(col), 1)

######################
# COERCE
######################


class CoerceTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logger.title('TESTING COERCE FUNCITONS...')

    def setUp(self):
        collector = rpw.Collector()
        self.wall = collector.filter(of_class='Wall').first

    def tearDown(self):
        pass

    def test_corce_into_id(self):
        ids = rpw.utils.coerce.to_element_ids(self.wall)
        all_id = all([isinstance(i, DB.ElementId) for i in ids])
        self.assertTrue(all_id)

    def test_corce_into_ids(self):
        ids = rpw.utils.coerce.to_element_ids([self.wall])
        all_id = all([isinstance(i, DB.ElementId) for i in ids])
        self.assertTrue(all_id)

    def test_corce_element_ref_int(self):
        element = rpw.utils.coerce.to_elements(wall_int)[0]
        self.assertIsInstance(element, DB.Element)

    def test_corce_element_ref_id(self):
        wall_id = DB.ElementId(wall_int)
        elements = rpw.utils.coerce.to_elements(wall_id)
        self.assertTrue(all([isinstance(e, DB.Element) for e in elements]))

    def test_corce_to_element_diverse(self):
        wall_id = DB.ElementId(wall_int)
        elements = rpw.utils.coerce.to_elements([wall_id, wall_int, self.wall])
        self.assertTrue(all([isinstance(e, DB.Element) for e in elements]))


if __name__ == '__main__':
    logger.verbose(False)
    # logger.disable()
    unittest.main(verbosity=3, buffer=False)
    # unittest.main(verbosity=0, buffer=True)
    # unittest.main(verbosity=0, defaultTest='ParameterFilterTests')
    # unittest.main(defaultTest='SelectionTests')
