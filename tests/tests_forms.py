""" Revit Python Wrapper Tests

Passes:

    * Revit:
        * Revit 2015
        * Revit 2016
"""

import sys
import unittest
import os

test_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(test_dir)
sys.path.append(root_dir)

import rpw
from rpw import DB, UI, doc, uidoc, version
from rpw import List
from rpw.exceptions import RPW_ParameterNotFound, RPW_WrongStorageType
from rpw.logger import logger

data = ['A', 'B', 'C']

######################
# FORMS
######################

class FormSelectFromListTests(unittest.TestCase):

    def test_get_value(self):
        form = rpw.forms.SelectFromList('Select From List Test', data,
                                        description='Select A and click select')
        form_ok = form.show()
        self.assertTrue(form_ok)
        self.assertEqual(form.selected, 'A')

    def test_cancel(self):
        form = rpw.forms.SelectFromList('Test Cancel', data,
                                        description='CLOSE WITHOUT SELECTING')
        form_ok = form.show()
        self.assertFalse(form_ok)
        self.assertFalse(form.selected)

class FormTextInputTests(unittest.TestCase):

    def test_get_value(self):
        form = rpw.forms.TextInput('Text Input',default='A',
                                   description='select with letter A')
        form_ok = form.show()
        self.assertTrue(form_ok)
        self.assertEqual(form.selected, 'A')

    def test_cancel(self):
        form = rpw.forms.TextInput('Test Cancel', default='A',
                                   description='CLOSE FORM')
        form_ok = form.show()
        self.assertFalse(form_ok)
        self.assertFalse(form.selected)


if __name__ == '__main__':
    logger.verbose(False)
    # logger.disable()
    unittest.main(verbosity=3, buffer=True)
    # unittest.main(verbosity=0, buffer=True)
    # unittest.main(verbosity=0, defaultTest='ParameterFilterTests')
    # unittest.main(defaultTest='SelectionTests')
