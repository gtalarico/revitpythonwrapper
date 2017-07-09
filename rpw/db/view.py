"""
View Wrappers

"""  #

import rpw
from rpw import revit, DB
from rpw.db.element import Element
from rpw.db.pattern import LinePatternElement, FillPatternElement
from rpw.db.collector import Collector
from rpw.base import BaseObjectWrapper
from rpw.utils.coerce import to_element_ids, to_element_id, to_element
from rpw.utils.coerce import to_category_id, to_iterable
from rpw.exceptions import RpwTypeError, RpwCoerceError
from rpw.utils.logger import logger


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
        """ Access to overrides.

        For more information see :any:`OverrideGraphicSettings`

        >>> view.override.projection_line(element, color=[0,255,0])
        >>> view.override.cut_line(category, weight=5)

        """
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
    >>> wrapped_view.override.projection_line(target, color=(255,0,0))
    >>> wrapped_view.override.projection_fill(target, color=(0,0,255), pattern=pattern_id)
    >>> wrapped_view.override.cut_line(target, color=(0,0,255), weight=2)
    >>> wrapped_view.override.cut_fill(target, visible=False)
    >>> wrapped_view.override.transparency(target, 50)
    >>> wrapped_view.override.halftone(target, True)
    >>> wrapped_view.override.detail_level(target, 'Coarse')

    Note:
        Target can be any of the following:

        * Element
        * ElementId
        * BuiltInCategory Enum
        * BuiltInCategory Fuzzy Name (See :any:`BiCategory.fuzzy_get`)
        * Category_id
        * An iterable containing any of the above types

    """

    # TODO: Pattern: Add pattern_id from name. None sets InvalidElementId
    # TODO: Weight: None to set InvalidPenNumber
    # TODO: Color: Add color from name util
    # TODO: Add tests

    _revit_object_class = DB.OverrideGraphicSettings

    def __init__(self, wrapped_view):
        super(OverrideGraphicSettings, self).__init__(DB.OverrideGraphicSettings())
        self.view = wrapped_view.unwrap()

    def _set_overrides(self, target):
        targets = to_iterable(target)
        for target in targets:
            try:
                category_id = to_category_id(target)
                self._set_category_overrides(category_id)
            except (RpwTypeError, RpwCoerceError) as errmsg:
                logger.debug('Not Category, Trying Element Override')
                element_id = to_element_id(target)
                self._set_element_overrides(element_id)

    # @rpw.db.Transaction.ensure('Set OverrideGraphicSettings')
    def _set_element_overrides(self, element_id):
        self.view.SetElementOverrides(element_id, self._revit_object)

    def _set_category_overrides(self, category_id):
        self.view.SetCategoryOverrides(category_id, self._revit_object)

    def match_element(self, target, element_to_match):
        """
        Matches the settings of another element

        Args:
            target (``Element``, ``ElementId``, ``Category``): Target Element(s) or Category(ies) to apply override. Can be list.
            element_to_match (``Element``, ``ElementId``): Element to match
        """
        element_to_match = to_element_id(element_to_match)

        self._revit_object = self.view.GetElementOverrides(element_to_match)
        self._set_overrides(target)

    def projection_line(self, target, color=None, pattern=None, weight=None):
        """
        Sets ProjectionLine overrides

        Args:
            target (``Element``, ``ElementId``, ``Category``): Target Element(s) or Category(ies) to apply override. Can be list.
            color (``tuple``, ``list``): RGB Colors [ex. (255, 255, 0)]
            pattern (``DB.ElementId``): ElementId of Pattern
            weight (``int``,``None``): Line weight must be a positive integer less than 17 or None(sets invalidPenNumber)
        """
        if color:
            Color = DB.Color(*color)
            self._revit_object.SetProjectionLineColor(Color)
        if pattern:
            line_pattern = LinePatternElement.by_name_or_element_ref(pattern)
            self._revit_object.SetProjectionLinePatternId(line_pattern.Id)
        if weight:
            self._revit_object.SetProjectionLineWeight(weight)

        self._set_overrides(target)

    def cut_line(self, target, color=None, pattern=None, weight=None):
        """
        Sets CutLine Overrides

        Args:
            target (``Element``, ``ElementId``, ``Category``): Target Element(s) or Category(ies) to apply override. Can be list.
            color (``tuple``, ``list``): RGB Colors [ex. (255, 255, 0)]
            pattern (``DB.ElementId``): ElementId of Pattern
            weight (``int``,``None``): Line weight must be a positive integer less than 17 or None(sets invalidPenNumber)
        """
        if color:
            Color = DB.Color(*color)
            self._revit_object.SetCutLineColor(Color)
        if pattern:
            line_pattern = LinePatternElement.by_name_or_element_ref(pattern)
            self._revit_object.SetCutLinePatternId(line_pattern.Id)
        if weight:
            self._revit_object.SetCutLineWeight(weight)

        self._set_overrides(target)

    def projection_fill(self, target, color=None, pattern=None, visible=None):
        """
        Sets ProjectionFill overrides

        Args:
            target (``Element``, ``ElementId``, ``Category``): Target Element(s) or Category(ies) to apply override. Can be list.
            color (``tuple``, ``list``): RGB Colors [ex. (255, 255, 0)]
            pattern (``DB.ElementId``): ElementId of Pattern
            visible (``bool``): Cut Fill Visibility
        """
        if color:
            Color = DB.Color(*color)
            self._revit_object.SetProjectionFillColor(Color)
        if pattern:
            fill_pattern = FillPatternElement.by_name_or_element_ref(pattern)
            self._revit_object.SetProjectionFillPatternId(fill_pattern.Id)
        if visible is not None:
            self._revit_object.SetProjectionFillPatternVisible(visible)

        self._set_overrides(target)

    def cut_fill(self, target, color=None, pattern=None, visible=None):
        """
        Sets CutFill overrides

        Args:
            target (``Element``, ``ElementId``, ``Category``): Target Element(s) or Category(ies) to apply override. Can be list.
            color (``tuple``, ``list``): RGB Colors [ex. (255, 255, 0)]
            pattern (``DB.ElementId``): ElementId of Pattern
            visible (``bool``): Cut Fill Visibility
        """

        if color:
            Color = DB.Color(*color)
            self._revit_object.SetCutFillColor(Color)
        if pattern:
            fill_pattern = FillPatternElement.by_name_or_element_ref(pattern)
            self._revit_object.SetCutFillPatternId(fill_pattern.Id)
        if visible is not None:
            self._revit_object.SetCutFillPatternVisible(visible)

        self._set_overrides(target)

    def transparency(self, target, transparency):
        """
        Sets SurfaceTransparency override

        Args:
            target (``Element``, ``ElementId``, ``Category``): Target Element(s) or Category(ies) to apply override. Can be list.
            transparency (``int``): Value of the transparency of the projection surface (0 = opaque, 100 = fully transparent)
        """
        self._revit_object.SetSurfaceTransparency(transparency)
        self._set_overrides(target)

    def halftone(self, target, halftone):
        """
        Sets Halftone Override

        Args:
            target (``Element``, ``ElementId``, ``Category``): Target Element(s) or Category(ies) to apply override. Can be list.
            halftone (``bool``): Halftone
        """
        self._revit_object.SetHalftone(halftone)
        self._set_overrides(target)

    def detail_level(self, target, detail_level):
        """
        Sets DetailLevel Override. DetailLevel can be Enumeration memeber of
        DB.ViewDetailLevel or its name as a string. The Options are:

            * Coarse
            * Medium
            * Fine

        Args:
            target (``Element``, ``ElementId``, ``Category``): Target Element(s) or Category(ies) to apply override. Can be list.
            detail_level (``DB.ViewDetailLevel``, ``str``): Detail Level Enumerator or name
        """

        if isinstance(detail_level, str):
            detail_level = getattr(DB.ViewDetailLevel, detail_level)

        self._revit_object.SetDetailLevel(detail_level)
        self._set_overrides(target)
