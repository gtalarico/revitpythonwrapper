"""

************************************
A Python Interface For the Revit API
************************************

Revit Python Wrapper allows you write Revit API Python code
that in a way that is more natural to the language.

Wrapper objects not only make the interaction with Revit API objects more
natural and consistent with Python's naming conventions, but also implement
patterns to make your code more conscise (DRY).

Goals:

* Normalize API calls for different Revit Version
* Normalize API calls for Revit Vs Dynamo to allow re-use
*

Please help improve the project by contributing with improvements, bugs,
and ideas.

Disclaimer
**********

Please keep in mind this is my first *public API*, so if you know better,
don't hesitate to enlighthen me.

I hope this is just the start of project that will help Python lovers
write better Revit API Code.


http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
https://github.com/kennethreitz/requests/blob/master/requests/api.py

"""

# TODO:
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
