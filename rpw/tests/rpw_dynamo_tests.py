""" Revit Python Wrapper Tests

Passes:

    * Revit:
        * Revit 2015
        * Revit 2016
"""

import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
import unittest
import traceback

import os
repos = os.getenv('REPOS')
path = os.path.join(repos, 'revitpythonwrapper')
sys.path.append(path)

os.chdir(path)

from StringIO import StringIO
result = StringIO()
sys.stdout = result

from rpw.tests import rpw_tests

testsuite = unittest.TestLoader().loadTestsFromModule(rpw_tests)
test_result = unittest.TextTestRunner(verbosity=3, buffer=True).run(testsuite)

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
