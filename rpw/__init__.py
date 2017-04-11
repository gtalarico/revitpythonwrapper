__title__ = 'revitpythonwrapper'
__version__ = '0.0.97'
__maintainer__ = 'Gui Talarico'
__license__ = 'MIT'
__contact__ = 'github.com/gtalarico/revitpythonwrapper'

import sys
from rpw.utils.logger import logger

try:
    #  This is a workaround to fix Sphinx's autodoc
    import clr
    clr.AddReference('RevitAPI')
    clr.AddReference('RevitAPIUI')
    clr.AddReference('System')

    from Autodesk.Revit import DB
    from Autodesk.Revit import UI
    from System.Collections.Generic import List
    from System import Enum

except Exception as errmsg:
    logger.error(errmsg)
    platform = {'testing': True}
    logger.warning('Could not Revit Document. Will Import Sphinx Compat Vars')
    from rpw.utils.sphinx_compat import *

# Imported Revit's Assemblies
else:
    try:
        uidoc = __revit__.ActiveUIDocument
        doc = __revit__.ActiveUIDocument.Document
        version = __revit__.Application.VersionNumber.ToString()
        platform = {'revit': version}
        logger.debug("Running In Revit")

    except NameError:
        logger.debug('Could not find pyRevit Document. Trying Dynamo.')
        try:
            clr.AddReference("RevitServices")
        except:
            raise Exception('Could Not Find Dynamo Services')
        else:
            # Adds Built in Library for Dynamo
            sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')

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


if platform is not None or platform.get('testing'):
    from rpw.base import BaseObjectWrapper
    from rpw.element import Element, Instance, Symbol, Family, Category
    from rpw.element import WallInstance, WallSymbol, WallFamily, WallCategory
    from rpw.element import Room, Area
    from rpw.parameter import ParameterSet, Parameter
    from rpw.selection import Selection
    from rpw.collector import Collector, ParameterFilter
    from rpw.transaction import Transaction, TransactionGroup
    from rpw.utils.logger import logger
    # from rpw.enumeration import BipEnum, BicEnum
    # from rpw.utils.coerce import to_element_ids, to_elements

    try:
        import forms
    except ImportError as errmsg:
        logger.critical('Could Not load Forms dependencies')
        logger.warning(errmsg)
