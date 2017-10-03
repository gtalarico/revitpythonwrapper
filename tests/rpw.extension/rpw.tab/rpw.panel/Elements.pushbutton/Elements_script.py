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
from rpw.utils.dotnet import List
from rpw.exceptions import RpwParameterNotFound, RpwWrongStorageType, RpwCoerceError
from rpw.utils.logger import logger

import test_utils

def setUpModule():
    logger.title('SETTING UP ELEMENTS TESTS...')
    revit.uidoc.Application.OpenAndActivateDocument(os.path.join(panel_dir, 'collector.rvt'))
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
        self.wall = DB.FilteredElementCollector(revit.doc).OfClass(DB.Wall).ToElements()[0]
        self.wrapped_wall = rpw.db.Element(self.wall)
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
                revit.doc.Delete(level.Id)

    def test_element_repr(self):
        self.assertIn('<RPW_Element:<Autodesk.Revit.DB.Wall', self.wrapped_wall.__repr__())

    def test_element_repr(self):
        self.assertIsInstance(self.wrapped_wall, rpw.db.Element)
        self.assertIsInstance(self.wrapped_wall.unwrap(), DB.Wall)

    def test_element_id(self):
        assert isinstance(self.wrapped_wall.Id, DB.ElementId)

    def test_element_from_id(self):
        element = rpw.db.Element.from_id(self.wall.Id)
        self.assertIsInstance(element, rpw.db.Element)

    def test_element_from_int(self):
        element = rpw.db.Element.from_int(self.wall.Id.IntegerValue)
        self.assertIsInstance(element, rpw.db.Element)

    def test_element_id(self):
        self.assertIsInstance(self.wrapped_wall, rpw.db.Element)

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
        active_view = revit.uidoc.ActiveView
        wrapped_view = rpw.db.Element(active_view)
        with rpw.db.Transaction('Create and Set Level'):
            try:
                new_level = DB.Level.Create(revit.doc, 10)
            except:
                new_level = revit.doc.Create.NewLevel(10)
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
        with self.assertRaises(RpwWrongStorageType) as context:
            with rpw.db.Transaction('Set String'):
                self.wrapped_wall.parameters['Unconnected Height'].value = 'Test'

    def test_parameter_does_not_exist(self):
        with self.assertRaises(RpwParameterNotFound) as context:
            self.wrapped_wall.parameters['Parameter Name']

    def test_built_in_parameter_exception_raised(self):
        with self.assertRaises(RpwCoerceError) as context:
            self.wrapped_wall.parameters.builtins['PARAMETERD_DOES_NOT_EXIST']


#########################
# Parameters / Isolated #
#########################

    def tests_param_class(self):
        param = self.wall.LookupParameter('Comments')
        self.assertIsInstance(param, DB.Parameter)
        wrapped_param = rpw.db.Parameter(param)
        self.assertIs(wrapped_param.type, str)
        self.assertEqual(wrapped_param.builtin, DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS)

################################### INSTANCES / Symbols / Families #
##################################

class InstanceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING INSTANCES...')

    def setUp(self):
        instance = rpw.db.Collector(of_category='OST_Furniture', is_not_type=True).get_first(wrapped=False)
        self.instance = rpw.db.FamilyInstance(instance)

    def tearDown(self):
        logger.debug('SELECTION TEST PASSED')

    def test_instance_wrap(self):
        self.assertIsInstance(self.instance, rpw.db.FamilyInstance)
        self.assertIsInstance(self.instance.unwrap(), DB.FamilyInstance)

    def test_instance_symbol(self):
        symbol = self.instance.symbol
        self.assertIsInstance(symbol, rpw.db.FamilySymbol)
        self.assertIsInstance(symbol.unwrap(), DB.FamilySymbol)
        self.assertEqual(symbol.name, '60" x 30"')
        self.assertEqual(len(symbol.instances), 2)
        self.assertEqual(len(symbol.siblings), 3)

    def test_instance_family(self):
        family = self.instance.symbol.family
        self.assertIsInstance(family, rpw.db.Family)
        self.assertEqual(family.name, 'desk')
        self.assertIsInstance(family.unwrap(), DB.Family)
        self.assertEqual(len(family.instances), 3)
        self.assertEqual(len(family.siblings), 1)
        self.assertEqual(len(family.symbols), 3)

    def test_instance_category(self):
        category = self.instance.symbol.family.category
        self.assertIsInstance(category, rpw.db.Category)
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
        self.assertIsInstance(rpw.db.Element.Factory(instance.unwrap()), rpw.db.FamilyInstance)
        self.assertIsInstance(rpw.db.Element.Factory(symbol.unwrap()), rpw.db.FamilySymbol)
        self.assertIsInstance(rpw.db.Element.Factory(family.unwrap()), rpw.db.Family)

        # TODO: Move this. Category No Longer Element
        # self.assertIsInstance(rpw.db.Element.Factory(category.unwrap()), rpw.db.Category)


##################################################
# Wall / Wall Types / Wall Kind / Wall Category  #
##################################################

class WallTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING WALL...')

    def setUp(self):
        test_utils.delete_all_walls()
        test_utils.make_wall()
        wall = rpw.db.Collector(of_class='Wall', is_not_type=True).get_first(wrapped=False)
        self.wall = rpw.db.wall.Wall(wall)

    def tearDown(self):
        test_utils.delete_all_walls()

    def test_wall_instance_wrap(self):
        self.assertIsInstance(self.wall, rpw.db.wall.Wall)
        self.assertIsInstance(self.wall.unwrap(), DB.Wall)

    def test_wall_factory(self):
        wrapped = rpw.db.Element.Factory(self.wall.unwrap())
        self.assertIsInstance(wrapped, rpw.db.wall.Wall)
        wrapped = rpw.db.Element.Factory(self.wall.symbol.unwrap())
        self.assertIsInstance(wrapped, rpw.db.wall.WallType)
        # TODO: MOVE THESE > No Longer Element
        wrapped = rpw.db.WallKind(self.wall.family.unwrap())
        self.assertIsInstance(wrapped, rpw.db.WallKind)

    def test_wall_instance_symbol(self):
        wall_symbol = self.wall.symbol
        self.assertIsInstance(wall_symbol, rpw.db.wall.WallType)
        self.assertIsInstance(wall_symbol.unwrap(), DB.WallType)
        self.assertEqual(wall_symbol.name, 'Wall 1')
        self.assertEqual(len(wall_symbol.instances), 1)
        self.assertEqual(len(wall_symbol.siblings), 2)

    def test_wall_instance_family(self):
        wall_family = self.wall.family
        self.assertIsInstance(wall_family, rpw.db.wall.WallKind)
        self.assertEqual(wall_family.unwrap(), DB.WallKind.Basic)
        self.assertEqual(wall_family.name, 'Basic')
        self.assertEqual(len(wall_family.instances), 1)
        self.assertEqual(len(wall_family.symbols), 2)

    def test_wall_instance_category(self):
        wall_category = self.wall.category
        self.assertIsInstance(wall_category, rpw.db.wall.WallCategory)
        self.assertIsInstance(wall_category.unwrap(), DB.Category)
        self.assertEqual(wall_category.name, 'Walls')

    def test_wall_instance_category(self):
        wall_category = self.wall.category
        self.assertIsInstance(wall_category, rpw.db.wall.WallCategory)
        self.assertIsInstance(wall_category.unwrap(), DB.Category)
        self.assertEqual(wall_category.name, 'Walls')

    def test_wall_change_type_by_name(self):
        wall = self.wall
        with rpw.db.Transaction():
            wall.change_type('Wall 2')
        self.assertEqual(wall.wall_type.name, 'Wall 2')

    def test_wall_change_type(self):
        wall = self.wall
        wall_type = rpw.db.Collector(of_class='WallType', where=lambda w: w.name == 'Wall 2').get_first(wrapped=False)
        with rpw.db.Transaction():
            wall.change_type('Wall 2')
        self.assertEqual(wall.wall_type.name, 'Wall 2')

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
        room = rpw.db.Collector(os_category='OST_Rooms', is_not_type=True).get_first(wrapped=False)
        self.wall = rpw.db.wall.Wall(wall)
    #
    # def test_wall_instance_wrap(self):
    #     self.assertIsInstance(self.wall, rpw.db.wall.Wall)
    #     self.assertIsInstance(self.wall.unwrap(), DB.Wall)



def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)



if __name__ == '__main__':
    run()
