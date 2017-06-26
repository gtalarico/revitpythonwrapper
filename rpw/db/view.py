"""
View Wrappers

"""  #

import rpw
from rpw import revit, DB
from rpw.db import Element
from rpw.db import FamilyInstance, Symbol, Family, Category
from rpw.base import BaseObjectWrapper
from rpw.utils.logger import logger
from rpw.db.builtins import BipEnum


class ViewInstance(Element):
    """
    Inherits base ``Instance`` and overrides symbol attribute to
    get `Symbol` equivalent of Wall `(GetTypeId)`
    """

    _revit_object_category = DB.BuiltInCategory.OST_Views
    _revit_object_class = DB.View
    _collector_params = {'of_class': _revit_object_class, 'is_type': False}

    @property
    def siblings(self):
        raise NotImplemented

    @property
    def view_type(self):
        return Element(self._revit_object.ViewType)


class ViewType(Element):
    _revit_object_category = DB.BuiltInCategory.OST_Views
    _revit_object_class = DB.View
    _collector_params = {'of_class': _revit_object_class, 'is_type': True}

    @property
    def views(self):
        return Element(self._revit_object.ViewType)

    @property
    def view_family(self):
        return Element(self._revit_object.ViewFamily)

class ViewFamily(BaseObjectWrapper):
    # _revit_object_category = DB.BuiltInCategory.OST_Views
    _revit_object_class = DB.ViewFamily
    _collector_params = {'of_class': _revit_object_class, 'is_type': True}
