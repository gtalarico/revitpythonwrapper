.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


===============
Dynamo
===============

The Revit Python Wrapper can easily be used within dynamo.
The package distributed through Dynamo's Package Manager ships
with everything you need, but you can always download it your self
and import it as you would with any other Python modules.

The package includes a Node that helps you find the location of the RPW library (see image below).
Once you have the location, just add it to your ``sys.path``, and you should be able to import the library.
You can always manually add the library path; the node is only included for convenience.

.. Note::
    Be sure the checkout the ``RPW_GetStarted.dyn`` file that is installed with the Package
    for practical examples.
    The file will typically be saved in:
    :file:`.../Dynamo/1.X/packages/RevitPythonWrapper/extra/RPW_GetStarted.dyn`

Python Code Sample

>>> # Find RPW_GetFilePath node and plugged it into IN[0]
>>> # or append path manually
>>> import sys
>>> rpw_path = IN[0]
>>> sys.path.append(rpw_path)
>>> import rpw
>>> from rpw.db.collector import Collector

.. image:: _static/dynamo/package.png
.. image:: _static/dynamo/intro.png

.. disqus
