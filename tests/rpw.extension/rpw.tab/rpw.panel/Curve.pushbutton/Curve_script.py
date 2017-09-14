"""
Curve Tests

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
from rpw import revit, DB, UI, db

doc, uidoc = revit.doc, revit.uidoc

from rpw.db.xyz import XYZ
from rpw.exceptions import RpwParameterNotFound, RpwWrongStorageType
from rpw.utils.logger import logger


def setUpModule():
    logger.title('SETTING UP Curve TESTS...')

def tearDownModule():
    pass

class Line(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING Line...')
        pt1 = DB.XYZ(0,0,0)
        pt2 = DB.XYZ(10,10,0)
        cls.Line = DB.Line.CreateBound(pt1, pt2)
        cls.line = db.Line.new(pt1, pt2)

    def test_line(self):
        Line, line = self.Line, self.line
        self.assertIsInstance(line.unwrap(), DB.Line)
        self.assertTrue(Line.GetEndPoint(1).IsAlmostEqualTo(line.end_point.unwrap()))

    def test_line_start_point(self):
        Line, line = self.Line, self.line
        self.assertTrue(Line.GetEndPoint(0).IsAlmostEqualTo(line.start_point.unwrap()))

    def test_line_end_point(self):
        Line, line = self.Line, self.line
        self.assertTrue(Line.GetEndPoint(1).IsAlmostEqualTo(line.end_point.unwrap()))

    def test_line_end_point(self):
        Line, line = self.Line, self.line
        self.assertTrue(Line.GetEndPoint(0.5).IsAlmostEqualTo(line.mid_point.unwrap()))

    def test_line_end_points(self):
        Line, line = self.Line, self.line
        self.assertIsInstance(line.end_points, tuple)
        self.assertTrue(Line.GetEndPoint(0).IsAlmostEqualTo(line.end_points[0].unwrap()))


class Ellipse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING Line...')
        pt1 = DB.XYZ(0,0,0)
        pt2 = DB.XYZ(10,10,0)
        cls.Line = DB.Line.CreateBound(pt1, pt2)
        cls.line = db.Line.new(pt1, pt2)

    # def test_line(self):
    #     Line, line = self.Line, self.line
    #     self.assertIsInstance(line.unwrap(), DB.Line)
    #     self.assertTrue(Line.GetEndPoint(1).IsAlmostEqualTo(line.end_point.unwrap()))
    #
    # def test_line_start_point(self):
    #     Line, line = self.Line, self.line
    #     self.assertTrue(Line.GetEndPoint(0).IsAlmostEqualTo(line.start_point.unwrap()))
    #
    # def test_line_end_point(self):
    #     Line, line = self.Line, self.line
    #     self.assertTrue(Line.GetEndPoint(1).IsAlmostEqualTo(line.end_point.unwrap()))
    #
    # def test_line_end_point(self):
    #     Line, line = self.Line, self.line
    #     self.assertTrue(Line.GetEndPoint(0.5).IsAlmostEqualTo(line.mid_point.unwrap()))
    #
    # def test_line_end_points(self):
    #     Line, line = self.Line, self.line
    #     self.assertIsInstance(line.end_points, tuple)
    #     self.assertTrue(Line.GetEndPoint(0).IsAlmostEqualTo(line.end_points[0].unwrap()))


class CurveCreate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING Curve Create...')

    def setUp(self):
        line = db.Line.new([0,0], [10,10])
        with rpw.db.Transaction():
            self.detail_line = line.create_detail()

    def tearDown(self):
        with rpw.db.Transaction():
            revit.doc.Delete(self.detail_line.Id)

    def test_detail_line(self):
        self.assertIsInstance(self.detail_line, DB.DetailLine)
        curve = self.detail_line.GeometryCurve
        self.assertTrue(curve.GetEndPoint(1).IsAlmostEqualTo(DB.XYZ(10,10,0)))


def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)

if __name__ == '__main__':
    run()
