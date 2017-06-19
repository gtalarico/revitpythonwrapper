.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

====================
Revit Python Wrapper
====================


.. toctree::
   :maxdepth: 1
   :hidden:

   self
   revit
   base
   element
   selection
   transaction
   collector
   geometry
   builtins
   forms
   console
   utils
   dynamo
   revitpythonshell
   exceptions
   tests

   known_issues


.. image:: _static/logo/logo-tight.png
  :scale: 50%

Version: |version|

:ref:`modindex` | :ref:`genindex`

**********************************
A Python Wrapper For the Revit API
**********************************

Revit Python Wrapper was created to help Python programmers write Revit API code.

Wrapper classes make the interaction with API objects less repetitive,
and more consistent with Python's conventions.

It also provides a few convenient shortcuts:

    * Initializes a ``doc`` and ``uidoc``
      document handling variables, so you can
      reuse code across platforms with no change to your import code.

    * Imports ``clr``, and adds ``RevitAPI.dll`` + ``RevitAPIUI.dll`` assemblies.

    * Adds Reference the IronPython Standard Library to your ``sys.path`` (for :doc:`dynamo`).

    * Easy to use WPF :doc:`forms` so you can request additional user input
      with little effort.


.. caution::
    | This library should not be used in complex applications or mission-critical work.
    | API changes are expected.

-------------------------------------------------------------------

**********************************
Using RPW
**********************************

There are several ways to use RevitPythonWrapper:

    * :doc:`revitpythonshell`: import the library directly into the interactive interpreter
    * :doc:`dynamo`: Install through `Dynamo Package Manager <https://dynamopackages.com/>`_
    * `pyRevit <http://eirannejad.github.io/pyRevit/>`_ : import it into your scripts
    * Macros: import library into your Python Macros (untested).

Benefits
^^^^^^^^

    * Normalizes Document and Application handlers for Revit + Dynamo
    * Increase code re-use across platforms (ie. :doc:`revit`)
    * Implements patterns to reduce repetitive tasks (ie. :class:`rpw.db.transaction`)
    * Handles some data-type casting for speed and flexibility (ie. :any:`rpw.db.Parameter`)
    * Normalizes API calls for different Revit Versions (not yet implemented)

Compatibility
^^^^^^^^^^^^^

    RevitPythonWrapper has been tested on the following platforms:

    * RevitPythonShell + Revit: 2015, 2016, 2017
    * pyRevit: 2015, 2016
    * Dynamo: 1.2

Contribute
^^^^^^^^^^
    https://www.github.com/gtalarico/revitpythonwrapper

License
^^^^^^^
    `MIT License <https://opensource.org/licenses/MIT>`_

---------------------------------------------------------------------------------

**********************************
Basic Components
**********************************

The examples below give a basic overview of how the library is used,
paired with an example sans-rpw.

:doc:`revit`
^^^^^^^^^^^^^^

    >>> # Handles Document Manager and namespace imports for RevitPythonShell and Dynamo
    >>> from rpw import doc, uidoc, DB, UI
    >>> uidoc.ActiveView

Without RPW

    >>> # Dynamo Example
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


:doc:`transaction`
^^^^^^^^^^^^^^^^^^

    >>> # Using Wrapper - Same code for RevitPythonShell, and Dynamo
    >>> import rpw
    >>> from rpw import doc
    >>> with rpw.db.transaction('Delete Object'):
    >>>     doc.Remove(SomeElementId)

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
    >>>
    >>> transaction = Transaction(doc, 'Delete Object')
    >>> transaction.Start()
    >>> try:
    >>>     doc.Remove(SomeElementId)
    >>> except:
    >>>     transaction.RollBack()
    >>> else:
    >>>     transaction.Commit()


:doc:`selection`
^^^^^^^^^^^^^^^^^^^

    >>> import rpw
    >>> selection = rpw.ui.selection()
    >>> selection[0]
    < Autodesk.Revit.DB.Element >
    >>> selection.elements
    [< Autodesk.Revit.DB.Element >]

    >>> # Other Features
    >>> selection.clear()
    >>> selection.add(DB.Element or DB.ElementId)

Without RPW

    >>> # In Revit Python Shell
    >>> uidoc = __revit__.ActiveUIDocument # Different for Dynamo
    >>> selection_ids = uidoc.Selection.GetElementIds()
    >>> selected_elements = [doc.GetElemend(eid) for eid in selection_ids]


:doc:`element`
^^^^^^^^^^^^^^^^^^^

    >>> import rpw
    >>> element = rpw.db.element(SomeRevitElement)
    >>> with rpw.db.transaction('Set Comment Parameter'):
    >>>     element.parameters['Comments'].value = 'Some String'
    >>>
    >>> # Parameters
    >>> element.parameters['some value'].type
    <type: string>
    >>> element.parameters['some value'].value
    'Some String'
    >>> element.parameters.builtins['WALL_LOCATION_LINE'].value
    1

    Access to original attributes, and parameters are provided
    by the :any:`Element` wrapper. More Specialized Wrappers
    also provide additional features based on its type:
    ``DB.FamilyInstace`` (:any:`Instance`), ``DB.FamilySymbol`` (:any:`Symbol`),
    ``DB.Family`` (:any:`Family`), and ``DB.Category`` (:any:`Category`).


    >>> instance = rpw.Instance(SomeFamilyInstance)
    >>> instance.parameters['Comments']
    'Comment'
    >>> instance.parameters['Comments'].value = 'Your Comment'
    # Comment set
    >>> instance.parameters.builtins['SOME_BUILT_IN'].value
    'Parameter Value'
    >>> instance.symbol
    <RPW_Symbol:72" x 36">
    >>> instance.symbol.name
    '72" x 36"'
    >>> instance.family
    <RPW_Family:desk>
    >>> instance.family.name
    'desk'
    >>> instance.category
    <RPW_Category:Furniture>
    >>> instance.symbol.instances
    [<RPW_Instance:72" x 36">, <RPW_Instance:72" x 36">, ... ]


:doc:`collector`
^^^^^^^^^^^^^^^^^^^

    >>> import rpw
    >>> walls = rpw.db.collector(of_class='Wall').elements
    [< instance DB.Wall>, < instance DB.Wall>, < instance DB.Wall>, etc]

    >>> aview = rpw.db.collector(of_category='OST_Views', is_element_type=True).first
    < instance DB.View>

Without RPW

    >>> # Typical API Example:
    >>> from Autodesk.Revit.DB import FilteredElementCollector, WallType
    >>> collector = FilteredElementCollector()
    >>> walls = FilteredElementCollector.OfClass(WallType).ToElements()

:any:`ParameterFilter`
^^^^^^^^^^^^^^^^^^^^^^^^

    >>> import rpw
    >>> filter_rule = rpw.db.parameterFilter(some_param_id, greater=3)
    >>> collector = rpw.db.collector(of_class='WallType', paramter_filter=filter_rule)

Without RPW

    >>> # Typical API Example:
    >>> from Autodesk.Revit.DB import FilteredElementCollector, WallType
    >>> from Autodesk.Revit.DB import ParameterFilterRuleFactory, ElementParameterFilter
    >>>
    >>> rule = ParameterFilterRuleFactory.CreateEqualsRule(param_id, some_string, False)
    >>> filter_rule = ElementParameterFilter(rule)
    >>> collector = FilteredElementCollector.OfClass(WallType).WherePasses(filter_rule)


:doc:`forms`
^^^^^^^^^^^^^^^^^^^

    >>> options = ['Option 1','Option 2','Option 3']
    >>> form = SelectFromList('Window Title', options)
    >>> # Form shows on screen
    >>> form_ok = form.show()
    >>> if not form_ok:
    >>>     sys.exit() # User Canceld
    >>> selected_item = form.selected


:doc:`utils`
^^^^^^^^^^^^^^^^^^^

    >>> # Handy Batch Converters to and from Element / ElementIds
    >>> rpw.utils.to_elements(DB.ElementId)
    [ DB.Element ]
    >>> rpw.utils.to_elements(20001)
    [ DB.Element ]
    >>> rpw.utils.to_elements([20001, 20003])
    [ DB.Element, DB.Element ]

    >>> rpw.utils.to_element_ids(DB.Element)
    [ DB.ElementId ]
    >>> rpw.utils.to_element_ids(20001)
    [ DB.ElementId ]
    >>> rpw.utils.to_element_ids([20001, 20003])
    [ DB.ElementId, DB.ElementId ]
