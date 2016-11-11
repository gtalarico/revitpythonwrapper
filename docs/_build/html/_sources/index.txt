.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Revit Python Wrapper
==============================================


.. toctree::
   :maxdepth: 1
   :hidden:

   self
   globals
   element
   selection
   transaction
   collector
   enumeration
   forms
   dynamo
   revitpythonshell
   exceptions

   known_issues


.. automodule:: rpw

************************************
Content
************************************

* :ref:`modindex`
* :ref:`genindex`

************************************
A Python Wrapper For the Revit API
************************************

Revit Python Wrapper was created to help Python programmers write Revit API code.

Wrapper classes make the interaction with API objects less repetitive,
and more consistent with Python's conventions.

It also handles the creation of global ``doc`` and ``uidoc`` variables so you can
reuse code across platforms with no change
application and document handlers (:ref:`globals`), as well as
imports to common API namespaces, so you can
so you can re-use your code across platforms without having to change your imports.

Lastly, it provides some

I started this library primary to bootstrapping scripts, testing and educational purposes,


.. caution::
    This library should not be used in complex applications or mission-critical work.


Where To Use RWP
****************

There are several ways to use RevitPythonWrapper:

    * Import Library into :doc:`revitpythonshell` interactive interpreter
    * :doc:`dynamo`: Install through `Dynamo Package Manager <https://dynamopackages.com/>`_
    * `MIT License <https://opensource.org/licenses/MIT>`_
    * `pyRevit <http://eirannejad.github.io/pyRevit/>`_ : import it into your scripts
    * Macros: import library into your Python Macros

Why Use it
**********

    * Normalizes Document and Application handlers for Revit + Dynamo
    * Normalizes API calls for different Revit Versions
    * Increase code re-use across platforms
    * Implements patterns to reduce repetitive tasks
    * Make some calls feel more natural to Python
    * Handle data coercion for speed and flexibility (see :any:`rpw.selection` for example)
    * `Might` help new users get started with the API


License
^^^^^^^
    `MIT License <https://opensource.org/licenses/MIT>`_


Basic Components
****************


:doc:`globals`
^^^^^^^^^^^^^^

    >>> # Handles Document Manager and namespace imports for RevitPythonShell and Dynamo
    >>> from rpw import doc, uidoc, DB, UI
    >>> uidoc.ActiveView
    >>> doc.Delete()
    >>> DB.ElementId(20000)


:doc:`transaction`
^^^^^^^^^^^^^^^^^^

    >>> # Using Wrapper
    >>> from rpw import Transaction, doc
    >>> with rpw.Transaction('Delete Object')
    >>>     doc.Remove(SomeElementId)
    >>> # This code remains the same for RevitPythonShell, and Dynamo

    In constrast, Transactions usually looks something like this

    >>> # In Dynamo
    >>> import clr
    >>> clr.AddReference("RevitServices")
    >>> import RevitServices
    >>> from RevitServices.Persistence import DocumentManager
    >>> from RevitServices.Transactions import TransactionManager
    >>> doc = DocumentManager.Instance.CurrentDBDocument
    >>> TransactionManager.Instance.EnsureInTransaction(doc)
    >>> doc.Remove(SomeElementId)
    >>> TransactionManager.Instance.TransactionTaskDone()

    >>> # Revit Python Shell
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
    >>> selection = rpw.Selection()
    >>> selection[0]
    < Autodesk.Revit.DB.Element >
    >>> selection.elements
    [< Autodesk.Revit.DB.Element >]

    >>> # Other Features
    >>> selection.add(SomeElementID)

    >>> # In Revit Python Shell
    >>> uidoc = __revit__.ActiveUIDocument # Different for Dynamo
    >>> selection_ids = uidoc.Selection.GetElementIds()
    >>> selected_elements = [doc.GetElemend(eid) for eid in selection_ids]


:doc:`element`
^^^^^^^^^^^^^^^^^^^

    >>> import rpw
    >>> element = rpw.Element(SomeRevitElement)
    >>> with rpw.Transaction('Set Comment Parameter'):
    >>>     element.parameters['Comments'].value = 'Some String'
    'Some String' set as parameter value
    >>> element.parameters['some value'].type
    `<type: string>`
    >>> element.parameters['some value'].value
    'Some String'
    >>> element.parameters.builtins['WALL_LOCATION_LINE'].value
    1

:doc:`collector`
^^^^^^^^^^^^^^^^^^^

    >>> import rpw
    >>> walls = rpw.Collector(of_class='Wall').elements
    [< instance DB.Wall>, < instance DB.Wall>, < instance DB.Wall>, etc]

    >>> aview = rpw.Collector(of_category='OST_Views', is_element_type=True).first
    < instance DB.View>

    >>> # Typical API Example:
    >>> from Autodesk.Revit.DB import FilteredElementCollector, WallType
    >>> collector = FilteredElementCollector()
    >>> walls = FilteredElementCollector.OfClass(WallType).ToElements()


:any:`ParameterFilter`
^^^^^^^^^^^^^^^^^^^^^^^

    >>> import rpw
    >>> filter_rule = rpw.ParameterFilter(some_param_id, greater=3)
    >>> collector = rpw.Collector(of_class='WallType', paramter_filter=filter_rule)

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
