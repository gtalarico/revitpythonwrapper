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
from rpw.db import Element
from rpw.db import View, ViewPlan, ViewSection
from rpw.db import ViewSheet, ViewSchedule, View3D
from rpw.db import ViewFamilyType
from rpw.db import ViewType, ViewPlanType

from rpw.utils.logger import logger

# from rpw.utils.dotnet import List
# from rpw.exceptions import RpwParameterNotFound, RpwWrongStorageType

import test_utils

def setUpModule():
    logger.title('SETTING UP VIEW TESTS...')
    # test_utils.delete_all_walls()
    # test_utils.make_wall()

def tearDownModule():
    pass
    # test_utils.delete_all_walls()

class TestViewWrappers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING View Classes...')
        cls.view = DB.FilteredElementCollector(revit.doc).OfClass(DB.View).FirstElement()
        cls.view_plan = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewPlan).FirstElement()
        cls.view_sheet = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewSheet).FirstElement()
        cls.view_schedule = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewSchedule).FirstElement()
        cls.view_section = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewSection).FirstElement()
        cls.view_3d = DB.FilteredElementCollector(revit.doc).OfClass(DB.View3D).FirstElement()
        cls.view_family_type = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewFamilyType).FirstElement()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_view_wrapper(self):
        wrapped_view = Element(self.view)
        self.assertIsInstance(wrapped_view, View)
        wrapped_view = View(self.view)
        self.assertIsInstance(wrapped_view, View)

    def test_view_plan_wrapper(self):
        wrapped_view_plan = Element(self.view_plan)
        self.assertIsInstance(wrapped_view_plan, ViewPlan)
        wrapped_view_plan = ViewPlan(self.view_plan)
        self.assertIsInstance(wrapped_view_plan, ViewPlan)

    def test_view_section_wrapper(self):
        wrapped_view_section = Element(self.view_section)
        self.assertIsInstance(wrapped_view_section, ViewSection)
        wrapped_view_section = ViewSection(self.view_section)
        self.assertIsInstance(wrapped_view_section, ViewSection)

    def test_view_sheet_wrapper(self):
        wrapped_view_sheet = Element(self.view_sheet)
        self.assertIsInstance(wrapped_view_sheet, ViewSheet)
        wrapped_view_sheet = ViewSheet(self.view_sheet)
        self.assertIsInstance(wrapped_view_sheet, ViewSheet)

    def test_view_schedule_wrapper(self):
        wrapped_view_schedule = Element(self.view_schedule)
        self.assertIsInstance(wrapped_view_schedule, ViewSchedule)
        wrapped_view_schedule = ViewSchedule(self.view_schedule)
        self.assertIsInstance(wrapped_view_schedule, ViewSchedule)

    def test_view_3D(self):
        wrapped_view_3d = Element(self.view_3d)
        self.assertIsInstance(wrapped_view_3d, View3D)
        wrapped_view_3d = View3D(self.view_3d)
        self.assertIsInstance(wrapped_view_3d, View3D)

    def test_view_family_type(self):
        wrapped_view_family_type = Element(self.view_family_type)
        self.assertIsInstance(wrapped_view_family_type, ViewFamilyType)
        wrapped_view_family_type = ViewFamilyType(self.view_family_type)
        self.assertIsInstance(wrapped_view_family_type, ViewFamilyType)

class TestViewRelationships(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING View Classes...')
        cls.view = DB.FilteredElementCollector(revit.doc).OfClass(DB.View).FirstElement()
        cls.view_plan = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewPlan).FirstElement()
        cls.view_sheet = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewSheet).FirstElement()
        cls.view_schedule = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewSchedule).FirstElement()
        cls.view_section = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewSection).FirstElement()
        cls.view_3d = DB.FilteredElementCollector(revit.doc).OfClass(DB.View3D).FirstElement()
        cls.view_family_type = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewFamilyType).FirstElement()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_view_type(self):
        wrapped_view = Element(self.view_3d)
        view_type = wrapped_view.view_type
        self.assertIsInstance(view_type, DB.ViewType)
        self.assertEqual(view_type, DB.ViewType.ThreeD)

    def test_view_plan_level(self):
        wrapped_view = Element(self.view_plan)
        level = wrapped_view.level
        self.assertIsInstance(level, DB.Level)

    def test_view_family_type(self):
        wrapped_view = Element(self.view_3d)
        view_type = wrapped_view.view_family_type
        self.assertIsInstance(view_type.unwrap(), DB.ViewFamilyType)


def run():
    logger.verbose(True)
    suite = unittest.TestLoader().discover('tests')
    unittest.main(verbosity=3, buffer=True)



if __name__ == '__main__':
    run()
