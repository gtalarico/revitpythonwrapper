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
from rpw.ui.selection import Pick
from rpw.db.reference import Reference
from rpw.db.xyz import XYZ
from rpw.db.element import Element

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
        # Pick().clear()

    def tearDown(self):
        # Pick().clear()
        logger.debug('SELECTION TEST PASSED')

    def test_pick_element(self):
        selection = Pick()
        desk = selection.pick_element('Pick a Desk')
        self.assertIsInstance(desk, Reference)

    def test_pick_elements(self):
        selection = Pick()
        desks = selection.pick_element('Pick 2 Desks', multiple=True)
        self.assertIsInstance(desks[0], Reference)

    def test_pick_element_point(self):
        selection = Pick()
        rv = selection.pick_pt_on_element('pick_pt_on_element')
        self.assertIsInstance(rv, Reference)
        rv = selection.pick_pt_on_element('pick_pt_on_element', multiple=True)
        self.assertIsInstance(rv[0], Reference)

    def test_pick_element_edge(self):
        selection = Pick()
        rv = selection.pick_edge('pick_edge')
        self.assertIsInstance(rv, Reference)
        rv = selection.pick_edge('pick_edges', multiple=True)
        self.assertIsInstance(rv[0], Reference)

    def test_pick_element_face(self):
        selection = Pick()
        rv = selection.pick_face('pick_face')
        self.assertIsInstance(rv, Reference)
        rv = selection.pick_face('pick_faces', multiple=True)
        self.assertIsInstance(rv[0], Reference)

    def test_pick_pt(self):
        selection = Pick()
        rv = selection.pick_pt('pick_pt')
        self.assertIsInstance(rv, XYZ)

    def test_pick_snaps(self):
        selection = Pick()
        rv = selection.pick_pt('pick_pt', snap='endpoints')
        self.assertIsInstance(rv, XYZ)

    def test_pick_box(self):
        selection = Pick()
        rv = selection.pick_box('PickBox')
        self.assertIsInstance(rv[0], XYZ)

    def test_pick_by_rectangle(self):
        selection = Pick()
        rv = selection.pick_by_rectangle('Pick By Rectangle')
        self.assertIsInstance(rv[0], Element)

    # def test_pick_linked(self):
    #     selection = Pick()
    #     rv = selection.pick_linked_element('pick_linked_element')
    #     rpw.ui.Console()



def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=False)

if __name__ == '__main__':
    run()
