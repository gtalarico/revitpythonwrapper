"""

************************************
A Python Wrapper For the Revit API
************************************

Revit Python Wrapper helps lazy programmers write Revit API code in Python.

The Wrappers make the interaction with API objects more
consistent with Python's conventions, and also implement
patterns to make your code more conscise.

The wrapper will also normalize application and document handler, as well
as some  API version-specific calls so you can re-use your code across
platforms and Revit API versions.

This library should not be used in complex applications, and it's not guaranteed
it will be maintained at all.

When to Use RPW
****************

* When you are working in the RevitPythonShell, pyRevit, or Dynamo Python Nodes
* When you want your code to work with no change in the aforementioned platforms
* Short scripts and other non-mission-critical work
* Testing, and educational purporses


Project Goals
*************

* Normalize Document and Application handlers for Revit + Dynamo
* Normalize API calls for different Revit Versions
* Implement Resusable patterns to reduce repetitive tasks
* Create wrappers to make common calls more natural to Python
* Increase code re-use
* Handle data coercion for more flexibility (see :any:`rpw.selection` for example)

License
^^^^^^^
`MIT License <https://opensource.org/licenses/MIT>`_



Using RevitPythonWrapper
************************


:doc:`globals`
**************

    >>> # Handles Document Manager and namespace imports for RevitPythonShell and Dynamo
    >>> from rpw import doc, uidoc, DB, UI
    >>> uidoc.ActiveView
    >>> doc.Delete()
    >>> DB.ElementId(20000)


:doc:`transaction`
******************

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
****************

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
**************

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
****************

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
^^^^^^^^^^^^^^^^^^^^^^

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
****************

    >>> options = ['Option 1','Option 2','Option 3']
    >>> form = SelectFromList('Window Title', options)
    >>> # Form shows on screen
    >>> form_ok = form.show()
    >>> if not form_ok:
    >>>     sys.exit() # User Canceld
    >>> selected_item = form.selected


"""


__title__ = 'revitpythonwrapper'
__version__ = '0.0.7'
__author__ = 'Gui Talarico'
__license__ = 'MIT'
__copyright__ = 'Gui Talarico'


import sys
from rpw.logger import logger

try:
    #  This is a workaround to fix Sphinx's autodoc
    import clr
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')
    clr.AddReference('System')

    from Autodesk.Revit import DB
    from Autodesk.Revit import UI
    from System.Collections.Generic import List

except Exception as errmsg:
    logger.error(errmsg)
    logger.error('Import Failed Using Fake Import')

try:
    uidoc = __revit__.ActiveUIDocument
    doc = __revit__.ActiveUIDocument.Document
    version = __revit__.Application.VersionNumber.ToString()
    platform = {'revit': version}
    logger.info("Running In Revit")

except NameError:
    print('Could not find pyRevit Document. Trying Dynamo.')
    try:
        clr.AddReference("RevitServices")
    except:
        print('Could not Revit Document')
        from rpw.sphinx_compat import *
    else:

        import RevitServices
        from RevitServices.Persistence import DocumentManager
        from RevitServices.Transactions import TransactionManager

        doc = DocumentManager.Instance.CurrentDBDocument
        uiapp = DocumentManager.Instance.CurrentUIApplication
        app = uiapp.Application
        uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
        version = app.VersionNumber.ToString()
        platform = {'dynamo': version}
        logger.info('Running in Dynamo')


# FIXME: Test this on test suite and dynamo
# IDEA: Re-think namespace imports: ie import forms only if wpf is found.
# TODO: Refactor this page

# Loads Modules into main rpw namespace
from rpw.selection import Selection
from rpw.collector import Collector, ParameterFilter
from rpw.transaction import Transaction
from rpw.element import Element, Parameter
from rpw.coerce import elements_to_element_ids
from rpw.forms import SelectFromList, TextInput
