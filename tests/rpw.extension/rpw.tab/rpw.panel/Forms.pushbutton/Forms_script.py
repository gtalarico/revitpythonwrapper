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
from rpw import DB, UI, doc, uidoc, version
from rpw import List
from rpw.exceptions import RPW_ParameterNotFound, RPW_WrongStorageType
from rpw.utils.logger import logger

data = ['A', 'B', 'C']

######################
# FORMS
######################


class FormSelectFromListTests(unittest.TestCase):

    def test_get_value(self):
        form = rpw.forms.SelectFromList('Select From List Test', data,
                                        description='Select A and click select',
                                        exit_on_close=False)
        form_ok = form.show()
        self.assertTrue(form_ok)
        self.assertEqual(form.selected, 'A')

    def test_get_dict_value(self):
        form = rpw.forms.SelectFromList('Select From List Test', {'A':10},
                                        description='Select A and click select',
                                        exit_on_close=False)
        form_ok = form.show()
        self.assertTrue(form_ok)
        self.assertEqual(form.selected, 10)

    def test_cancel(self):
        form = rpw.forms.SelectFromList('Test Cancel', data,
                                        description='CLOSE WITHOUT SELECTING',
                                        exit_on_close=False)
        form_ok = form.show()
        self.assertFalse(form_ok)
        self.assertFalse(form.selected)

    def test_close_exit(self):
        form = rpw.forms.SelectFromList('Text Exit on Close', data,
                                        description='CLOSE WITHOUT SELECTING',
                                        exit_on_close=True)

        with self.assertRaises(SystemExit):
            form_ok = form.show()


class FormTextInputTests(unittest.TestCase):

    def test_get_value(self):
        form = rpw.forms.TextInput('Text Input', default='A',
                                   description='select with letter A',
                                   exit_on_close=False)
        form_ok = form.show()
        self.assertTrue(form_ok)
        self.assertEqual(form.selected, 'A')

    def test_cancel(self):
        form = rpw.forms.TextInput('Test Cancel', default='A',
                                   description='CLOSE FORM',
                                   exit_on_close=False)
        form_ok = form.show()
        self.assertFalse(form_ok)
        self.assertFalse(form.selected)

    def test_close_exit(self):
        form = rpw.forms.TextInput('Test Exit on Close', default='A',
                                   description='CLOSE FORM',
                                   exit_on_close=True)
        with self.assertRaises(SystemExit):
            form_ok = form.show()

def run():
    # logger.verbose(False)
    unittest.main(verbosity=3, buffer=True)

if __name__ == '__main__':
    run()
