""" Revit Python Wrapper Tests

Passes:

    * Revit:
        * Revit 2015
        * Revit 2016
"""

import sys
import unittest
import os
import traceback

parent = os.path.dirname

script_dir = parent(__file__)
panel_dir = parent(script_dir)
os.chdir(panel_dir)

for item in os.listdir('.'):
    if os.path.isdir(item):
        sys.path.append(os.path.join(panel_dir, item))

import Globals_script as GlobalsTests
import Collector_script as CollectorTests
import Elements_script as ElementTests
import Forms_script as FormTests
import Transaction_script as TransactionTests
import Selection_script as SelectionTests
import Utils_script as UtilsTests

all_tests = [
             GlobalsTests,
             CollectorTests,
             UtilsTests,
             ElementTests,
             TransactionTests,
             SelectionTests,
             #  FormTests,
             ]

results = []
for module in all_tests:
    from rpw.utils.logger import logger
    # logger.verbose(False) # Disable Logger
    logger.disable()

    testsuite = unittest.TestLoader().loadTestsFromModule(module)
    # test_result = unittest.TextTestRunner(verbosity=0, buffer=True).run(testsuite)
    test_result = unittest.TextTestRunner(verbosity=3, buffer=False).run(testsuite)
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

    # for fail_test in failed:
    #     print('++++++++++')
    #     print('Test: {}'.format(fail_test[0]))
    #     print('Traceback: {}'.format(fail_test[1]))
    #     print('++++++++++')
    # if failed:
    #     print('++++++++++')
    #     traceback.print_exc()
    #     print('++++++++++')

print('===========================')
if all([r.wasSuccessful() for m, r in results]):
    total = sum([r.testsRun for m, r in results if r.wasSuccessful()])
    print('All Tests Passed: {}'.format(total))
else:
    print('FAILED')
print('===========================')
