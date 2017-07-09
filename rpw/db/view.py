"""
View Wrappers

"""  #

import rpw
from rpw import revit, DB
from rpw.db.element import Element
from rpw.db.pattern import LinePatternElement, FillPatternElement
from rpw.db.collector import Collector
from rpw.base import BaseObjectWrapper
from rpw.utils.coerce import to_element_ids, to_element_id, to_element, to_iterable
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
        return ViewType(self._revit_object.ViewType)

    @property
    def view_family_type(self):
        # NOTE: This can return Empty, as Some Views like SystemBrowser have no Type
        view_type_id = self._revit_object.GetTypeId()
        view_type = self.doc.GetElement(view_type_id)
        if view_type:
            return ViewFamilyType(self.doc.GetElement(view_type_id))

    @property
    def view_family(self):
        # Some Views don't have a ViewFamilyType
        return getattr(self.view_family_type, 'view_family', None)

    @property
    def siblings(self):
        return self.view_type.views

    @property
    def override(self):
        return OverrideGraphicSettings(self)

    def __repr__(self):
        return super(View, self).__repr__(data={'view_name': self.name,
                                                'view_family_type': getattr(self.view_family_type, 'name', None),
                                                'view_type': self.view_type.name,
                                                'view_family': getattr(self.view_family, 'name', None)
                                                })


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

    @property
    def name(self):
        # Could use the line below but would required re-importing element, as per
        # return DB.Element.Name.GetValue(self._revit_object)
        return self.parameters.builtins['SYMBOL_FAMILY_NAME_PARAM'].value

    @property
    def view_family(self):
        """ Returns ViewFamily Enumerator """
        # Autodesk.Revit.DB.ViewFamily.FloorPlan
        return ViewFamily(self._revit_object.ViewFamily)

    @property
    def views(self):
        # Collect All Views, Compare view_family of each view with self
        views = Collector(of_class='View').wrapped_elements
        return [view for view in views if getattr(view.view_family_type, '_revit_object', None) == self.unwrap()]



    def __repr__(self):
        return super(ViewFamilyType, self).__repr__(data={'name': self.name,
                                                          'view_family': self.view_family.name,
                                                          })

class ViewFamily(BaseObjectWrapper):
    """ ViewFamily Enumerator Wrapper.
    An enumerated type that corresponds to the type of a Revit view.

    This is returned on view.ViewFamily
    AreaPlan, CeilingPlan, CostReport
    Detail, Drafting, Elevation
    FloorPlan, GraphicalColumnSchedule, ImageView, Legend
    LoadsReport, PanelSchedule, PressureLossReport
    Schedule, Section, Sheet, StructuralPlan
    ThreeDimensional, Walkthrough
    """
    _revit_object_class = DB.ViewFamily

    @property
    def name(self):
        return self._revit_object.ToString()

    @property
    def views(self):
        # Collect All Views, Compare view_family of each view with self
        views = Collector(of_class='View').wrapped_elements
        return [view for view in views if getattr(view.view_family, '_revit_object', None) == self.unwrap()]


    def __repr__(self):
        return super(ViewFamily, self).__repr__(data={'family': self.name})



class ViewType(BaseObjectWrapper):
    """ ViewType Wrapper.
    An enumerated type listing available view types.

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
    def name(self):
        return self._revit_object.ToString()

    @property
    def views(self):
        views = Collector(of_class='View').wrapped_elements
        return [view for view in views if view.view_type.unwrap() == self.unwrap()]


    def __repr__(self):
        return super(ViewType, self).__repr__(data={'view_type': self.name})



class ViewPlanType(BaseObjectWrapper):
    """
    Enumerator
        ViewPlanType.FloorPlan, ViewPlanType.CeilingPlan
    No Wrapper Need. Enum is only used as arg for when creating ViewPlan
    """


class OverrideGraphicSettings(BaseObjectWrapper):

    """ Internal Wrapper for OverrideGraphicSettings

    >>> wrapped_view = rpw.db.Element(some_view)
    >>> wrapped_view.override.projection_line(element, color=(255,0,0))
    >>> wrapped_view.override.projection_fill(element, color=(0,0,255), pattern=pattern_id)
    >>> wrapped_view.override.cut_line(element, color=(0,0,255), weight=2)
    >>> wrapped_view.override.cut_fill(element, visible=False)
    >>> wrapped_view.override.transparency(element, 50)
    >>> wrapped_view.override.halftone(element, True)
    >>> wrapped_view.override.detail_level(element, 'Coarse')

    WIP NOTE: This could be embeded into View Class. Leaving it here as it
    could be re-used by other overrides (filters, templates, etc)
    """

    # TODO: Pattern: Add pattern_id from name. None sets InvalidElementId
    # TODO: Weight: None to set InvalidPenNumber
    # TODO: Color: Add color from name util
    # TODO: Add tests

    _revit_object_class = DB.OverrideGraphicSettings

    def __init__(self, wrapped_view):
        super(OverrideGraphicSettings, self).__init__(DB.OverrideGraphicSettings())
        self.view = wrapped_view.unwrap()

    # @rpw.db.Transaction.ensure('Set OverrideGraphicSettings')
    def _set_overrides(self, element_ids):
        for element_id in element_ids:
            self.view.SetElementOverrides(element_id, self._revit_object)

    def match(self, element_references, element_to_match):
        """
        Matches the settings of another object

        Args:
            element_references (``Element``, ``ElementId``): Element(s) to apply override
            element_to_match (``Element``, ``ElementId``): Element to match
        """
        element_ids = to_element_ids(element_references)
        element_to_match = to_element(element_to_match)

        self._revit_object = self.view.GetElementOverrides(element_to_match)
        self._set_overrides(element_ids)

    def projection_line(self, element_references, color=None, pattern=None, weight=None):
        """
        Sets ProjectionLine overrides

        Args:
            element_references (``Element``, ``ElementId``): Element(s) to apply override
            color (``tuple``, ``list``): RGB Colors [ex. (255, 255, 0)]
            pattern (``DB.ElementId``): ElementId of Pattern
            weight (``int``,``None``): Line weight must be a positive integer less than 17 or None(sets invalidPenNumber)
        """
        element_ids = to_element_ids(element_references)

        if color:
            Color = DB.Color(*color)
            self._revit_object.SetProjectionLineColor(Color)
        if pattern:
            line_pattern = LinePatternElement.by_name_or_element_ref(pattern)
            self._revit_object.SetProjectionLinePatternId(line_pattern.Id)
        if weight:
            self._revit_object.SetProjectionLineWeight(weight)

        self._set_overrides(element_ids)

    def cut_line(self, element_references, color=None, pattern=None, weight=None):
        """
        Sets CutLine Overrides

        Args:
            element_references (``Element``, ``ElementId``): Element(s) to apply override
            color (``tuple``, ``list``): RGB Colors [ex. (255, 255, 0)]
            pattern (``DB.ElementId``): ElementId of Pattern
            weight (``int``,``None``): Line weight must be a positive integer less than 17 or None(sets invalidPenNumber)
        """
        element_ids = to_element_ids(element_references)

        if color:
            Color = DB.Color(*color)
            self._revit_object.SetCutLineColor(Color)
        if pattern:
            line_pattern = LinePatternElement.by_name_or_element_ref(pattern)
            self._revit_object.SetCutLinePatternId(line_pattern.Id)
        if weight:
            self._revit_object.SetCutLineWeight(weight)

        self._set_overrides(element_ids)

    def projection_fill(self, element_references, color=None, pattern=None, visible=None):
        """
        Sets ProjectionFill overrides

        Args:
            element_references (``Element``, ``ElementId``): Element(s) to apply override
            color (``tuple``, ``list``): RGB Colors [ex. (255, 255, 0)]
            pattern (``DB.ElementId``): ElementId of Pattern
            visible (``bool``): Cut Fill Visibility
        """

        element_ids = to_element_ids(element_references)

        if color:
            Color = DB.Color(*color)
            self._revit_object.SetProjectionFillColor(Color)
        if pattern:
            fill_pattern = FillPatternElement.by_name_or_element_ref(pattern)
            self._revit_object.SetProjectionFillPatternId(fill_pattern.Id)
        if visible is not None:
            self._revit_object.SetProjectionFillPatternVisible(visible)

        self._set_overrides(element_ids)

    def cut_fill(self, element_references, color=None, pattern=None, visible=None):
        """
        Sets CutFill overrides

        Args:
            element_references (``Element``, ``ElementId``): Element(s) to apply override
            color (``tuple``, ``list``): RGB Colors [ex. (255, 255, 0)]
            pattern (``DB.ElementId``): ElementId of Pattern
            visible (``bool``): Cut Fill Visibility
        """
        element_ids = to_element_ids(element_references)

        if color:
            Color = DB.Color(*color)
            self._revit_object.SetCutFillColor(Color)
        if pattern:
            fill_pattern = FillPatternElement.by_name_or_element_ref(pattern)
            self._revit_object.SetCutFillPatternId(fill_pattern.Id)
        if visible is not None:
            self._revit_object.SetCutFillPatternVisible(visible)

        self._set_overrides(element_ids)

    def transparency(self, element_references, transparency):
        """
        Sets SurfaceTransparency override

        Args:
            element_references (``Element``, ``ElementId``): Element(s) to apply override
            transparency (``int``): Value of the transparency of the projection surface (0 = opaque, 100 = fully transparent)
        """
        element_ids = to_element_ids(element_references)
        self._revit_object.SetSurfaceTransparency(transparency)
        self._set_overrides(element_ids)

    def halftone(self, element_references, halftone):
        """
        Sets Halftone Override

        Args:
            element_references (``Element``, ``ElementId``): Element(s) to apply override
            halftone (``bool``): Halftone
        """
        element_ids = to_element_ids(element_references)
        self._revit_object.SetHalftone(halftone)
        self._set_overrides(element_ids)

    def detail_level(self, element_references, detail_level):
        """
        Sets DetailLevel Override. DetailLevel can be Enumeration memeber of
        DB.ViewDetailLevel or its name as a string. The Options are:

            * Coarse
            * Medium
            * Fine

        Args:
            element_references (``Element``, ``ElementId``): Element(s) to apply override
            detail_level (``DB.ViewDetailLevel``, ``str``): Detail Level Enumerator or name
        """
        element_ids = to_element_ids(element_references)

        if isinstance(detail_level, str):
            detail_level = getattr(DB.ViewDetailLevel, detail_level)

        self._revit_object.SetDetailLevel(detail_level)
        self._set_overrides(element_ids)
