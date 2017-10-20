# coding: utf8

import sys
import unittest
import os

parent = os.path.dirname

script_dir = parent(__file__)
panel_dir = parent(script_dir)
sys.path.append(script_dir)

import rpw
from rpw import DB, revit
from rpw.utils.logger import logger
from rpw.db import Element
from rpw.db import FluidType


class TestFluidTypeWrapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.title('TESTING FluidType Wrapper...')
        cls.fluidtype = DB.FilteredElementCollector(revit.doc).OfClass(DB.Plumbing.FluidType).FirstElement()

    def test_fluidtype_wrapper(self):
        wrapped_fluidtype = Element(self.fluidtype)
        self.assertIsInstance(wrapped_fluidtype, FluidType)
        wrapped_fluidtype = FluidType(self.fluidtype)
        self.assertIsInstance(wrapped_fluidtype, FluidType)

def run():
    logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)


if __name__ == '__main__':
    run()
