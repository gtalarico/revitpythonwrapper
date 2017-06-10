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
from rpw import DB, UI, doc, uidoc, version, clr
from rpw import List
from rpw.exceptions import RPW_ParameterNotFound, RPW_WrongStorageType
from rpw.utils.logger import logger

import test_utils

def setUpModule():
    logger.title('SETTING UP ELEMENTS TESTS...')
    logger.title('REVIT {}'.format(version))
    uidoc.Application.OpenAndActivateDocument(os.path.join(panel_dir, 'collector.rvt'))
    test_utils.delete_all_walls()
    test_utils.make_wall()

def tearDownModule():
    test_utils.delete_all_walls()


######################
# ELEMENT
######################


class ElementTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logger.title('TESTING ELEMENT...')

    def setUp(self):
        self.wall = DB.FilteredElementCollector(doc).OfClass(DB.Wall).ToElements()[0]
        self.wrapped_wall = rpw.Element(self.wall)
        # param = self.wall.LookupParameter('Comments')
        # t = DB.Transaction(doc)
        # t.Start('Clear Comment Param')
        # param.Set('')
        # t.Commit()

    def tearDown(self):
        collector = rpw.db.Collector()
        levels = rpw.db.Collector(of_class=DB.Level).elements
        with rpw.db.Transaction('Delete Test Levels'):
            for level in levels[1:]:
                doc.Delete(level.Id)

    def test_element_repr(self):
        self.assertIn('<RPW_Element:<Autodesk.Revit.DB.Wall', self.wrapped_wall.__repr__())

    def test_element_repr(self):
        self.assertIsInstance(self.wrapped_wall, rpw.Element)
        self.assertIsInstance(self.wrapped_wall.unwrap(), DB.Wall)

    def test_element_id(self):
        assert isinstance(self.wrapped_wall.Id, DB.ElementId)

    def test_element_from_id(self):
        element = rpw.Element.from_id(self.wall.Id)
        self.assertIsInstance(element, rpw.Element)

    def test_element_from_int(self):
        element = rpw.Element.from_int(self.wall.Id.IntegerValue)
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
        with rpw.db.Transaction('Set String'):
            self.wrapped_wall.parameters['Comments'].value = 'Test String'
        rv = self.wrapped_wall.parameters['Comments'].value
        self.assertEqual(rv, 'Test String')

    def tests_element_set_get_parameter_coerce_string(self):
        with rpw.db.Transaction('Set String'):
            self.wrapped_wall.parameters['Comments'].value = 5
        rv = self.wrapped_wall.parameters['Comments'].value
        self.assertEqual(rv, '5')

    def tests_element_set_get_parameter_float(self):
        with rpw.db.Transaction('Set Integer'):
            self.wrapped_wall.parameters['Unconnected Height'].value = 5.0
        rv = self.wrapped_wall.parameters['Unconnected Height'].value
        self.assertEqual(rv, 5.0)

    def tests_element_set_get_parameter_coerce_int(self):
        with rpw.db.Transaction('Set Coerce Int'):
            self.wrapped_wall.parameters['Unconnected Height'].value = 5
        rv = self.wrapped_wall.parameters['Unconnected Height'].value
        self.assertEqual(rv, 5.0)

    def tests_element_set_get_parameter_element_id(self):
        active_view = uidoc.ActiveView
        wrapped_view = rpw.Element(active_view)
        with rpw.db.Transaction('Create and Set Level'):
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
        with rpw.db.Transaction('Set Value'):
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
            with rpw.db.Transaction('Set String'):
                self.wrapped_wall.parameters['Unconnected Height'].value = 'Test'

    def test_parameter_does_not_exist(self):
        with self.assertRaises(RPW_ParameterNotFound) as context:
            self.wrapped_wall.parameters['Parameter Name']

    def test_built_in_parameter_exception_raised(self):
        with self.assertRaises(RPW_ParameterNotFound) as context:
            self.wrapped_wall.parameters.builtins['PARAMETERD_DOES_NOT_EXIST']


#########################
# Parameters / Isolated #
#########################

    def tests_param_class(self):
        param = self.wall.LookupParameter('Comments')
        self.assertIsInstance(param, DB.Parameter)
        wrapped_param = rpw.Parameter(param)
        self.assertIs(wrapped_param.type, str)
        self.assertEqual(wrapped_param.builtin, DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)

##################################
# INSTANCES / Symbols / Families #
##################################

class InstanceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING INSTANCES...')

    def setUp(self):
        instance = rpw.db.Collector(of_category='OST_Furniture', is_not_type=True).first
        self.instance = rpw.Instance(instance)

    def tearDown(self):
        logger.debug('SELECTION TEST PASSED')

    def test_instance_wrap(self):
        self.assertIsInstance(self.instance, rpw.Instance)
        self.assertIsInstance(self.instance.unwrap(), DB.FamilyInstance)

    def test_instance_symbol(self):
        symbol = self.instance.symbol
        self.assertIsInstance(symbol, rpw.Symbol)
        self.assertIsInstance(symbol.unwrap(), DB.FamilySymbol)
        self.assertEqual(symbol.name, '60" x 30"')
        self.assertEqual(len(symbol.instances), 2)
        self.assertEqual(len(symbol.siblings), 3)

    def test_instance_family(self):
        family = self.instance.symbol.family
        self.assertIsInstance(family, rpw.Family)
        self.assertEqual(family.name, 'desk')
        self.assertIsInstance(family.unwrap(), DB.Family)
        self.assertEqual(len(family.instances), 3)
        self.assertEqual(len(family.siblings), 1)
        self.assertEqual(len(family.symbols), 3)

    def test_instance_category(self):
        category = self.instance.symbol.family.category
        self.assertIsInstance(category, rpw.Category)
        self.assertIsInstance(category.unwrap(), DB.Category)
        self.assertEqual(category.name, 'Furniture')
        self.assertEqual(len(category.instances), 3)
        self.assertEqual(len(category.symbols), 3)
        self.assertEqual(len(category.families), 1)

    def test_element_factory_class(self):
        instance = self.instance
        symbol = instance.symbol
        family = instance.family
        category = instance.category
        self.assertIsInstance(rpw.Element.Factory(instance.unwrap()), rpw.Instance)
        self.assertIsInstance(rpw.Element.Factory(symbol.unwrap()), rpw.Symbol)
        self.assertIsInstance(rpw.Element.Factory(family.unwrap()), rpw.Family)
        self.assertIsInstance(rpw.Element.Factory(category.unwrap()), rpw.Category)


##################################################
# Wall / Wall Types / Wall Kind / Wall Category  #
##################################################

class WallTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING WALL...')

    def setUp(self):
        wall = rpw.db.Collector(of_class='Wall', is_not_type=True).first
        self.wall = rpw.WallInstance(wall)

    def test_wall_instance_wrap(self):
        self.assertIsInstance(self.wall, rpw.WallInstance)
        self.assertIsInstance(self.wall.unwrap(), DB.Wall)

    def test_wall_factory(self):
        wrapped = rpw.Element.Factory(self.wall.unwrap())
        self.assertIsInstance(wrapped, rpw.WallInstance)
        wrapped = rpw.Element.Factory(self.wall.symbol.unwrap())
        self.assertIsInstance(wrapped, rpw.WallSymbol)
        wrapped = rpw.Element.Factory(self.wall.family.unwrap())
        self.assertIsInstance(wrapped, rpw.WallFamily)

    def test_wall_instance_symbol(self):
        wall_symbol = self.wall.symbol
        self.assertIsInstance(wall_symbol, rpw.WallSymbol)
        self.assertIsInstance(wall_symbol.unwrap(), DB.WallType)
        self.assertEqual(wall_symbol.name, 'Wall 1')
        self.assertEqual(len(wall_symbol.instances), 1)
        self.assertEqual(len(wall_symbol.siblings), 1)

    def test_wall_instance_family(self):
        wall_family = self.wall.family
        self.assertIsInstance(wall_family, rpw.WallFamily)
        self.assertEqual(wall_family.unwrap(), DB.WallKind.Basic)
        self.assertEqual(wall_family.name, 'Basic Wall')
        self.assertEqual(len(wall_family.instances), 1)
        self.assertEqual(len(wall_family.symbols), 1)
        self.assertEqual(len(wall_family.siblings), 4)

    def test_wall_instance_category(self):
        wall_category = self.wall.category
        self.assertIsInstance(wall_category, rpw.WallCategory)
        self.assertIsInstance(wall_category.unwrap(), DB.Category)
        self.assertEqual(wall_category.name, 'Walls')


##################
# Rooms / Areas  #
##################

class RoomTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass
        # t = DB.Transaction(doc)
        # t.Start('Add Room')


    def setUp(self):
        room = rpw.db.Collector(os_category='OST_Rooms', is_not_type=True).first
        self.wall = rpw.WallInstance(wall)
    #
    # def test_wall_instance_wrap(self):
    #     self.assertIsInstance(self.wall, rpw.WallInstance)
    #     self.assertIsInstance(self.wall.unwrap(), DB.Wall)



def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover('tests')
    unittest.main(verbosity=3, buffer=True)



if __name__ == '__main__':
    run()
