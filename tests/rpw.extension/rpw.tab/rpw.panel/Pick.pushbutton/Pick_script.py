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
from rpw.ui import Selection

import test_utils

def setUpModule():
    logger.title('SETTING UP PICK TESTS...')

def tearDownModule():
    pass


######################
# SELECTION
######################


class PickTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING PICK...')
        test_utils.delete_all_walls()
        wall = test_utils.make_wall()
        cls.wall = wall

    @classmethod
    def tearDownClass(cls):
        test_utils.delete_all_walls()

    def setUp(self):
        self.wall = PickTests.wall
        Selection().clear()

    def tearDown(self):
        Selection().clear()
        logger.debug('SELECTION TEST PASSED')

    def test_pick_element(self):
        selection = Selection()
        desk = selection.pick_element('Pick a Desk')
        self.assertIsInstance(desk, DB.Reference)
        self.assertEqual(len(selection), 1)

    def test_pick_elements(self):
        selection = Selection()
        desks = selection.pick_element('Pick 2 Desks', multiple=True)
        self.assertIsInstance(desks[0], DB.Reference)
        self.assertEqual(len(selection), 2)

    def test_pick_elements(self):
        selection = Selection()
        desks = selection.pick_element('Pick 2 Desks', multiple=True)
        self.assertIsInstance(desks[0], DB.Reference)
        self.assertEqual(len(selection), 2)

    def test_pick_element_point(self):
        selection = Selection()
        rv = selection.pick_pt_on_element('pick_pt_on_element')
        self.assertIsInstance(rv, DB.Reference)
        rv = selection.pick_pt_on_element('pick_pt_on_element', multiple=True)
        self.assertIsInstance(rv[0], DB.Reference)

    def test_pick_element_edge(self):
        selection = Selection()
        rv = selection.pick_edge('pick_edge')
        self.assertIsInstance(rv, DB.Reference)
        rv = selection.pick_edge('pick_edges', multiple=True)
        self.assertIsInstance(rv[0], DB.Reference)

    def test_pick_element_face(self):
        selection = Selection()
        rv = selection.pick_face('pick_face')
        self.assertIsInstance(rv, DB.Reference)
        rv = selection.pick_face('pick_faces', multiple=True)
        self.assertIsInstance(rv[0], DB.Reference)

    def test_pick_pt(self):
        selection = Selection()
        rv = selection.pick_pt('pick_pt')
        self.assertIsInstance(rv, DB.XYZ)

    def test_pick_snaps(self):
        selection = Selection()
        rv = selection.pick_pt('pick_pt', snap='endpoints')
        self.assertIsInstance(rv, DB.XYZ)

    # def test_pick_linked(self):
    #     selection = Selection()
    #     rv = selection.pick_linked_element('pick_linked_element')
    #     rpw.ui.Console()



def run():
    logger.verbose(True)
    suite = unittest.TestLoader().discover('tests')
    unittest.main(verbosity=3, buffer=False)

if __name__ == '__main__':
    run()
