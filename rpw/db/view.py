"""
View Wrappers

"""  #

import rpw
from rpw import revit, DB
from rpw.db import Element
from rpw.base import BaseObjectWrapper
from rpw.utils.logger import logger
from rpw.utils.dotnet import Enum
from rpw.db.builtins import BipEnum


class View(Element):
    """
    This is the master View Class. All other View classes inherit
    from DB.View

    This is also used for some Types: Legend, ProjectBrowser, SystemBrowser
    """

    _revit_object_category = DB.BuiltInCategory.OST_Views
    _revit_object_class = DB.View
    _collector_params = {'of_class': _revit_object_class, 'is_type': False}

    @property
    def name(self):
        # TODO: Make Mixin ?
        return self._revit_object.Name

    @name.setter
    def name(self, value):
        self._revit_object.Name == value

    @property
    def view_type(self):
        return self._revit_object.ViewType

    @property
    def view_family_type(self):
        view_type_id = self._revit_object.GetTypeId()
        return Element(self.doc.GetElement(view_type_id))

    # def __repr__(self):
    #     return super(View, self).__repr__(data={'view_name': self.name,
    #                                             'view_family_type': self.view_family_type.name,
    #                                             'view_type': self.view_type,
    #                                             })


# ViewPlanType
class ViewPlan(View):
    _revit_object_class = DB.ViewPlan
    _collector_params = {'of_class': _revit_object_class, 'is_type': False}

    @property
    def level(self):
        return self._revit_object.GenLevel


class ViewSheet(View):
    """ View where ``ViewType`` is ViewType.DrawingSheet """
    _revit_object_class = DB.ViewSheet
    _collector_params = {'of_class': _revit_object_class, 'is_type': False}


class ViewSchedule(View):
    """ View where ``ViewType`` is ViewType.DrawingSheet """
    _revit_object_class = DB.ViewSchedule
    _collector_params = {'of_class': _revit_object_class, 'is_type': False}


class ViewSection(View):
    """ View where ``ViewType`` is ViewType.DrawingSheet """
    _revit_object_class = DB.ViewSection
    _collector_params = {'of_class': _revit_object_class, 'is_type': False}


class ViewSchedule(View):
    _revit_object_class = DB.ViewSchedule
    _collector_params = {'of_class': _revit_object_class, 'is_type': False}

class View3D(View):
    _revit_object_class = DB.View3D
    _collector_params = {'of_class': _revit_object_class, 'is_type': False}


class ViewFamilyType(Element):
    """ View Family Type Wrapper """
    _revit_object_class = DB.ViewFamilyType
    _collector_params = {'of_class': _revit_object_class, 'is_type': True}

    def name(self):
        return Element.Name.GetValue(self._revit_object)

    @property
    def view_family(self):
        """ Returns ViewFamily Enumerator """
        # Autodesk.Revit.DB.ViewFamily.FloorPlan
        return self._revit_object.ViewFamily


    # def __repr__(self):
    #     return super(ViewFamilyType, self).__repr__(data={'name': self.name,
    #                                                       'type': self.view_family})

class ViewFamily(BaseObjectWrapper):
    """ Enumerator for ViewFamily

    This is returned on view.ViewFamily
    AreaPlan, CeilingPlan, CostReport
    Detail, Drafting, Elevation
    FloorPlan, GraphicalColumnSchedule, ImageView, Legend
    LoadsReport, PanelSchedule, PressureLossReport
    Schedule, Section, Sheet, StructuralPlan
    ThreeDimensional, Walkthrough
    """

class ViewType(BaseObjectWrapper):
    """ View Type Wrapper .

    Can be on of the following types:
        AreaPlan ,CeilingPlan, ColumnSchedule, CostReport,
        Detail, DraftingView, DrawingSheet, Elevation, EngineeringPlan,
        FloorPlan, Internal, Legend,
        LoadsReport, PanelSchedule, PresureLossReport,
        ProjectBrowser, Rendering, Report,
        Schedule, Section, SystemBrowser,
        ThreeD, Undefined, Walkthrough
    """
    _revit_object_class = DB.ViewType

    @property
    def views(self):
        return Element(self._revit_object.ViewType)


class ViewPlanType(BaseObjectWrapper):
    """
    Enumerator
        FloorPlan, CeilingPlan
    """
