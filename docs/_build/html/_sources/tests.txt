.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


==================
Tests
==================

Over 75+ tests are provide to verify functionalities, as well as to
validate compatibility across different platforms.

Tests shown below have been execute with 100% success on
Revit 2015, 2016, and Dynamo 1.2.

The tests use original API commands to set up some base elements,
and then use ``rpw`` wrappers as needed.

They included here to help document the intended usages.


----------------------------------------------

Test Suite
**************

.. literalinclude:: ../tests/tests_rpw.py
    :end-before: run()

.. literalinclude:: ../tests/tests_forms.py
    :end-before: run()
