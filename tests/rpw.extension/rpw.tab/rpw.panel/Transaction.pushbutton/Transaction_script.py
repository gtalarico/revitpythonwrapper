"""
Transaction Tests

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
from rpw.utils.dotnet import List
from rpw.utils.logger import logger
doc = rpw.revit.doc

import test_utils

def setUpModule():
    logger.title('SETTING UP TRANSACTION TESTS...')

def tearDownModule():
    pass


class TransactionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.title('TESTING TRANSACTIONS...')
        test_utils.delete_all_walls()
        wall = test_utils.make_wall()
        cls.wall = wall

    @classmethod
    def tearDownClass(cls):
        test_utils.delete_all_walls()

    def setUp(self):
        wall = DB.FilteredElementCollector(doc).OfClass(DB.Wall).ToElements()[0]
        self.wall = rpw.db.Wall(wall)
        with rpw.db.Transaction('Reset Comment') as t:
            self.wall.parameters['Comments'] = ''

    def test_transaction_instance(self):
        with rpw.db.Transaction('Test Is Instance') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertIsInstance(t.unwrap(), DB.Transaction)

    def test_transaction_started(self):
        with rpw.db.Transaction('Has Started') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertTrue(t.HasStarted())

    def test_transaction_has_ended(self):
        with rpw.db.Transaction('Add Comment') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertFalse(t.HasEnded())

    def test_transaction_get_name(self):
        with rpw.db.Transaction('Named Transaction') as t:
            self.assertEqual(t.GetName(), 'Named Transaction')

    def test_transaction_commit_status_success(self):
        with rpw.db.Transaction('Set String') as t:
            self.wall.parameters['Comments'].value = ''
            self.assertEqual(t.GetStatus(), DB.TransactionStatus.Started)
        self.assertEqual(t.GetStatus(), DB.TransactionStatus.Committed)

    def test_transaction_commit_status_rollback(self):
        with self.assertRaises(Exception):
            with rpw.db.Transaction('Set String') as t:
                self.wall.parameters['Top Constraint'].value = DB.ElementId('a')
        self.assertEqual(t.GetStatus(), DB.TransactionStatus.RolledBack)

    def test_transaction_group(self):
        with rpw.db.TransactionGroup('Multiple Transactions') as tg:
            self.assertEqual(tg.GetStatus(), DB.TransactionStatus.Started)
            with rpw.db.Transaction('Set String') as t:
                self.assertEqual(t.GetStatus(), DB.TransactionStatus.Started)
                self.wall.parameters['Comments'].value = '1'
            self.assertEqual(t.GetStatus(), DB.TransactionStatus.Committed)
        self.assertEqual(tg.GetStatus(), DB.TransactionStatus.Committed)

    def test_transaction_decorator(self):
        @rpw.db.Transaction.ensure('Transaction Name')
        def somefunction():
            param = self.wall.parameters['Comments'].value = '1'
            return param
        self.assertTrue(somefunction())


def run():
    # logger.verbose(False)
    logger.disable()
    suite = unittest.TestLoader().discover(os.path.dirname(__file__))
    unittest.main(verbosity=3, buffer=True)



if __name__ == '__main__':
    run()
