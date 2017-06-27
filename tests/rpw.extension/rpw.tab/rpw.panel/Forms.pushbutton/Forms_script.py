""" Revit Python Wrapper Tests - Forms

Passes:
2017

"""

import sys
import unittest
import os

test_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(test_dir)
sys.path.append(root_dir)

import rpw
from rpw import revit, DB, UI
doc, uidoc = rpw.revit.doc, rpw.revit.uidoc

from rpw.utils.dotnet import List
from rpw.exceptions import RpwParameterNotFound, RpwWrongStorageType
from rpw.utils.logger import logger

data = ['A', 'B', 'C']

######################
# FORMS
######################


class FormSelectFromListTests(unittest.TestCase):

    def test_get_value(self):
        value = rpw.ui.forms.SelectFromList('Select From List Test', data,
                                        description='Select A and click select',
                                        exit_on_close=False)
        self.assertEqual(value, 'A')

    def test_get_dict_value(self):
        value = rpw.ui.forms.SelectFromList('Select From List Test', {'A':10},
                                            description='Select A and click select',
                                            exit_on_close=False)
        self.assertEqual(value, 10)

    def test_cancel(self):
        value = rpw.ui.forms.SelectFromList('Test Cancel', data,
                                        description='CLOSE WITHOUT SELECTING',
                                        exit_on_close=False)
        self.assertIsNone(value)

    def test_close_exit(self):
        with self.assertRaises(SystemExit):
            rpw.ui.forms.SelectFromList('Text Exit on Close', data,
                                        description='CLOSE WITHOUT SELECTING',
                                        exit_on_close=True)


class FormTextInputTests(unittest.TestCase):

    def test_get_value(self):
        value = rpw.ui.forms.TextInput('Text Input', default='A',
                                       description='select with letter A',
                                       exit_on_close=False)
        self.assertEqual(value, 'A')

    def test_cancel(self):
        value = rpw.ui.forms.TextInput('Test Cancel', default='A',
                                   description='CLOSE FORM',
                                   exit_on_close=False)
        self.assertIsNone(value)

    def test_close_exit(self):
        with self.assertRaises(SystemExit):
            rpw.ui.forms.TextInput('Test Exit on Close', default='A',
                                    description='CLOSE FORM',
                                    exit_on_close=True)

def run():
    # logger.verbose(False)
    unittest.main(verbosity=3, buffer=True)

if __name__ == '__main__':
    run()
