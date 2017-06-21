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
import os
import unittest
import traceback

# rpw_module_path = IN[0]  # Path to RPW Module
# if isinstance(rpw_module_path, list):
#     sys.path = rpw_module_path
# else:
#     sys.path.insert(0, rpw_module_path)
sys.path.append(r'C:\Users\gtalarico\Dropbox\Shared\dev\repos\revitpythonwrapper\revitpythonwrapper.lib')
sys.path.append(r'C:\Users\gtalarico\Dropbox\Shared\dev\repos\revitpythonwrapper\revitpythonwrapper.lib\tests\rpw.extension\rpw.tab\rpw.panel\RunAll.pushbutton')
os.chdir(r'C:\Users\gtalarico\Dropbox\Shared\dev\repos\revitpythonwrapper\revitpythonwrapper.lib\tests\rpw.extension\rpw.tab\rpw.panel\RunAll.pushbutton')

from StringIO import StringIO
result = StringIO()
sys.stdout = result


print('IMPORT TESTS...')
# import tests_rpw
# import RunAll_script as tests_rpw
print('TESTS RUNNER: {}'.format(__file__))
from rpw import logger
# logger.disable()
#
# testsuite = unittest.TestLoader().loadTestsFromModule(tests_rpw)
# test_result = unittest.TextTestRunner(verbosity=3, buffer=False).run(testsuite)
#
# success = test_result.wasSuccessful()
# ran = test_result.testsRun
# failed = test_result.failures
#
# print('Ran: {}'.format(ran))
# print('Success: {}'.format(success))
# print('Failed: {}'.format(len(failed)))
#
# for fail_test in failed:
#     print('Test: {}'.format(fail_test[0]))
#     print('Traceback: {}'.format(fail_test[1]))
# if failed:
#     print('===========================')
#     traceback.print_exc()
#     print('===========================')
#
# OUT = result.getvalue()


script_dir = IN[0]
# panel_dir = parent(script_dir)
os.chdir(script_dir)

for item in os.listdir('.'):
    if os.path.isdir(item):
        sys.path.append(os.path.join(script_dir, item))

# OUT = [script_dir, sys.path]
import Globals_script as GlobalsTests
import Collector_script as CollectorTests
import Elements_script as ElementTests
import Forms_script as FormTests
import Transaction_script as TransactionTests
import Selection_script as SelectionTests
import Utils_script as UtilsTests
#
all_tests = [
             GlobalsTests,
             CollectorTests,
             UtilsTests,
             ElementTests,
             TransactionTests,
             SelectionTests,
             #  FormTests,
             ]


testsuite = unittest.TestLoader().loadTestsFromModule(GlobalsTests)
test_result = unittest.TextTestRunner(verbosity=3, buffer=True).run(testsuite)
print(test_result)

OUT = result.getvalue()
results = []
for module in all_tests:
    from rpw.utils.logger import logger
    # logger.verbose(False) # Disable Logger
    # logger.disable()

    testsuite = unittest.TestLoader().loadTestsFromModule(module)
    # test_result = unittest.TextTestRunner(verbosity=0, buffer=True).run(testsuite)
    test_result = unittest.TextTestRunner(verbosity=3, buffer=True).run(testsuite)
    results.append((module, test_result))

for module, test_result in results:
    print('===========================')
    print(module.__name__)
    print(test_result)

    success = test_result.wasSuccessful()
    ran = test_result.testsRun
    failed = test_result.failures
    errors = test_result.errors

    print('Success: {}'.format(success))
    print('Ran: {}'.format(ran))
    print('Failed: {}'.format(len(failed)))
    print('Errors: {}'.format(len(errors)))

    for fail_test in failed:
        print('++++++++++')
        print('Test: {}'.format(fail_test[0]))
        print('Traceback: {}'.format(fail_test[1]))
        print('++++++++++')
    if failed:
        print('++++++++++')
        traceback.print_exc()
        print('++++++++++')

print('===========================')
if all([r.wasSuccessful() for m, r in results]):
    total = sum([r.testsRun for m, r in results if r.wasSuccessful()])
    print('All Tests Passed: {}'.format(total))
else:
    print('FAILED')
print('===========================')


OUT = result.getvalue()
