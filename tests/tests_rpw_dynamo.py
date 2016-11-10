""" Revit Python Wrapper Tests

Passes:

    * Revit:
        * Revit 2015
        * Revit 2016

    * Dynamo
        * 1.2

"""
import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import unittest
import traceback

rpw_module_path = IN[0]  # Path to RPW Module
if isinstance(rpw_module_path, list):
    sys.path = rpw_module_path
else:
    sys.path.insert(0, rpw_module_path)

from StringIO import StringIO
result = StringIO()
sys.stdout = result

print('IMPORT TESTS...')
from tests import tests_rpw
print('TESTS RUNNER: {}'.format(tests_rpw.__file__))

testsuite = unittest.TestLoader().loadTestsFromModule(tests_rpw)
test_result = unittest.TextTestRunner(verbosity=3, buffer=False).run(testsuite)

success = test_result.wasSuccessful()
ran = test_result.testsRun
failed = test_result.failures

print('Ran: {}'.format(ran))
print('Success: {}'.format(success))
print('Failed: {}'.format(len(failed)))

for fail_test in failed:
    print('Test: {}'.format(fail_test[0]))
    print('Traceback: {}'.format(fail_test[1]))
if failed:
    print('===========================')
    traceback.print_exc()
    print('===========================')

OUT = result.getvalue()
