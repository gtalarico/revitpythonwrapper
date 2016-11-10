.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Globals
==================

Global variables help normalize imports across platforms.

    >>> from rpw import doc, uidoc, DB, UI
    >>> uidoc.ActiveView
    >>> DB.ElementId(00000)

.. data:: doc
    :module: rpw
    :annotation: Application Document handler

.. data:: uidoc
    :module: rpw
    :annotation: UI Document handler

.. data:: UI
    :module: rpw
    :annotation: Revit.UI Namespace

.. data:: DB
    :module: rpw
    :annotation: Revit.DB Namespace


Implementation
**************

.. literalinclude:: ../rpw/__init__.py
    :start-after: import sys
