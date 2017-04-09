.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


==================
Tests
==================

The Test Suite below is used to verify functionalities, as well as to
validate compatibility across different platforms. These tests below have
been executed without failures on:

    * Revit 2015
    * Revit 2016
    * Revit 2017
    * Dynamo 1.2

The Test Suite also provides a many
examples of how the library is intended to be used.

----------------------------------------------

Test Suite
**************

.. literalinclude:: ../tests/tests_rpw.py
    :end-before: run()

.. literalinclude:: ../tests/tests_forms.py
    :end-before: run()

.. disqus::
