"""
Selection Tests

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
from rpw import DB, UI
doc, uidoc = rpw.revit.doc, rpw.revit.uidoc
from rpw.utils.logger import logger

import test_utils

def setUpModule():
    logger.title('SETTING UP SELECTION TESTS...')
    # uidoc.Application.OpenAndActivateDocument(os.path.join(panel_dir, 'collector.rvt'))

def tearDownModule():
    pass


######################
# SELECTION
######################


class SelectionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING SELECTION...')
        test_utils.delete_all_walls()
        wall = test_utils.make_wall()
        cls.wall = wall

    @classmethod
    def tearDownClass(cls):
        test_utils.delete_all_walls()

    def setUp(self):
        self.wall = SelectionTests.wall
        self.selection = rpw.ui.Selection([self.wall.Id])

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
        wall = self.selection.get_elements(wrapped=False)[0]
        self.assertIsInstance(wall, DB.Wall)
        wall2 = self.selection.get_elements(wrapped=True)[0]
        self.assertTrue(hasattr(wall2, 'unwrap'))

    def test_selection_length(self):
        self.assertEqual(len(self.selection), 1)

    def test_selection_boolean(self):
        self.assertTrue(self.selection)

    def test_selection_boolean_false(self):
        self.selection.clear()
        self.assertFalse(self.selection)

    def test_selection_clear(self):
        self.selection.clear()
        self.assertEqual(len(self.selection), 0)
        self.selection = rpw.ui.Selection([self.wall.Id])

    def test_selection_add(self):
        selection = rpw.ui.Selection()
        selection.add([self.wall])
        wall = self.selection.get_elements(wrapped=False)[0]
        self.assertIsInstance(wall, DB.Wall)

    def test_selection_contains(self):
        selection = rpw.ui.Selection()
        selection.add([self.wall])
        self.assertIn(self.wall, selection)

    def test_selection_updates_does_not_lose(self):
        selection = rpw.ui.Selection([self.wall])
        selection2 = rpw.ui.Selection([self.wall])
        selection2.update()
        self.assertEqual(selection.elements[0].Id, selection2.elements[0].Id)

    def test_selection_update(self):
        selection = rpw.ui.Selection()
        selection.update()

def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)

if __name__ == '__main__':
    run()
