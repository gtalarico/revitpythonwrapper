"""

************************************
A Python Interface For the Revit API
************************************

Revit Python Wrapper allows you write Revit API in Python code
that in a way that is more natural to the language.

Wrapper objects makes the interaction with Revit API objects more
consistent with Python's naming conventions, but also implement
patterns to make your code more conscise (DRY).

The wrapper will also normalize version specific calls so you can re-use
your code across Revit versions.


Project Goals
*************

* Normalize API calls for different Revit Version
* Normalize API calls for Revit Vs Dynamo to allow re-use
* Implement Resusable patterns reduce repetitive tasks
* Create wrappers to make common calls feel more **pythonic**


Code Examples
*************

Transactions:

    >>> # Traditional Transaction (API)
    >>> from Autodesk.Revit.DB import Transaction
    >>> from Autodesk.Revit.UI.UIApplication import ActiveUIDocument
    >>> doc = ActiveUIDocument.Document
    >>> transaction = Transaction(doc, 'Delete Object')
    >>> transaction.Start()
    >>> try:
    >>>     doc.Remove(SomeElementId)
    >>> except:
    >>>     transaction.RollBack()
    >>> else:
    >>>     transaction.Commit()

    >>> # Using Wrapper
    >>> from rpw.transaction import Transaction
    >>> from rpw import doc
    >>> with Transaction('Delete Object')
    >>>     doc.Remove(SomeElementId)


Selection:

    >>> from Autodesk.Revit.UI.UIApplication import ActiveUIDocument
    >>> uidoc = ActiveUIDocument
    >>> selection_ids = uidoc.Selection.GetElementIds()
    >>> selected = [doc.GetElemend(eid) for eid in selection_ids]

    >>> from rpw.selection import Selection
    >>> selection = Selection()
    >>> selection[0]
    < Autodesk.Revit.DB.Element >
    >>> selection.elements
    [< Autodesk.Revit.DB.Element >]


Element:

    >>> from rpw.wrappers import Element
    >>> element = Element(SomeRevitElement)
    >>> with Transaction('Set Comment Parameter'):
    >>>     element.parameters['Comments'].value = 'Some String'
    'Some String' set as parameter value
    >>> element.parameters['some value'].type
    `<type: string>`
    >>> element.parameters['some value'].value
    'Some String'
    >>> element.parameters.builtins['WALL_LOCATION_LINE'].value
    1

FilteredElementCollector:

    >>> from Autodesk.Revit.DB import FilteredElementCollector, WallType
    >>> collector = FilteredElementCollector()
    >>> walls = FilteredElementCollector.OfClass(WallType).ToElements()

    >>> # Using Wrapped
    >>> from rpw.collector import Collector
    >>> walls = Collector(of_class='WallType').elements


Disclaimer
**********

Please keep in mind this is my first *public API*, so if you know better,
don't hesitate to enlighthen me.

I hope this is just the start of project that to help Python lovers
have more fun writing Revit API Code.

Contribute
**********

Please help improve the project by contributing with improvements, bugs,
and ideas.


"""
# https://github.com/kennethreitz/requests/blob/master/requests/api.py
# http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html

# TODO:
#  - Move out Elements and Parameters
#  - Finder/Filter Tool*
#  - Documentation
#  - Dynamo Doc Manager + Transaction Manager


__title__ = 'revitpythonwrapper'
__version__ = '0.0.1'
__author__ = 'Gui Talarico'
__license__ = '?'
__copyright__ = '?'


import sys
from rpw.logger import logger

logger.verbose(True)

try:
    #  This is a workaround to fix Sphinx's autodoc
    import clr
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')
    clr.AddReference('System')
    from Autodesk.Revit import DB
    from Autodesk.Revit import UI
except:
    print('Import Failed Using Fake Import')
    from rpw.sphinx_compat import *

try:
    "Running In PyRevit"
    uidoc = __revit__.ActiveUIDocument
    doc = __revit__.ActiveUIDocument.Document
    version = __revit__.Application.VersionNumber

except NameError:
    logger.error('Could not pyRevit Document. Trying Dynamo.')
    try:
        "Running In PyRevit"
        clr.AddReference("RevitServices")
    except:
        logger.error('Could not Revit Document')
    else:
        import RevitServices
        from RevitServices.Persistence import DocumentManager

        doc = DocumentManager.Instance.CurrentDBDocument
        uiapp = DocumentManager.Instance.CurrentUIApplication
        app = uiapp.Application

        # Verify
        uidoc = uiapp.ActiveUIDocument

# from rpw.wrappers import *
