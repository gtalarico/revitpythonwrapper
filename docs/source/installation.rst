=============================
Installation
=============================

********************
pyRevit
********************

RevitPythonWrapper now ships with pyRevit. Just import rpw:

>>> from rpw import revit, db, ui

********************
RevitPythonShell
********************

Revit Python Wrapper works well with the RevitPythonShell

    1. Clone the `RevitPythonWrapper Repository <http://www.github.com/gtalarico/revitpythonwrapper>`_
    2. Add the the repository directory to `RevitPythonShell's <https://github.com/architecture-building-systems/revitpythonshell>`_ search path

.. tip::
    Add rpw to RevitPythonShell's Search Path to have it pre-loaded every you start it.

.. image:: ../_static/rps/add-path.png
.. image:: ../_static/rps/rps-use.png




********************
Dynamo
********************

RevitPythonWrapper is distributed through Dynamo's Package Manager ships
with everything you need, but you can also download it your self
and import it as you would with any other Python modules.

The package includes a Node that helps you find the location of the RPW library (see image below).
Once you have the location, just add it to your ``sys.path``, and you should be able to import the library.
You can always manually add the library path; the node is only included for convenience.

For more details and question about this please see this `post <https://forum.dynamobim.com/t/debugging-python-code/12729/20>`_.

.. Note::
    Be sure the checkout the ``RPW_GetStarted.dyn`` file that is installed with the Package
    for practical examples.
    The file will typically be saved in:
    :file:`.../Dynamo/1.X/packages/RevitPythonWrapper/extra/RPW_GetStarted.dyn`

Python Code Sample

>>> # USe RPW_GetFilePath to find Rpw's path and plugged it into IN[0]
>>> # or append path manually
>>> import sys
>>> rpw_path = IN[0]  # IN[0] is a path to rpw.zip or the parent folder where rpw is located
>>> sys.path.append(rpw_path)
>>> from rpw import db, ui
>>> walls = db.Collector(of_class='Wall').elements
>>> ui.forms.Alert('Found {} walls'.format(len(walls)))

.. image:: ../_static/dynamo/package.png
.. image:: ../_static/dynamo/intro.png

.. note::
    Images below might be outdated
