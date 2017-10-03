"""
Utils Tests

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
from rpw.exceptions import RpwParameterNotFound, RpwWrongStorageType
from rpw.utils.logger import logger

import test_utils

def setUpModule():
    logger.title('SETTING UP UTILS TESTS...')
    test_utils.delete_all_walls()
    test_utils.make_wall()

def tearDownModule():
    test_utils.delete_all_walls()

class CoerceTests(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        logger.title('TESTING COERCE FUNCITONS...')

    def setUp(self):
        self.wall = rpw.db.Collector(of_class='Wall').get_first(wrapped=False)

    def tearDown(self):
        pass

    def test_corce_into_id(self):
        id_ = rpw.utils.coerce.to_element_id(self.wall)
        self.assertIsInstance(id_, DB.ElementId)

    def test_corce_into_ids(self):
        ids = rpw.utils.coerce.to_element_ids([self.wall])
        all_id = all([isinstance(i, DB.ElementId) for i in ids])
        self.assertTrue(all_id)

    def test_corce_element_ref_int(self):
        element = rpw.utils.coerce.to_element(self.wall.Id.IntegerValue)
        self.assertIsInstance(element, DB.Element)

    def test_corce_element_ref_id(self):
        wall_id = DB.ElementId(self.wall.Id.IntegerValue)
        elements = rpw.utils.coerce.to_elements([wall_id])
        self.assertTrue(all([isinstance(e, DB.Element) for e in elements]))

    def test_corce_to_element_diverse(self):
        elements = rpw.utils.coerce.to_elements([self.wall, self.wall.Id, self.wall.Id.IntegerValue])
        self.assertTrue(all([isinstance(e, DB.Element) for e in elements]))

    def test_to_class_wall(self):
        self.assertIs(rpw.utils.coerce.to_class('Wall'), DB.Wall)

    def test_to_class_view(self):
        self.assertIs(rpw.utils.coerce.to_class('View'), DB.View)

    def test_to_category_walls(self):
        self.assertIs(rpw.utils.coerce.to_category('Walls'), DB.BuiltInCategory.OST_Walls)
        self.assertIs(rpw.utils.coerce.to_category('walls'), DB.BuiltInCategory.OST_Walls)
        self.assertIs(rpw.utils.coerce.to_category('ost_walls'), DB.BuiltInCategory.OST_Walls)

    def test_to_category_id_walls(self):
        self.assertEqual(rpw.utils.coerce.to_category_id('Walls'), DB.ElementId(DB.BuiltInCategory.OST_Walls))
        self.assertEqual(rpw.utils.coerce.to_category_id('walls'), DB.ElementId(DB.BuiltInCategory.OST_Walls))
        self.assertEqual(rpw.utils.coerce.to_category_id('ost_walls'), DB.ElementId(DB.BuiltInCategory.OST_Walls))

    def test_to_category_stacked_walls(self):
        self.assertIs(rpw.utils.coerce.to_category('ost_StackedWalls'), DB.BuiltInCategory.OST_StackedWalls)
        self.assertIs(rpw.utils.coerce.to_category('StackedWalls'), DB.BuiltInCategory.OST_StackedWalls)
        self.assertIs(rpw.utils.coerce.to_category('stackedwalls'), DB.BuiltInCategory.OST_StackedWalls)
        self.assertIs(rpw.utils.coerce.to_category('stacked walls'), DB.BuiltInCategory.OST_StackedWalls)

    def test_to_iterable(self):
        self.assertTrue([w for w in rpw.utils.coerce.to_iterable(self.wall)])

    def test_to_iterable_element_id(self):
        self.assertTrue([w for w in rpw.utils.coerce.to_element_ids(self.wall)])

    def test_to_iterable_element(self):
        self.assertTrue([w for w in rpw.utils.coerce.to_elements(self.wall)])


    # TODO: Add BuiltInCategory Tests
    # CATEGORY COERCE
    # >>> with rpw.db.Transaction():
    # ... 	rpw.revit.active_view.override.projection_line(BuiltInCategory.OST_Furniture, color=[255,0,255])
    # ...
    # >>> with rpw.db.Transaction():
    # ... 	rpw.revit.active_view.override.projection_line(ElementId(BuiltInCategory.OST_Furniture), color=[255,0,255])
    # ...
    # >>> with rpw.db.Transaction():
    # ... 	rpw.revit.active_view.override.projection_line(ElementId(BuiltInCategory.OST_Furniture), color=[255,0,120])
    # ...
    # >>>

def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)



if __name__ == '__main__':
    run()
