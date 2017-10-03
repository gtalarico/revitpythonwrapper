.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


==================
rpw and rpw.revit
==================

Revit Python Wrapper
*********************

.. automodule:: rpw.__revit
    :undoc-members:

.. data:: UI
    :module: rpw
    :annotation:  Revit.UI Namespace

.. data:: DB
    :module: rpw
    :annotation:   Revit.DB Namespace

Revit Wrapper
*********************

.. autoclass:: rpw.__revit.Revit
    :members:
    :special-members: __init__, __getattr__, __getitem__
    :private-members:
    :show-inheritance:

.. hint::
    Besides creating these global variables, the module's global variable initializer
    also adds the path to the Ironpython Library to your sys.path, so you can import standard python
    libraries right away, and skip the typical:

    >>> import sys
    >>> sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')

Typical Methods
******************

When RPW is not used, import code ends up being different for each platform:

    >>> # RevitPythonShell / pyRevit
    >>> import clr
    >>> clr.AddReference('RevitAPI')
    >>> clr.AddReference('RevitAPIUI')
    >>>
    >>> from Autodesk.Revit.DB import *
    >>> from Autodesk.Revit.UI import *
    >>>
    >>> doc = __revit__.ActiveUIDocument.Document
    >>> uidoc = __revit__.ActiveUIDocument

    >>> # Dynamo
    >>> import clr
    >>> clr.AddReference('RevitAPI')
    >>> clr.AddReference('RevitAPIUI')
    >>> from Autodesk.Revit.DB import *
    >>> from Autodesk.Revit.UI import *
    >>>
    >>> clr.AddReference("RevitServices")
    >>> import RevitServices
    >>> from RevitServices.Persistence import DocumentManager
    >>> from RevitServices.Transactions import TransactionManager
    >>>
    >>> doc = DocumentManager.Instance.CurrentDBDocument
    >>> uiapp = DocumentManager.Instance.CurrentUIApplication
    >>> app = uiapp.Application
    >>> uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

----------------------------------------------

Implementation
**************

.. literalinclude:: ../../rpw/__revit.py
    :start-after: """  #

.. disqus
