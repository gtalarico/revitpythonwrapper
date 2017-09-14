"""
Globals

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


######################
# Globals
######################


class Globals(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import rpw

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_doc(self):
        from rpw import revit
        self.assertEqual(revit.doc.__class__.__name__, 'Document')

    def test_db(self):
        from rpw import revit, DB
        Wall = getattr(DB, 'Wall', None)
        self.assertIsInstance(Wall, type)

    def test_ui(self):
        from rpw import revit, UI
        TaskDialog = getattr(UI, 'TaskDialog', None)
        self.assertIsInstance(TaskDialog, type)

    def test_uidoc(self):
        from rpw import revit
        self.assertEqual(revit.uidoc.Application.__class__.__name__, 'UIApplication')

    def test_logger(self):
        from rpw.utils.logger import logger
        from rpw.utils.logger import LoggerWrapper
        self.assertIsInstance(logger, LoggerWrapper)

    #TODO: test version
    #TODO: test built



def run():
    # logger.verbose(False)
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)

if __name__ == '__main__':
    run()
