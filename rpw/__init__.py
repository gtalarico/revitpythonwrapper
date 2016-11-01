"""
### A Python Interface For the Revit API

Revit Python Wrapper allows you write Revit API Python code
that in a way that is more natural to the language.

Wrapper objects not only make the interaction with Revit API objects more
natural and consistent with Python's naming conventions, but also implement
patterns to make your code more conscise (DRY).

Please help improve the project by contributing with improvemnts, bugs,
and ideas.

### Disclaimer
Please keep in mind this is my first _public API_, so if you know better,
don't hesitate to enlighthen me.

I hope this is just the start of project that will help Python lovers
write better Revit API Code.

"""

__title__ = 'revitpythonwrapper'
__version__ = '0.0.1'
__author__ = 'Gui Talarico'
__license__ = 'Apache 2.0'
__copyright__ = ''

# See Doc style:
# https://github.com/kennethreitz/requests/blob/master/requests/api.py
import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from Autodesk.Revit.DB import Transaction, XYZ

try:
    "Running In PyRevit"
    uidoc = __revit__.ActiveUIDocument
    doc = __revit__.ActiveUIDocument.Document

except NameError:
    "Running In PyRevit"
    clr.AddReference("RevitServices")
    import RevitServices
    from RevitServices.Persistence import DocumentManager

    doc = DocumentManager.Instance.CurrentDBDocument
    uiapp = DocumentManager.Instance.CurrentUIApplication
    app = uiapp.Application

    # Verify
    uidoc = uiapp.ActiveUIDocument

# from rpw.wrappers import *
