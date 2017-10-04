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
from rpw.db.xyz import XYZ
from rpw.exceptions import RpwParameterNotFound, RpwWrongStorageType
from rpw.utils.logger import logger

import test_utils

def setUpModule():
    logger.title('SETTING UP COLLECTION TESTS...')

def tearDownModule():
    test_utils.delete_all_walls()

######################
# ElementSet
######################

class ElementSetTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING ElementSetTests...')
        collector = DB.FilteredElementCollector(doc)
        cls.views = collector.OfClass(DB.View).ToElements()

    # def setUp(self):
        # self.collector_helper = CollectorTests.collector_helper


    def test_element_set_element_add(self):
        rv = rpw.db.ElementSet()
        rv.add(self.views)
        self.assertEqual(len(rv), len(self.views))

    def test_element_set_unique(self):
        rv = rpw.db.ElementSet()
        rv.add(self.views)
        rv.add(self.views)
        self.assertEqual(len(rv), len(self.views))

    def test_element_set_init__bool(self):
        x = rpw.db.ElementSet(self.views)
        self.assertTrue(x)

    def test_element_set_elements(self):
        x = rpw.db.ElementSet(self.views)
        self.assertIsInstance(x.elements[0], DB.View)

    def test_element_set_element_ids(self):
        x = rpw.db.ElementSet(self.views)
        self.assertIsInstance(x.element_ids[0], DB.ElementId)

    def test_element_set_len(self):
        rv = len(rpw.db.ElementSet(self.views))
        self.assertGreater(rv, 2)

    def test_element_set_element_clear(self):
        rv = rpw.db.ElementSet(self.views)
        rv.clear()
        self.assertEqual(len(rv), 0)

    def test_element_set_as_element_list(self):
        rv = rpw.db.ElementSet(self.views)
        l = rv.as_element_list
        self.assertTrue(hasattr(l, 'Count'))
        self.assertEqual(len(l), len(self.views))

    def test_element_set_as_element_id_list(self):
        rv = rpw.db.ElementSet(self.views)
        l = rv.as_element_id_list
        self.assertTrue(hasattr(l, 'Count'))
        self.assertEqual(len(l), len(self.views))

    def test_element_set_select(self):
        rv = rpw.db.ElementSet(self.views)
        rv.select()

    def test_element_set_get_item(self):
        rv = rpw.db.ElementSet(self.views)
        key = self.views[0]
        self.assertIsInstance(rv[key].unwrap(), DB.View)

    def test_element_set_iter(self):
        rv = rpw.db.ElementSet(self.views)
        self.assertTrue(all([isinstance(v.unwrap(), DB.View) for v in rv]))

    def test_element_set_pop(self):
        rv = rpw.db.ElementSet(self.views)
        id_ = self.views[0].Id
        poped = rv.pop(id_)
        self.assertNotIn(id_, rv)
        self.assertEqual(poped.Id, id_)
        self.assertIsInstance(poped.unwrap(), DB.View)

    def test_element_set_wrapped_elements(self):
        rv = rpw.db.ElementSet(self.views).wrapped_elements
        self.assertIsInstance(rv[0], rpw.db.Element)



######################
# ElementCollection
######################

class ElementCollectionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING ElementCollection...')
        collector = DB.FilteredElementCollector(doc)
        cls.views = collector.OfClass(DB.View).ToElements()

    def test_element_collection_element_add(self):
        rv = rpw.db.ElementCollection()
        rv.append(self.views)
        self.assertEqual(len(rv), len(self.views))

    def test_element_collection_unique(self):
        rv = rpw.db.ElementCollection()
        rv.append(self.views)
        rv.append(self.views)
        self.assertEqual(len(rv), len(self.views)*2)

    def test_element_collection_init__bool(self):
        x = rpw.db.ElementCollection(self.views)
        self.assertTrue(x)

    def test_element_collection_elements(self):
        x = rpw.db.ElementCollection(self.views)
        self.assertIsInstance(x.elements[0].unwrap(), DB.View)

    def test_element_collection_element_ids(self):
        x = rpw.db.ElementCollection(self.views)
        self.assertIsInstance(x.element_ids[0], DB.ElementId)

    def test_element_collection_len(self):
        rv = len(rpw.db.ElementCollection(self.views))
        self.assertGreater(rv, 2)

    def test_element_collection_element_clear(self):
        rv = rpw.db.ElementCollection(self.views)
        rv.clear()
        self.assertEqual(len(rv), 0)

    def test_element_collection_as_element_list(self):
        rv = rpw.db.ElementCollection(self.views)
        l = rv.as_element_list
        self.assertTrue(hasattr(l, 'Count'))
        self.assertEqual(len(l), len(self.views))

    def test_element_collection_as_element_id_list(self):
        rv = rpw.db.ElementCollection(self.views)
        l = rv.as_element_id_list
        self.assertTrue(hasattr(l, 'Count'))
        self.assertEqual(len(l), len(self.views))

    def test_element_collection_select(self):
        rv = rpw.db.ElementCollection(self.views)
        rv.select()

    def test_element_collection_first(self):
        rv = rpw.db.ElementCollection(self.views)
        self.assertEqual(rv.get_first(wrapped=False).Id, self.views[0].Id)

    def test_element_collection_get_item(self):
        rv = rpw.db.ElementCollection(self.views)
        self.assertIsInstance(rv[0].unwrap(), DB.View)

    def test_element_collection_iter(self):
        rv = rpw.db.ElementCollection(self.views)
        self.assertTrue(all([isinstance(v.unwrap(), DB.View) for v in rv]))

    def test_element_collection_pop(self):
        col = rpw.db.ElementCollection(self.views)
        size = len(col)
        e = col.pop(0, wrapped=False)

        self.assertIsInstance(e, DB.View)
        self.assertEqual(len(col), size - 1)

    def test_element_collection_wrapped_elements(self):
        rv = rpw.db.ElementSet(self.views).wrapped_elements
        self.assertIsInstance(rv[0], rpw.db.Element)


######################
# XYZCollection
######################

class XyzCollectionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING XYZ Collection...')
        cls.points = [XYZ(0,0,0), XYZ(10,10,0), XYZ(5,5,0)]

    def test_xyz_add_len(self):
        xyz_collection = rpw.db.XyzCollection(self.points)
        self.assertEqual(len(xyz_collection), 3)

    def test_xyz_max(self):
        xyz_collection = rpw.db.XyzCollection(self.points)
        mx = xyz_collection.max
        self.assertEqual(mx, XYZ(10,10,0))

    def test_xyz_min(self):
        xyz_collection = rpw.db.XyzCollection(self.points)
        mn = xyz_collection.min
        self.assertEqual(mn, XYZ(0,0,0))

    def test_xyz_average(self):
        xyz_collection = rpw.db.XyzCollection(self.points)
        av = xyz_collection.average
        self.assertEqual(av, XYZ(5,5,0))

    def test_xyz_sorted_by(self):
        xyz_collection = rpw.db.XyzCollection(self.points)
        rv = xyz_collection.sorted_by('x')
        self.assertEqual(rv[0], XYZ(0,0,0))
        self.assertEqual(rv[1], XYZ(5,5,0))
        self.assertEqual(rv[2], XYZ(10,10,0))


def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)



if __name__ == '__main__':
    run()
