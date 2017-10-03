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
        self.assertIsInstance(view_type.unwrap(), DB.ViewType)
        self.assertEqual(view_type.unwrap(), DB.ViewType.ThreeD)
        self.assertEqual(view_type.name, 'ThreeD')

    def test_view_plan_level(self):
        wrapped_view = Element(self.view_plan)
        level = wrapped_view.level
        self.assertIsInstance(level, DB.Level)

    def test_view_family_type(self):
        wrapped_view = Element(self.view_3d)
        view_type = wrapped_view.view_family_type
        self.assertIsInstance(view_type.unwrap(), DB.ViewFamilyType)

    def test_view_family(self):
        wrapped_view = Element(self.view_3d)
        view_family = wrapped_view.view_family
        self.assertIsInstance(view_family.unwrap(), DB.ViewFamily)

    def test_view_type_aggregator(self):
        wrapped_view_plan = Element(self.view_plan)
        same_view_type_views = wrapped_view_plan.view_type.views
        for view in same_view_type_views:
            self.assertEqual(view.view_type.unwrap(), wrapped_view_plan.view_type.unwrap())

    def test_view_family_aggregator(self):
        wrapped_view_plan = Element(self.view_plan)
        same_family_views = wrapped_view_plan.view_family.views
        for view in same_family_views:
            self.assertEqual(view.view_family.unwrap(), wrapped_view_plan.view_family.unwrap())

    def test_view_family_aggregator(self):
        wrapped_view_plan = Element(self.view_plan)
        same_view_family_type_views = wrapped_view_plan.view_family_type.views
        for view in same_view_family_type_views:
            self.assertEqual(view.view_family_type.unwrap(), wrapped_view_plan.view_family_type.unwrap())

    def test_view_family_type_name(self):
        wrapped_view = rpw.db.ViewPlan.collect(where=lambda x: x.view_family_type.name == 'Floor Plan').wrapped_elements[0]
        self.assertEqual(wrapped_view.view_family_type.name, 'Floor Plan')

    # def test_view_family_type_name_get_setter(self):
    #     wrapped_view = rpw.db.ViewPlan.collect(where=lambda x: x.view_family_type.name == 'My Floor Plan').wrapped_elements[0]
    #     # self.assertEqual(wrapped_view.view_family_type.name, 'My Floor Plan')
    #     with rpw.db.Transaction('Set Name'):
    #         wrapped_view.view_family_type.name = 'ABC'
    #     self.assertEqual(wrapped_view.view_family_type.name, 'ABC')
        # with rpw.db.Transaction('Set Name'):
            # wrapped_view.view_family_type.name = 'My Floor Plan'
        # rpw.ui.forms.Console()

class TestViewOverrides(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING View Classes...')
        cls.view_plan = revit.active_view.unwrap()
        # cls.view_plan = DB.FilteredElementCollector(revit.doc).OfClass(DB.ViewPlan).FirstElement()
        cls.wrapped_view = revit.active_view
        cls.element = DB.FilteredElementCollector(revit.doc).OfClass(DB.FamilyInstance).WhereElementIsNotElementType().FirstElement()

        linepattern = rpw.db.Collector(of_class='LinePatternElement', where=lambda x: x.Name == 'Dash').get_first()
        cls.line_pattern_id = linepattern.Id
        fillpattern = rpw.db.Collector(of_class='FillPatternElement', where=lambda x: x.Name == 'Horizontal').get_first()
        cls.fillpattern_id = fillpattern.Id

    def tearDown(cls):
        """ Resets Element after each test """
        with rpw.db.Transaction():
            cls.view_plan.SetElementOverrides(cls.element.Id, DB.OverrideGraphicSettings())

    def test_match(self):
        e1 = DB.FilteredElementCollector(revit.doc).OfClass(DB.FamilyInstance).WhereElementIsNotElementType().ToElements()[0]
        e2 = DB.FilteredElementCollector(revit.doc).OfClass(DB.FamilyInstance).WhereElementIsNotElementType().ToElements()[1]
        o = DB.OverrideGraphicSettings()
        o.SetHalftone(True)
        o.SetSurfaceTransparency(30)
        with rpw.db.Transaction():
            self.view_plan.SetElementOverrides(e1.Id, o)

        with rpw.db.Transaction():
            self.wrapped_view.override.match_element(e2, e1)
        rv = self.view_plan.GetElementOverrides(e2.Id)
        self.assertTrue(rv.Halftone)
        self.assertEqual(rv.Transparency, 30)

    def test_halftone(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.halftone(self.element, True)
        rv = self.view_plan.GetElementOverrides(self.element.Id)
        self.assertTrue(rv.Halftone)

    def test_halftone(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.halftone(self.element, True)
        rv = self.view_plan.GetElementOverrides(self.element.Id)
        self.assertTrue(rv.Halftone)

    def test_transparency(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.transparency(self.element, 40)
        rv = self.view_plan.GetElementOverrides(self.element.Id)
        self.assertEqual(rv.Transparency, 40)

    def test_detail_level_by_enum(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.detail_level(self.element, DB.ViewDetailLevel.Fine)
        rv = self.view_plan.GetElementOverrides(self.element.Id)
        self.assertEqual(rv.DetailLevel, DB.ViewDetailLevel.Fine)

    def test_detail_level_by_name(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.detail_level(self.element, 'Fine')
        rv = self.view_plan.GetElementOverrides(self.element.Id)
        self.assertEqual(rv.DetailLevel, DB.ViewDetailLevel.Fine)

    def test_projection_line(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.projection_line(self.element,
                                                       color=(0,120,255),
                                                       weight=5,
                                                       pattern=self.line_pattern_id)

        rv = self.view_plan.GetElementOverrides(self.element.Id)
        self.assertEqual(rv.ProjectionLineColor.Red, 0)
        self.assertEqual(rv.ProjectionLineColor.Green, 120)
        self.assertEqual(rv.ProjectionLineColor.Blue, 255)
        self.assertEqual(rv.ProjectionLineWeight, 5)
        self.assertEqual(rv.ProjectionLinePatternId, self.line_pattern_id)

    def test_projection_line_pattern_by_name(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.projection_line(self.element, pattern='Dash')
            rv = self.view_plan.GetElementOverrides(self.element.Id)
            self.assertEqual(rv.ProjectionLinePatternId, self.line_pattern_id)

    def test_cut_line(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.cut_line(self.element,
                                                color=(0,80,150),
                                                weight=7,
                                                pattern=self.line_pattern_id)

        rv = self.view_plan.GetElementOverrides(self.element.Id)
        self.assertEqual(rv.CutLineColor.Red, 0)
        self.assertEqual(rv.CutLineColor.Green, 80)
        self.assertEqual(rv.CutLineColor.Blue, 150)
        self.assertEqual(rv.CutLineWeight, 7)
        self.assertEqual(rv.CutLinePatternId, self.line_pattern_id)

    def test_cut_line_pattern_by_name(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.cut_line(self.element, pattern='Dash')
            rv = self.view_plan.GetElementOverrides(self.element.Id)
            self.assertEqual(rv.CutLinePatternId, self.line_pattern_id)

    def test_projection_fill(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.projection_fill(self.element,
                                                       color=(0,40,190),
                                                       pattern=self.fillpattern_id,
                                                       visible=False)

        rv = self.view_plan.GetElementOverrides(self.element.Id)
        self.assertEqual(rv.ProjectionFillColor.Red, 0)
        self.assertEqual(rv.ProjectionFillColor.Green, 40)
        self.assertEqual(rv.ProjectionFillColor.Blue, 190)
        self.assertEqual(rv.IsProjectionFillPatternVisible, False)
        self.assertEqual(rv.ProjectionFillPatternId, self.fillpattern_id)

    def test_projection_fill_pattern_by_name(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.projection_fill(self.element, pattern='Horizontal')
            rv = self.view_plan.GetElementOverrides(self.element.Id)
            self.assertEqual(rv.ProjectionFillPatternId, self.fillpattern_id)

    def test_cut_fill(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.cut_fill(self.element,
                                                color=(0,30,200),
                                                pattern=self.fillpattern_id,
                                                visible=False)

        rv = self.view_plan.GetElementOverrides(self.element.Id)
        self.assertEqual(rv.CutFillColor.Red, 0)
        self.assertEqual(rv.CutFillColor.Green, 30)
        self.assertEqual(rv.CutFillColor.Blue, 200)
        self.assertEqual(rv.IsCutFillPatternVisible, False)
        self.assertEqual(rv.CutFillPatternId, self.fillpattern_id)


    def test_cut_fill_pattern_by_name(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.cut_fill(self.element, pattern='Horizontal')
            rv = self.view_plan.GetElementOverrides(self.element.Id)
            self.assertEqual(rv.CutFillPatternId, self.fillpattern_id)

    def test_halftone_category(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.halftone('Furniture', True)
        rv = self.view_plan.GetCategoryOverrides(DB.ElementId(DB.BuiltInCategory.OST_Furniture))
        self.assertTrue(rv.Halftone)

    def test_halftone_category_bi(self):
        with rpw.db.Transaction():
            self.wrapped_view.override.halftone(DB.BuiltInCategory.OST_Furniture, True)
        rv = self.view_plan.GetCategoryOverrides(DB.ElementId(DB.BuiltInCategory.OST_Furniture))
        self.assertTrue(rv.Halftone)


def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)



if __name__ == '__main__':
    run()
