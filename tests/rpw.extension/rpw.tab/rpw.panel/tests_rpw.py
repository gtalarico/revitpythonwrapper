""" Revit Python Wrapper Tests

Passes:

    * Revit:
        * Revit 2015
        * Revit 2016
"""

import sys
import unittest
import os

test_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(test_dir)
sys.path.append(root_dir)

import rpw
from rpw import DB, UI, doc, uidoc, version, clr
from rpw import List
from rpw.exceptions import RpwParameterNotFound, RpwWrongStorageType
from rpw.utils.logger import logger

# sys.exit()

def setUpModule():
    logger.title('SETTING UP TESTS...')
    logger.title('REVIT {}'.format(version))
    collector = DB.FilteredElementCollector(doc)
    walls = collector.OfClass(DB.Wall).ToElements()
    if walls:
        t = DB.Transaction(doc, 'Delete Walls')
        t.Start()
        for wall in walls:
            doc.Delete(wall.Id)
        t.Commit()
    collector = DB.FilteredElementCollector(doc)
    level = collector.OfClass(DB.Level).FirstElement()
    pt1 = DB.XYZ(0, 0, 0)
    pt2 = DB.XYZ(20, 20, 0)
    wall_line = DB.Line.CreateBound(pt1, pt2)

    t = DB.Transaction(doc, 'Add Wall')
    t.Start()
    wall = DB.Wall.Create(doc, wall_line, level.Id, False)
    t.Commit()
    global wall_int
    wall_int = wall.Id.IntegerValue
    logger.debug('WALL CREATED.')

    collector = DB.FilteredElementCollector(doc)
    desk = collector.OfCategory(DB.BuiltInCategory.OST_Furniture).FirstElement()
    if desk:
        f = desk.Family
        t = DB.Transaction(doc, 'Delete')
        t.Start()
        doc.Delete(f.Id)
        t.Commit()

    ##################################################
    # Load Fixture Family and Place Instances
    ##################################################
    logger.debug('LOADING SYMBOl')
    family_path = os.path.join(test_dir, 'fixtures', 'desk.rfa')
    if not os.path.exists(family_path):
        raise Exception('Could not find fixture: {}'.format(family_path))

    logger.debug('LOADING SYMBOl')
    family = clr.Reference[DB.Family]()
    t = DB.Transaction(doc, 'Delete')
    t.Start()
    doc.LoadFamily(family_path, family)
    t.Commit()
    family = family.Value
    symbols = []
    # for family_symbol in family.Symbols:
    for family_symbol_id in family.GetFamilySymbolIds():
        family_symbol = doc.GetElement(family_symbol_id)
        symbols.append(family_symbol)
    t = DB.Transaction(doc)
    t.Start('Place Families')
    logger.critical('Starting Transactions')
    logger.critical(symbols)
    try:
        [s.Activate() for s in symbols]
    except:
        pass # Revit < 2016
    level = DB.FilteredElementCollector(doc).OfClass(DB.Level).WhereElementIsNotElementType().FirstElement()
    doc.Create.NewFamilyInstance(DB.XYZ(5, 0, 0), symbols[0], level, DB.Structure.StructuralType.NonStructural)
    doc.Create.NewFamilyInstance(DB.XYZ(10, 4, 0), symbols[0], level, DB.Structure.StructuralType.NonStructural)
    doc.Create.NewFamilyInstance(DB.XYZ(15, 8, 0), symbols[1], level, DB.Structure.StructuralType.NonStructural)
    t.Commit()

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
        with rpw.db.Transaction('Reset Comment') as t:
            self.wall.parameters['Comments'] = ''

    def test_transaction_instance(self):
        with rpw.db.Transaction('Test Is Instance') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertIsInstance(t, DB.Transaction)

    def test_transaction_started(self):
        with rpw.db.Transaction('Has Started') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertTrue(t.HasStarted())

    def test_transaction_has_ended(self):
        with rpw.db.Transaction('Add Comment') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertFalse(t.HasEnded())

    def test_transaction_get_name(self):
        with rpw.db.Transaction('Named Transaction') as t:
            self.assertEqual(t.GetName(), 'Named Transaction')

    def test_transaction_commit_status_success(self):
        with rpw.db.Transaction('Set String') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertEqual(t.GetStatus(), DB.TransactionStatus.Started)
        self.assertEqual(t.GetStatus(), DB.TransactionStatus.Committed)


    def test_transaction_commit_status_rollback(self):
        with self.assertRaises(Exception):
            with rpw.db.Transaction('Set String') as t:
                self.wall.parameters['Top Constraint'].value = DB.ElementId('a')
        self.assertEqual(t.GetStatus(), DB.TransactionStatus.RolledBack)

    def test_transaction_group(self):
        with rpw.db.TransactionGroup('Multiple Transactions') as tg:
            self.assertEqual(tg.GetStatus(), DB.TransactionStatus.Started)
            with rpw.db.Transaction('Set String') as t:
                self.assertEqual(t.GetStatus(), DB.TransactionStatus.Started)
                self.wall.parameters['Comments'].value = '1'
            self.assertEqual(t.GetStatus(), DB.TransactionStatus.Committed)
        self.assertEqual(tg.GetStatus(), DB.TransactionStatus.Committed)

    def test_transaction_decorator(self):
        @rpw.db.Transaction.ensure('Transaction Name')
        def somefunction():
            param = self.wall.parameters['Comments'].value = '1'
            return param
        self.assertTrue(somefunction())

######################
# COLLECTOR
######################


# class CollectorTests(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         logger.title('TESTING COLLECTOR...')
#         collector = DB.FilteredElementCollector(doc)
#         cls.family_loaded = collector.OfCategory(DB.BuiltInCategory.OST_Furniture).ToElements()
#
#     @staticmethod
#     def collector_helper(filters):
#         logger.debug('{}'.format(filters))
#         collector = rpw.db.Collector(**filters)
#         elements = collector.elements
#         logger.debug(collector)
#         logger.debug(collector.first)
#         return collector
#
#     def setUp(self):
#         self.collector_helper = CollectorTests.collector_helper
#
#     def test_collector_elements(self):
#         x = self.collector_helper({'of_class': DB.View})
#         assert isinstance(x.elements[0], DB.View)
#
#     def test_collector_elements_view_element(self):
#         x = self.collector_helper({'of_class': DB.Wall, 'view': uidoc.ActiveView})
#         self.assertEqual(len(x), 1)
#
#     def test_collector_elements_view_id(self):
#         x = self.collector_helper({'of_class': DB.Wall, 'view': uidoc.ActiveView.Id})
#         self.assertEqual(len(x), 1)
#
#     def test_collector_len(self):
#         x = self.collector_helper({'of_class': DB.View})
#         assert len(x) > 1
#
#     def test_collector_first(self):
#         x = self.collector_helper({'of_class': DB.View})
#         assert isinstance(x.first, DB.View)
#
#     def test_collector_caster(self):
#         x = self.collector_helper({'of_class': DB.Wall}).elements[0]
#         assert isinstance(x, DB.Wall)
#         y = self.collector_helper({'of_class': 'Wall'}).elements[0]
#         assert isinstance(y, DB.Wall)
#
#     def test_collector_is_element(self):
#         walls = self.collector_helper({'of_category': 'OST_Walls',
#                                        'is_not_type': True})
#         assert all([isinstance(x, DB.Wall) for x in walls.elements])
#
#     def test_collector_is_element_false(self):
#         walls = self.collector_helper({'of_category': 'OST_Walls',
#                                        'is_not_type': False})
#         assert all([isinstance(x, DB.WallType) for x in walls.elements])
#
#     def test_collector_is_element_type(self):
#         walls = self.collector_helper({'of_category': 'OST_Walls',
#                                        'is_type': True})
#         assert all([isinstance(x, DB.WallType) for x in walls.elements])
#
#     def test_collector_is_element_type_false(self):
#         walls = self.collector_helper({'of_category': 'OST_Walls',
#                                        'is_type': False})
#         assert all([isinstance(x, DB.Wall) for x in walls.elements])
#
#     def test_collector_is_view_dependent(self):
#         fregions = self.collector_helper({'of_category': 'OST_FilledRegion'})
#         assert all([f.ViewSpecific for f in fregions.elements])
#         view_dependent = self.collector_helper({'is_view_independent': True})
#         assert not all([f.ViewSpecific for f in view_dependent.elements])
#
#     def test_collector_chained_calls(self):
#         wall_collector = self.collector_helper({'of_category': DB.BuiltInCategory.OST_Walls})
#         walls_category = len(wall_collector)
#         wall_collector.filter(is_not_type=True)
#         walls_elements = len(wall_collector)
#         wall_collector.filter(is_type=True)
#         walls_element_type = len(wall_collector)
#         assert walls_category > walls_elements > walls_element_type
#
#     def tests_collect_rooms(self):
#         collector = rpw.db.Collector(of_category='OST_Rooms')
#         if collector:
#             self.assertIsInstance(collector.first, DB.SpatialElement)
#             collector = rpw.db.Collector(of_class='SpatialElement')
#             self.assertIsInstance(collector.first, DB.Architecture.Room)
#
#     def test_collector_scope_elements(self):
#         """ If Collector scope is list of elements, should not find View"""
#         wall = rpw.db.Collector(of_class='Wall').first
#         collector = rpw.db.Collector(elements=[wall], of_class='View')
#         self.assertEqual(len(collector), 0)
#
#     def test_collector_scope_element_ids(self):
#         wall = rpw.db.Collector(of_class='Wall').first
#         collector = rpw.db.Collector(element_ids=[wall.Id], of_class='View')
#         self.assertEqual(len(collector), 0)
#
#     def test_collector_symbol_filter(self):
#         desk_types = rpw.db.Collector(of_class='FamilySymbol',
#                                    of_category="OST_Furniture").elements
#         self.assertEqual(len(desk_types), 3)
#
#         all_symbols = rpw.db.Collector(of_class='FamilySymbol').elements
#         self.assertGreater(len(all_symbols), 3)
#         all_symbols = rpw.db.Collector(of_class='FamilySymbol').elements
#
#         #Placed Twice
#         first_symbol = rpw.db.Collector(symbol=desk_types[0]).elements
#         self.assertEqual(len(first_symbol), 2)
#
#         #Placed Once
#         second_symbol = rpw.db.Collector(symbol=desk_types[1]).elements
#         self.assertEqual(len(second_symbol), 1)
#
#         second_symbol = rpw.db.Collector(of_class='Wall', symbol=desk_types[1]).elements
#         self.assertEqual(len(second_symbol), 0)


######################
# SELECTION
######################


# class SelectionTests(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         logger.title('TESTING SELECTION...')
#
#     def setUp(self):
#         self.selection = rpw.ui.Selection([wall_int])
#
#     def tearDown(self):
#         self.selection.clear()
#         logger.debug('SELECTION TEST PASSED')
#
#     def test_selection_element_ids(self):
#         ids = self.selection.element_ids
#         self.assertTrue(all(
#                         [isinstance(eid, DB.ElementId) for eid in ids]
#                         ))
#
#     def test_selection_elements(self):
#         elements = self.selection.elements
#         self.assertTrue(all(
#                         [isinstance(e, DB.Element) for e in elements]
#                         ))
#
#     def test_selection_by_index(self):
#         wall = self.selection[0]
#         self.assertIsInstance(wall, DB.Wall)
#
#     def test_selection_length(self):
#         self.assertEqual(len(self.selection), 1)
#
#     def test_selection_boolean(self):
#         self.assertTrue(self.selection)
#
#     def test_selection_clear(self):
#         self.selection.clear()
#         self.assertEqual(len(self.selection), 0)
#         self.selection = rpw.ui.Selection([wall_int])
#
#     def test_selection_add(self):
#         selection = rpw.ui.Selection()
#         selection.add([wall_int])
#         self.assertIsInstance(selection[0], DB.Wall)

######################
# ELEMENT
######################


# class ElementTests(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(self):
#         logger.title('TESTING ELEMENT...')
#
#     def setUp(self):
#         self.wall = rpw.db.Collector(of_class='Wall').first
#         self.wrapped_wall = rpw.Element(self.wall)
#
#     def tearDown(self):
#         collector = rpw.db.Collector()
#         levels = rpw.db.Collector(of_class=DB.Level).elements
#         with rpw.db.Transaction('Delete Test Levels'):
#             for level in levels[1:]:
#                 doc.Delete(level.Id)
#
#     def test_element_repr(self):
#         self.assertIn('<RPW_Element:<Autodesk.Revit.DB.Wall', self.wrapped_wall.__repr__())
#
#     def test_element_repr(self):
#         self.assertIsInstance(self.wrapped_wall, rpw.Element)
#         self.assertIsInstance(self.wrapped_wall.unwrap(), DB.Wall)
#
#     def test_element_id(self):
#         assert isinstance(self.wrapped_wall.Id, DB.ElementId)
#         assert isinstance(self.wrapped_wall.id_as_int, int)
#         self.assertEqual(self.wrapped_wall.id_as_int, self.wall.Id.IntegerValue)
#
#     def test_element_from_id(self):
#         element = rpw.Element.from_id(DB.ElementId(wall_int))
#         self.assertIsInstance(element, rpw.Element)
#
#     def test_element_from_int(self):
#         element = rpw.Element.from_int(wall_int)
#         self.assertIsInstance(element, rpw.Element)
#
#     def test_element_id(self):
#         self.assertIsInstance(self.wrapped_wall, rpw.Element)
#
#     def test_element_get_parameter_type(self):
#         rv = self.wrapped_wall.parameters['Comments'].type
#         self.assertEqual(rv, str)
#         rv = self.wrapped_wall.parameters['Base Constraint'].type
#         self.assertEqual(rv, DB.ElementId)
#         rv = self.wrapped_wall.parameters['Unconnected Height'].type
#         self.assertEqual(rv, float)
#         rv = self.wrapped_wall.parameters['Room Bounding'].type
#         self.assertEqual(rv, int)
#
#     def test_element_get_parameter_name(self):
#         rv = self.wrapped_wall.parameters['Comments'].name
#         self.assertEqual(rv, 'Comments')
#
#     def test_element_get_parameter(self):
#         rv = self.wrapped_wall.parameters['Comments'].value
#         self.assertEqual(rv, None)
#
#     def tests_element_set_get_parameter_string(self):
#         with rpw.db.Transaction('Set String'):
#             self.wrapped_wall.parameters['Comments'].value = 'Test String'
#         rv = self.wrapped_wall.parameters['Comments'].value
#         self.assertEqual(rv, 'Test String')
#
#     def tests_element_set_get_parameter_coerce_string(self):
#         with rpw.db.Transaction('Set String'):
#             self.wrapped_wall.parameters['Comments'].value = 5
#         rv = self.wrapped_wall.parameters['Comments'].value
#         self.assertEqual(rv, '5')
#
#     def tests_element_set_get_parameter_float(self):
#         with rpw.db.Transaction('Set Integer'):
#             self.wrapped_wall.parameters['Unconnected Height'].value = 5.0
#         rv = self.wrapped_wall.parameters['Unconnected Height'].value
#         self.assertEqual(rv, 5.0)
#
#     def tests_element_set_get_parameter_coerce_int(self):
#         with rpw.db.Transaction('Set Coerce Int'):
#             self.wrapped_wall.parameters['Unconnected Height'].value = 5
#         rv = self.wrapped_wall.parameters['Unconnected Height'].value
#         self.assertEqual(rv, 5.0)
#
#     def tests_element_set_get_parameter_element_id(self):
#         active_view = uidoc.ActiveView
#         wrapped_view = rpw.Element(active_view)
#         with rpw.db.Transaction('Create and Set Level'):
#             try:
#                 new_level = DB.Level.Create(doc, 10)
#             except:
#                 new_level = doc.Create.NewLevel(10)
#             self.wrapped_wall.parameters['Top Constraint'].value = new_level.Id
#         self.assertEqual(self.wrapped_wall.parameters['Top Constraint'].value.IntegerValue,
#                          new_level.Id.IntegerValue)
#
#     def test_element_get_builtin_parameter_by_strin(self):
#         bip = self.wrapped_wall.parameters.builtins['WALL_KEY_REF_PARAM'].value
#         self.assertIsInstance(bip, int)
#
#     def test_element_set_get_builtin_parameter_by_strin(self):
#         bip = self.wrapped_wall.parameters.builtins['WALL_KEY_REF_PARAM']
#         with rpw.db.Transaction('Set Value'):
#             bip.value = 0
#         bip = self.wrapped_wall.parameters.builtins['WALL_KEY_REF_PARAM']
#         self.assertEqual(bip.value, 0)
#
#     def test_element_get_builtin_parameter_caster(self):
#         bip = self.wrapped_wall.parameters.builtins['WALL_KEY_REF_PARAM'].value
#         BIP_ENUM = DB.BuiltInParameter.WALL_KEY_REF_PARAM
#         bip2 = self.wrapped_wall.parameters.builtins[BIP_ENUM].value
#         self.assertEqual(bip, bip2)
#
#     def tests_wrong_storage_type(self):
#         with self.assertRaises(RpwWrongStorageType) as context:
#             with rpw.db.Transaction('Set String'):
#                 self.wrapped_wall.parameters['Unconnected Height'].value = 'Test'
#
#     def test_parameter_does_not_exist(self):
#         with self.assertRaises(RpwParameterNotFound) as context:
#             self.wrapped_wall.parameters['Parameter Name']
#
#     def test_built_in_parameter_exception_raised(self):
#         with self.assertRaises(RpwParameterNotFound) as context:
#             self.wrapped_wall.parameters.builtins['PARAMETERD_DOES_NOT_EXIST']
#

######################
# Parameter Independent
######################

    # def tests_param_class(self):
    #     param = self.wall.LookupParameter('Comments')
    #     self.assertIsInstance(param, DB.Parameter)
    #     wrapped_param = rpw.Parameter(param)
    #     self.assertIs(wrapped_param.type, str)
    #     self.assertEqual(wrapped_param.builtin, DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)


############################
# COLLECTOR PARAMETER FILTER
############################

# class ParameterFilterTests(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(self):
#         logger.title('TESTING PARAMETER FILTER...')
#
#     def setUp(self):
#         collector = rpw.db.Collector()
#         self.wall = collector.filter(of_class='Wall').first
#         self.wrapped_wall = rpw.Element(self.wall)
#         with rpw.db.Transaction('Set Comment'):
#             self.wrapped_wall.parameters['Comments'].value = 'Tests'
#             self.wrapped_wall.parameters['Unconnected Height'].value = 12.0
#
#         # BIP Ids
#         self.param_id_height = rpw.enumeration.BipEnum.get_id('WALL_USER_HEIGHT_PARAM')
#         self.param_id_location = rpw.enumeration.BipEnum.get_id('WALL_KEY_REF_PARAM')
#         self.param_id_comments = rpw.enumeration.BipEnum.get_id('ALL_MODEL_INSTANCE_COMMENTS')
#         self.param_id_level_name = rpw.enumeration.BipEnum.get_id('DATUM_TEXT')
#
#     def tearDown(self):
#         pass
#
#     def test_param_filter_float_less_no(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_height, less=10.0)
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 0)
#
#     def test_param_filter_float_less_yes(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_height, less=15.0)
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 1)
#
#     def test_param_filter_float_equal(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_height, equals=12.0)
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 1)
#
#     def test_param_filter_float_not_equal(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_height, not_equals=12.0)
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 0)
#
#     def test_param_filter_float_greater(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_height, greater=10.0)
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 1)
#
#     def test_param_filter_float_multi_filter(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_height, greater=10.0, less=14.0)
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 1)
#
#     def test_param_filter_float_multi_filter(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_height, greater=10.0, not_less=14.0)
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 0)
#
#     def test_param_filter_int_equal(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_location, equals=0)
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 1)
#
#     def test_param_filter_int_less(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_location, less=3)
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#
#         self.assertEqual(len(col), 1)
#
#     def test_param_comments_equals(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_comments, equals='Tests')
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 1)
#
#     def test_param_comments_not_equals(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_comments, equals='Blaa')
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 0)
#
#     def test_param_comments_begins(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_comments, begins='Tes')
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 1)
#
#     def test_param_comments_not_begins(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_comments, equals='Bla bla')
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 0)
#
#     def test_param_comments_not_begins(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_comments, not_begins='Bla bla')
#         col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 1)
#
#     # FAILS - CASE SENSITIVE FLAG IS NOT WORKING
#     # def test_param_comments_equal_case(self):
#         # parameter_filter = rpw.ParameterFilter(self.param_id_comments, contains='tests')
#         # col = rpw.db.Collector(of_class="Wall", parameter_filter=parameter_filter)
#         # self.assertEqual(len(col), 0)
#
#     def tests_param_name_contains(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_level_name, contains='1')
#         col = rpw.db.Collector(of_category="OST_Levels", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 1)
#
#     def tests_param_name_ends(self):
#         parameter_filter = rpw.ParameterFilter(self.param_id_level_name, ends='1')
#         col = rpw.db.Collector(of_category="OST_Levels", parameter_filter=parameter_filter)
#         self.assertEqual(len(col), 1)

######################
# COERCE
######################


# class CoerceTests(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(self):
#         logger.title('TESTING COERCE FUNCITONS...')
#
#     def setUp(self):
#         collector = rpw.db.Collector()
#         self.wall = collector.filter(of_class='Wall').first
#
#     def tearDown(self):
#         pass
#
#     def test_corce_into_id(self):
#         ids = rpw.utils.coerce.to_element_ids(self.wall)
#         all_id = all([isinstance(i, DB.ElementId) for i in ids])
#         self.assertTrue(all_id)
#
#     def test_corce_into_ids(self):
#         ids = rpw.utils.coerce.to_element_ids([self.wall])
#         all_id = all([isinstance(i, DB.ElementId) for i in ids])
#         self.assertTrue(all_id)
#
#     def test_corce_element_ref_int(self):
#         element = rpw.utils.coerce.to_elements(wall_int)[0]
#         self.assertIsInstance(element, DB.Element)
#
#     def test_corce_element_ref_id(self):
#         wall_id = DB.ElementId(wall_int)
#         elements = rpw.utils.coerce.to_elements(wall_id)
#         self.assertTrue(all([isinstance(e, DB.Element) for e in elements]))
#
#     def test_corce_to_element_diverse(self):
#         wall_id = DB.ElementId(wall_int)
#         elements = rpw.utils.coerce.to_elements([wall_id, wall_int, self.wall])
#         self.assertTrue(all([isinstance(e, DB.Element) for e in elements]))


######################
# INSTANCES
######################

# class InstanceTests(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         logger.title('TESTING INSTANCES...')
#
#     def setUp(self):
#         instance = rpw.db.Collector(of_category='OST_Furniture', is_not_type=True).first
#         self.instance = rpw.Instance(instance)
#
#     def tearDown(self):
#         logger.debug('SELECTION TEST PASSED')
#
#     def test_instance_wrap(self):
#         self.assertIsInstance(self.instance, rpw.Instance)
#         self.assertIsInstance(self.instance.unwrap(), DB.FamilyInstance)
#
#     def test_instance_symbol(self):
#         symbol = self.instance.symbol
#         self.assertIsInstance(symbol, rpw.Symbol)
#         self.assertIsInstance(symbol.unwrap(), DB.FamilySymbol)
#         self.assertEqual(symbol.name, '60" x 30"')
#         self.assertEqual(len(symbol.instances), 2)
#         self.assertEqual(len(symbol.siblings), 3)
#
#     def test_instance_family(self):
#         family = self.instance.symbol.family
#         self.assertIsInstance(family, rpw.Family)
#         self.assertEqual(family.name, 'desk')
#         self.assertIsInstance(family.unwrap(), DB.Family)
#         self.assertEqual(len(family.instances), 3)
#         self.assertEqual(len(family.siblings), 1)
#         self.assertEqual(len(family.symbols), 3)
#
#     def test_instance_category(self):
#         category = self.instance.symbol.family.category
#         self.assertIsInstance(category, rpw.Category)
#         self.assertIsInstance(category.unwrap(), DB.Category)
#         self.assertEqual(category.name, 'Furniture')
#         self.assertEqual(len(category.instances), 3)
#         self.assertEqual(len(category.symbols), 3)
#         self.assertEqual(len(category.families), 1)
#
#     def test_element_factory_class(self):
#         instance = self.instance
#         symbol = instance.symbol
#         family = instance.family
#         category = instance.category
#         self.assertIsInstance(rpw.Element.Factory(instance.unwrap()), rpw.Instance)
#         self.assertIsInstance(rpw.Element.Factory(symbol.unwrap()), rpw.Symbol)
#         self.assertIsInstance(rpw.Element.Factory(family.unwrap()), rpw.Family)
#         self.assertIsInstance(rpw.Element.Factory(category.unwrap()), rpw.Category)
#
#
# class WallTests(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         logger.title('TESTING WALL...')
#
#     def setUp(self):
#         wall = rpw.db.Collector(of_class='Wall', is_not_type=True).first
#         self.wall = rpw.WallInstance(wall)
#
#     def test_wall_instance_wrap(self):
#         self.assertIsInstance(self.wall, rpw.WallInstance)
#         self.assertIsInstance(self.wall.unwrap(), DB.Wall)
#
#     def test_wall_factory(self):
#         wrapped = rpw.Element.Factory(self.wall.unwrap())
#         self.assertIsInstance(wrapped, rpw.WallInstance)
#         wrapped = rpw.Element.Factory(self.wall.symbol.unwrap())
#         self.assertIsInstance(wrapped, rpw.WallSymbol)
#         wrapped = rpw.Element.Factory(self.wall.family.unwrap())
#         self.assertIsInstance(wrapped, rpw.WallFamily)
#
#     def test_wall_instance_symbol(self):
#         wall_symbol = self.wall.symbol
#         self.assertIsInstance(wall_symbol, rpw.WallSymbol)
#         self.assertIsInstance(wall_symbol.unwrap(), DB.WallType)
#         self.assertEqual(wall_symbol.name, 'Wall 1')
#         self.assertEqual(len(wall_symbol.instances), 1)
#         self.assertEqual(len(wall_symbol.siblings), 1)
#
#     def test_wall_instance_family(self):
#         wall_family = self.wall.family
#         self.assertIsInstance(wall_family, rpw.WallFamily)
#         self.assertEqual(wall_family.unwrap(), DB.WallKind.Basic)
#         self.assertEqual(wall_family.name, 'Basic Wall')
#         self.assertEqual(len(wall_family.instances), 1)
#         self.assertEqual(len(wall_family.symbols), 1)
#         self.assertEqual(len(wall_family.siblings), 4)
#
#     def test_wall_instance_category(self):
#         wall_category = self.wall.category
#         self.assertIsInstance(wall_category, rpw.WallCategory)
#         self.assertIsInstance(wall_category.unwrap(), DB.Category)
#         self.assertEqual(wall_category.name, 'Walls')
#
#
# class RoomTests(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         pass

    # def setUp(self):
    #     wall = rpw.db.Collector(of_class='Wall', is_not_type=True).first
    #     self.wall = rpw.WallInstance(wall)
    #
    # def test_wall_instance_wrap(self):
    #     self.assertIsInstance(self.wall, rpw.WallInstance)
    #     self.assertIsInstance(self.wall.unwrap(), DB.Wall)


def run():
    # logger.disable()
    logger.verbose(False)

    from tests.tests_forms import *
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))

    # suite = unittest.TestLoader().loadTestsFromTestCase(WallTests)
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(FormTextInputTests))

    unittest.main(verbosity=3, buffer=False)
    # unittest.main(verbosity=0, defaultTest='ParameterFilterTests')
    # unittest.main(defaultTest=suite())



if __name__ == '__main__':
    run()
