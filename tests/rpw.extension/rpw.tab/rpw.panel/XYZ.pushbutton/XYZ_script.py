"""
XYZ Tests

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

from rpw.db.xyz import XYZ
from rpw.exceptions import RpwParameterNotFound, RpwWrongStorageType
from rpw.utils.logger import logger

# import test_utils

def setUpModule():
    logger.title('SETTING UP COLLECTION TESTS...')

def tearDownModule():
    pass
    # test_utils.delete_all_walls()

######################
# XYZTests
######################

class XYZInitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING XYZ...')

    def test_xyz_from_2args(self):
        pt = XYZ(2,4)
        self.assertEqual(pt.X, 2)
        self.assertEqual(pt.Y, 4)
        self.assertEqual(pt.Z, 0)

    def test_xyz_from_3args(self):
        pt = XYZ(2,4,6)
        self.assertEqual(pt.X, 2)
        self.assertEqual(pt.Y, 4)
        self.assertEqual(pt.Z, 6)

    def test_xyz_from_tuple2(self):
        pt = XYZ([2,4])
        self.assertEqual(pt.X, 2)
        self.assertEqual(pt.Y, 4)
        self.assertEqual(pt.Z, 0)

    def test_xyz_from_tuple3(self):
        pt = XYZ([2,4,6])
        self.assertEqual(pt.X, 2)
        self.assertEqual(pt.Y, 4)
        self.assertEqual(pt.Z, 6)

    def test_xyz_from_DB_XYZ(self):
        pt = XYZ(DB.XYZ(2,4,6))
        self.assertEqual(pt.X, 2)
        self.assertEqual(pt.Y, 4)
        self.assertEqual(pt.Z, 6)

    def test_xyz_from_XYZ(self):
        pt = XYZ(XYZ(2,4,6))
        self.assertEqual(pt.X, 2)
        self.assertEqual(pt.Y, 4)
        self.assertEqual(pt.Z, 6)

class XYZUsageTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING XYZ Usage...')
        cls.pt = XYZ(1,2,3)
        cls.pt2 = XYZ(4,5,6)

    def test_xyz_get_properties(self):
        pt = XYZ(1,2,3)
        self.assertEqual(pt.x, 1)
        self.assertEqual(pt.y, 2)
        self.assertEqual(pt.z, 3)

    def test_xyz_set_properties(self):
        pt = XYZ(1,2,3)
        pt.x = 5
        pt.y = 6
        pt.z = 7
        self.assertEqual(pt.x, 5)
        self.assertEqual(pt.y, 6)
        self.assertEqual(pt.z, 7)

    def test_xyz_at_z(self):
        pt = XYZ(1,2,3).at_z(10)
        self.assertEqual(pt.z, 10)

    def test_xyz_as_tuple(self):
        pt_tuple = XYZ(1,2,3).as_tuple
        self.assertEqual(pt_tuple, (1,2,3))
        self.assertIsInstance(pt_tuple, tuple)

    def test_xyz_as_dict(self):
        pt_dict = XYZ(1,2,3).as_dict
        self.assertIsInstance(pt_dict, dict)
        self.assertEqual(pt_dict, {'x':1, 'y':2, 'z':3})

    def test_xyz_repr(self):
        self.assertIn('<rpw:XYZ', XYZ(0,0,0).__repr__())

    def test_xyz_add(self):
        pt = XYZ(1,2,3) + XYZ(4,5,6)
        self.assertEqual(pt.x, 5)
        self.assertEqual(pt.y, 7)
        self.assertEqual(pt.z, 9)

    def test_xyz_sub(self):
        pt = XYZ(1,2,3) - XYZ(1,1,1)
        self.assertEqual(pt.x, 0)
        self.assertEqual(pt.y, 1)
        self.assertEqual(pt.z, 2)

    def test_xyz_mul(self):
        pt = XYZ(1,2,3) * 2
        self.assertEqual(pt.x, 2)
        self.assertEqual(pt.y, 4)
        self.assertEqual(pt.z, 6)

    def test_xyz_eq(self):
        self.assertEqual(XYZ(1,2,3), XYZ(1,2,3))
        self.assertNotEqual(XYZ(1,2,3), XYZ(2,2,3))

    def test_xyz_rotate_90(self):
        pt = XYZ(1,0,0)
        rotate_pt = (0,1,0)
        self.assertEqual(pt.rotate(90), rotate_pt)

    def test_xyz_rotate_180(self):
        pt = XYZ(1,0,0)
        rotate_pt = (-1,0,0)
        self.assertEqual(pt.rotate(180), rotate_pt)

    def test_xyz_rotate_radians(self):
        import math
        pt = XYZ(1,0,0)
        rotate_pt = (-1,0,0)
        self.assertEqual(pt.rotate(math.pi, radians=True), rotate_pt)

    def test_xyz_rotate_radians(self):
        import math
        pt = XYZ(1,0,0)
        rotate_pt = (-1,0,0)
        self.assertEqual(pt.rotate(math.pi, radians=True), rotate_pt)

    def test_xyz_rotate_axis(self):
        import math
        pt = XYZ(1,0,0)
        axis = XYZ(0,-1,0)
        rotate_pt = (0,0,1)
        self.assertEqual(pt.rotate(90, axis=axis), rotate_pt)


def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)

if __name__ == '__main__':
    run()
