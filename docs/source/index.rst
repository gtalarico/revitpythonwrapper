.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================
Revit Python Wrapper
====================

.. image:: ../_static/logo/logo-tight.png
  :scale: 50%

Version: |version|

:ref:`modindex` | :ref:`genindex`

**********************************
A Python Wrapper For the Revit API
**********************************

`Python Revit Api code that looks like Python`

Revit Python Wrapper was created to help Python programmers write Revit API code.

Wrapper classes make the interaction with API objects less repetitive,
and more consistent with Python's conventions.

.. caution::
    | API breaking changes are expected on 2.0 release (Q4 2017)

Questions? Post them over in the project's `Github Page <http://www.github.com/gtalarico/revitpythonwrapper>`_ or
hit me up on `twitter <https://twitter.com/gtalarico>`_.

Release Notes
^^^^^^^^^^^^^

`Release Notes On Github Repository <https://github.com/gtalarico/revitpythonwrapper/blob/master/notes.md>`_

Contribute
^^^^^^^^^^
    https://www.github.com/gtalarico/revitpythonwrapper

License
^^^^^^^
    `MIT License <https://opensource.org/licenses/MIT>`_

-------------------------------------------------------------------

**********************************
Using RPW
**********************************

There are several ways to use RevitPythonWrapper:

    * `pyRevit <http://eirannejad.github.io/pyRevit/>`_
    * RevitPythonShell
    * Dynamo

    For more details on how to use pyRevit in these platforms, see the  :doc:`installation` page.

Benefits
^^^^^^^^

    * Normalizes Document and Application handlers for Revit + Dynamo
    * Increase code re-use across platforms (ie. :doc:`revit`)
    * Implements patterns to reduce repetitive tasks (ie. :class:`rpw.db.Transaction`, :class:`rpw.db.Collector`)
    * Handles some data-type casting for speed and flexibility (ie. :any:`rpw.db.Parameter`)
    * Normalizes API calls for different Revit Versions
    * Rpw Initializes all common variables such as document handling variables (``doc`` and ``uidoc``)
      so you can reuse code across platforms with no change to your import code. See :doc:`revit`.
    * Preloads ``clr``, and the required Revit assemblies such as ``RevitAPI.dll`` and ``RevitAPIUI.dll`` as well as .NET types such as ``List`` as ``Enum``. See :any:`rpw.utils.dotnet`
    * Adds IronPython Standard Library to your ``sys.path`` (useful for Dynamo scripts).
    * Easy to use WPF :doc:`ui/forms` and :any:`TaskDialog` wrapper makes it easy to request additional user input
      with little effort.

Compatibility
^^^^^^^^^^^^^

    RevitPythonWrapper has been tested on the following platforms:

    * RevitPythonShell + Revit: 2015, 2016, 2017
    * pyRevit 4.4+ on 2015, 2016, 2017, 2017.1
    * Dynamo: 1.2, 1.3

---------------------------------------------------------------------------------

**********************************
Before You start
**********************************

To make it easier to users, Rpw attempts to maintain close fidelity to names and terms use by the Revit Api.
So if you know the Revit API, it should feel familiar.
Alternative names are only used where Revit Api names are inconvenient or inadequate.
For example, the rpw :doc:`db/transaction` wrapper is also called ``Transaction``, however, the
FilteredElementCollector wrapper, is called ``Collector``.

To minimize namespace collisions, the patterns below are highly recommended:

1. Avoid ``from Something import *`` . This is generally not a good idea anyway.
2. Use rpw imports instead of `import clr` and `from Autodesk.Revit ...` See :doc:`revit` for more details. :any:`rpw.utils.dotnet` has .NET classes such as List and Enum ready to go.
3. Keep rpw namespaces isolated from Revit Namespaces. Rpw's wrappers are lowercase the lowercase counterpart of their Revit equivalents, such as db, and ui. Revit Namespaces are DB, UI (``from Autodesk.Revit import DB` and ``from Autodesk.Revit import UI`)

>>> from rpw import revit, db, ui, DB, UI
>>> # For rpw wrappers, especially those in rpw.db, keep them inside db:
>>> doors = db.Collector(of_category='Doors')
>>> with db.Transaction('Delete'):
...     [revit.doc.Delete(id) for id in doors.element_ids]
>>> # Keep Revit namespaces them under DB:
>>> invalid_id = DB.ElementId(-1)


**********************************
Contents
**********************************

:ref:`genindex` | :ref:`modindex`

.. toctree::
   :maxdepth: 2

   self
   installation

   revit
   db
   ui
   base
   utils
   extras
   exceptions

   known_issues
   tests
   contribute

---------------------------------------------------------------------------------

**********************************
Quick Overview and Comparison
**********************************

The examples below give a basic overview of how the library is used,
paired with an example sans-rpw.

:doc:`revit`
^^^^^^^^^^^^^^

    >>> # Handles Document Manager and namespace imports for RevitPythonShell and Dynamo
    >>> import rpw
    >>> from rpw import revit, db, ui, DB, UI
    # That's pretty much all you need

Without RPW

    >>> # Dynamo Example
    >>> import clr
    >>> clr.AddReference('RevitAPI')
    >>> clr.AddReference('RevitAPIUI')
    >>> from Autodesk.Revit.DB import *
    >>> from Autodesk.Revit.UI import *
    >>> # RevitServices
    >>> clr.AddReference("RevitServices")
    >>> import RevitServices
    >>> from RevitServices.Persistence import DocumentManager
    >>> from RevitServices.Transactions import TransactionManager
    >>> # doc and uiapp
    >>> doc = DocumentManager.Instance.CurrentDBDocument
    >>> uiapp = DocumentManager.Instance.CurrentUIApplication
    >>> app = uiapp.Application
    >>> uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument


:doc:`db/transaction`
^^^^^^^^^^^^^^^^^^^^^

    >>> # Using Wrapper - Same code for RevitPythonShell, and Dynamo
    >>> from rpw import revit, db
    >>> with db.Transaction('Delete Object'):
    ...     revit.doc.Remove(SomeElementId)

Without RPW

    >>> # Typical Transaction In Dynamo
    >>> import clr
    >>> clr.AddReference("RevitServices")
    >>> import RevitServices
    >>> from RevitServices.Persistence import DocumentManager
    >>> from RevitServices.Transactions import TransactionManager
    >>> doc = DocumentManager.Instance.CurrentDBDocument
    >>> TransactionManager.Instance.EnsureInTransaction(doc)
    >>> doc.Remove(SomeElementId)
    >>> TransactionManager.Instance.TransactionTaskDone()

    >>> # Typical Transaction in Revit Python Shell / pyRevit
    >>> import clr
    >>> clr.AddReference('RevitAPI')
    >>> from Autodesk.Revit.DB import Transaction
    >>> doc = __revit__.ActiveUIDocument.Document
    >>> transaction = Transaction(doc, 'Delete Object')
    >>> transaction.Start()
    >>> try:
    ...     doc.Remove(SomeElementId)
    >>> except:
    ...     transaction.RollBack()
    >>> else:
    ...     transaction.Commit()


:doc:`ui/selection`
^^^^^^^^^^^^^^^^^^^

    >>> from rpw import ui
    >>> selection = ui.Selection()
    >>> selection[0]
    < Autodesk.Revit.DB.Element >
    >>> selection.elements
    [< Autodesk.Revit.DB.Element >]

Without RPW

    >>> # In Revit Python Shell
    >>> uidoc = __revit__.ActiveUIDocument # Different for Dynamo
    >>> selection_ids = uidoc.Selection.GetElementIds()
    >>> selected_elements = [doc.GetElemend(eid) for eid in selection_ids]


:doc:`db/element`
^^^^^^^^^^^^^^^^^^^

    >>> from rpw import revit, db
    >>> element = db.Element(SomeRevitElement)
    >>> with db.Transaction('Set Comment Parameter'):
    ...     element.parameters['Comments'].value = 'Some String'
    >>> element.parameters['some value'].type
    <type: string>
    >>> element.parameters['some value'].value
    'Some String'
    >>> element.parameters.builtins['WALL_LOCATION_LINE'].value
    1

Access to original attributes, and parameters are provided
by the :any:`Element` wrapper.

More Specialized Wrappers
also provide additional features based on its type:
``DB.FamilyInstace`` (:any:`FamilyInstance`), ``DB.FamilySymbol`` (:any:`FamilySymbol`),
``DB.Family`` (:any:`Family`), and ``DB.Category`` (:any:`Category`).


    >>> instance = db.Element(SomeFamilyInstance)
    <rpw:FamilyInstance % DB.FamilyInstance symbol:72" x 36">
    >>> instance.symbol
    <rpw:FamilySymbol % DB.FamilySymbol symbol:72" x 36">
    >>> instance.symbol.name
    '72" x 36"'
    >>> instance.family
    <rpw:Family % DB.Family name:desk>
    >>> instance.family.name
    'desk'
    >>> instance.category
    <rpw:Category % DB.Category name:Furniture>
    >>> instance.symbol.instances
    [<rpw:Instance % DB.FamilyInstance symbol:72" x 36">, ... ]


:doc:`db/collector`
^^^^^^^^^^^^^^^^^^^

    >>> from rpw import db
    >>> walls = db.Collector(of_class='Wall')
    <rpw:Collector % DB.FilteredElementCollector count:10>
    >>> walls.wrapped_elements
    [< instance DB.Wall>, < instance DB.Wall>, < instance DB.Wall>, ...]

    >>> view = db.collector(of_category='OST_Views', is_type=False).first

    The Collector Class is also accessible through the wrappers using the ``collect()`` method

    >>> db.Room.collect()
    <rpw:Collector % DB.FilteredElementCollector count:8>
    >>> db.Room.collect(level='Level 1')
    <rpw:Collector % DB.FilteredElementCollector count:2>

Without RPW

    >>> # Typical API Example:
    >>> from Autodesk.Revit.DB import FilteredElementCollector, WallType
    >>> collector = FilteredElementCollector()
    >>> walls = FilteredElementCollector.OfClass(WallType).ToElements()

:doc:`db/parameters`
^^^^^^^^^^^^^^^^^^^^^^^^

    >>> import rpw
    >>> filter_rule = db.ParameterFilter(param_id, greater=3)
    >>> collector = db.Collector(of_class='WallType', paramter_filter=filter_rule)

Without RPW

    >>> # Typical API Example:
    >>> from Autodesk.Revit.DB import FilteredElementCollector, WallType
    >>> from Autodesk.Revit.DB import ParameterFilterRuleFactory, ElementParameterFilter
    >>>
    >>> rule = ParameterFilterRuleFactory.CreateEqualsRule(param_id, some_string, False)
    >>> filter_rule = ElementParameterFilter(rule)
    >>> collector = FilteredElementCollector.OfClass(WallType).WherePasses(filter_rule)


:doc:`ui/forms`
^^^^^^^^^^^^^^^^^^^

    >>> from rpw.ui.forms import SelectFromList
    >>> options = ['Option 1','Option 2','Option 3']
    >>> form = SelectFromList('Window Title', options)
    >>> form.show()
    >>> selected_item = form.selected
