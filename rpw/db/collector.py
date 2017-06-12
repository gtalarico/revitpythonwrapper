"""
>>> levels = rpw.db.Collector(of_category='OST_Levels', is_no_type=True)

>>> # Traditional
>>> levels = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType()

"""

import types

from rpw.revit import revit, DB
from rpw.utils.dotnet import List
from rpw.base import BaseObjectWrapper, BaseObject
from rpw.exceptions import RPW_Exception, RPW_TypeError, RPW_CoerceError
from rpw.db.element import Element
from rpw.db.builtins import BicEnum, BipEnum
from rpw.utils.coerce import to_element_id, to_element_ids
from rpw.utils.coerce import to_category, to_class
from rpw.utils.logger import logger

# More Info on Performance
# http://thebuildingcoder.typepad.com/blog/2015/12/quick-slow-and-linq-element-filtering.html


class BaseFilter(BaseObject):
    """ Base Filter and Apply Logic """

    method = 'WherePasses'

    @classmethod
    def apply(cls, doc, collector, value):
        method_name = cls.method
        method = getattr(collector, method_name)
        if hasattr(cls, 'process_value'):

            # FamilyInstanceFilter is the only Filter that  requires Doc
            if cls is not FilterClasses.FamilyInstanceFilter:
                value = cls.process_value(value)
            else:
                value = cls.process_value(value, doc)

        return method(value)


class SuperQuickFilter(BaseFilter):
    """ Preferred Quick """
    priority_group = 0


class QuickFilter(BaseFilter):
    """ Typical Quick """
    priority_group = 1


class SlowFilter(BaseFilter):
    """ Typical Slow """
    priority_group = 2


class SuperSlowFilter(BaseFilter):
    """ Leave it for Last! """
    priority_group = 3


class FilterClasses():
    """ Groups FilterClasses to facilitate discovery."""

    @classmethod
    def get_available_filters(cls):
        """ Discover all Defined Filter Classes """
        filters = []
        for filter_class_name in dir(FilterClasses):
            if filter_class_name.endswith('Filter'):
                filters.append(getattr(FilterClasses, filter_class_name))
        return filters

    @classmethod
    def get_sorted(cls):
        """ Returns Defined Filter Classes sorted by priority """
        return sorted(FilterClasses.get_available_filters(),
                      key=lambda f: f.priority_group)

    class ClassFilter(SuperQuickFilter):
        keyword = 'of_class'

        @classmethod
        def process_value(cls, class_reference):
            class_ = to_class(class_reference)
            return DB.ElementClassFilter(class_)

    class CategoryFilter(SuperQuickFilter):
        keyword = 'of_category'

        @classmethod
        def process_value(cls, category_reference):
            category = to_category(category_reference)
            return DB.ElementCategoryFilter(category)

    class IsTypeFilter(QuickFilter):
        keyword = 'is_type'

        @classmethod
        def process_value(cls, bool_value):
            return DB.ElementIsElementTypeFilter(not(bool_value))

    class IsNotTypeFilter(IsTypeFilter):
        keyword = 'is_not_type'

        @classmethod
        def process_value(cls, bool_value):
            return DB.ElementIsElementTypeFilter(bool_value)

    class FamilySymbolFilter(QuickFilter):
        keyword = 'family'

        @classmethod
        def process_value(cls, family_reference):
            family_id = to_element_id(family_reference)
            return DB.FamilySymbolFilter(family_id)

    class ViewOwnerFilter(QuickFilter):
        keyword = 'owner_view'
        reverse = False

        @classmethod
        def process_value(cls, view_reference):
            if view_reference is not None:
                view_id = to_element_id(view_reference)
            else:
                view_id = DB.ElementId.InvalidElementId
            return DB.ElementOwnerViewFilter(view_id, cls.reverse)

    class ViewIndependentFilter(QuickFilter):
        keyword = 'is_view_independent'

        @classmethod
        def process_value(cls, bool_value):
            view_id = DB.ElementId.InvalidElementId
            return DB.ElementOwnerViewFilter(view_id, not(bool_value))

    class CurveDrivenFilter(QuickFilter):
        keyword = 'is_curve_driven'

        @classmethod
        def process_value(cls, bool_value):
            return DB.ElementIsCurveDrivenFilter(not(bool_value))

    class FamilyInstanceFilter(SlowFilter):
        keyword = 'symbol'

        @classmethod
        def process_value(cls, symbol_reference, doc):
            symbol_id = to_element_id(symbol_reference)
            return DB.FamilyInstanceFilter(doc, symbol_id)

    class LevelFilter(SlowFilter):
        keyword = 'level'
        reverse = False

        @classmethod
        def process_value(cls, level_reference):
            # TODO: Move this into Level Wrapper - Level.collect(name='')
            # Handle filter by level name
            if isinstance(level_reference, str):
                level = Collector(of_class='Level', is_type=False,
                                  where=lambda x:
                                  x.Name == level_reference)
                try:
                    level_id = level[0].Id
                except IndexError:
                    RPW_CoerceError(level_reference, DB.Level)
            else:
                level_id = to_element_id(level_reference)
            return DB.ElementLevelFilter(level_id, cls.reverse)

    class NotLevelFilter(LevelFilter):
        keyword = 'not_level'
        reverse = True

    class ParameterFilter(SlowFilter):
        keyword = 'parameter_filter'

        @classmethod
        def process_value(cls, parameter_filter):
            if isinstance(parameter_filter, ParameterFilter):
                return parameter_filter.unwrap()
            else:
                raise Exception('Shouldnt get here')

    class WhereFilter(SuperSlowFilter):
        """ Requires Unpacking of each Element. As per the API design,
        this filter must be combined """
        keyword = 'where'
        # w = rpw.db.Collector(of_category='Walls', is_type=False, where=lambda x: x.LookupParameter('Length').AsDouble() > 5 )
        # rpw.db.Collector(of_class='FamilyInstance', where=lambda x: 'Student' in x.name)
        @classmethod
        def apply(cls, doc, collector, func):
            excluded_elements = set()
            for element in collector:
                wrapped_element = Element(element)
                if not func(wrapped_element):
                    excluded_elements.add(element.Id)
            excluded_elements = List[DB.ElementId](excluded_elements)
            if excluded_elements:
                return collector.Excluding(excluded_elements)
            else:
                return collector


class Collector(BaseObjectWrapper):
    """
    Revit FilteredElement Collector Wrapper

    Usage:
        >>> collector = Collector(of_class='View')
        >>> elements = collector.elements

        Multiple Filters:

        >>> Collector(of_class='Wall', is_not_type=True)
        >>> Collector(of_class='ViewSheet', is_not_type=True)
        >>> Collector(of_category='OST_Rooms', level=some_level)
        >>> Collector(symbol=SomeSymbol)
        >>> Collector(owner_view=SomeView)
        >>> Collector(owner_view=None)
        >>> Collector(parameter_filter=parameter_filter)

        Use Enumeration member or its name as a string:

        >>> Collector(of_category='OST_Walls')
        >>> Collector(of_category=DB.BuiltInCategory.OST_Walls)
        >>> Collector(of_class=DB.ViewType)
        >>> Collector(of_class='ViewType')

        Search Document, View, or list of elements

        >>> Collector(of_category='OST_Walls') # doc is default
        >>> Collector(view=SomeView, of_category='OST_Walls') # Doc is default
        >>> Collector(doc=SomeLinkedDoc, of_category='OST_Walls')
        >>> Collector(elements=[Element1, Element2,...], of_category='OST_Walls')
        >>> Collector(owner_view=SomeView)
        >>> Collector(owner_view=None)

    Attributes:
        collector.elements: Returns list of all `collected` elements
        collector.first: Returns first found element, or ``None``
        collector.wrapped_elements: Returns list with all elements wrapped. Elements will be instantiated using :any:`Element.Factory`

    Wrapped Element:
        self._revit_object = ``Revit.DB.FilteredElementCollector``

    """

    _revit_object_class = DB.FilteredElementCollector

    def __init__(self, **filters):
        """
        Args:
            **filters (``keyword args``): Scope and filters

        Returns:
            Collector (:any:`Collector`): Collector Instance

        Scope Options:
            * ``view`` `(DB.View)`: View Scope (Optional)
            * ``element_ids`` `([ElementId])`: List of Element Ids to limit Collector Scope
            * ``elements`` `([Element])`: List of Elements to limit Collector Scope

        Warning:
            Only one scope filter should be used per query. If more then one is used,
            only one will be applied, in this order ``view`` > ``elements`` > ``element_ids``

        Filter Options:
            * ``is_type`` (``bool``): Same as ``WhereElementIsElementType``
            * ``is_not_type`` (``bool``): Same as ``WhereElementIsNotElementType``
            * ``of_class`` (``Type``): Same as ``OfClass``. Type can be ``DB.SomeType`` or string: ``DB.Wall`` or ``'Wall'``
            * ``of_category`` (``BuiltInCategory``): Same as ``OfCategory``. Type can be Enum member or String: ``DB.BuiltInCategory.OST_Wall`` or ``OST_Wall``
            * ``owner_view`` (``DB.ElementId, View`): ``WhereElementIsViewIndependent(True)``
            * ``is_view_independent`` (``bool``): ``WhereElementIsViewIndependent(True)``
            * ``symbol`` (``DB.ElementId``, ``DB.Element``)`: Element or ElementId of Symbol
            * ``level`` (``DB.Level``, ``DB.ElementId``, ``Level Name``)`: Level, ElementId of Level, or Level Name
            * ``not_level`` (``DB.Level``, ``DB.ElementId``, ``Level Name``)`: Level, ElementId of Level, or Level Name
            * ``parameter_filter`` (:any:`ParameterFilter`): Similar to ``ElementParameterFilter`` Class

        """
        # Define Filtered Element Collector Scope + Doc
        collector_doc = filters.pop('doc') if 'doc' in filters else revit.doc

        if 'view' in filters:
            view = filters.pop('view')
            view_id = view if isinstance(view, DB.ElementId) else view.Id
            collector = DB.FilteredElementCollector(collector_doc, view_id)
        elif 'elements' in filters:
            elements = filters.pop('elements')
            element_ids = to_element_ids(elements)
            collector = DB.FilteredElementCollector(collector_doc, List[DB.ElementId](element_ids))
        elif 'element_ids' in filters:
            element_ids = filters.pop('element_ids')
            collector = DB.FilteredElementCollector(collector_doc, List[DB.ElementId](element_ids))
        else:
            collector = DB.FilteredElementCollector(collector_doc)

        super(Collector, self).__init__(collector)

        for key in filters.keys():
            if key not in [f.keyword for f in FilterClasses.get_sorted()]:
                raise RPW_Exception('Collector Filter not valid: {}'.format(key))

        self._collector = self._collect(collector_doc, collector, filters)

    def _collect(self, doc, collector, filters):
        for filter_class in FilterClasses.get_sorted():
            if filter_class.keyword not in filters:
                continue
            filter_value = filters.pop(filter_class.keyword)
            logger.debug('Applying Filter: {}'.format(filter_class))
            new_collector = filter_class.apply(doc, collector, filter_value)
            return self._collect(doc, new_collector, filters)
        return collector

    # #CLEAN MOVED TO WHERE FILTER
    # def filter(self, func, wrapped=True):
    #     #  rpw.db.Collector(of_category='Walls', is_type=False).filter(lambda x: x.LookupParameter('Length').AsDouble() > 5 )
    #     #  rpw.db.Collector(of_category='Walls', is_type=False).filter(lambda x: x.parameters['Length'] < 5 )
    #     #  rpw.db.Family.collect().filter(lambda x: x.Name == 'desk' )
    #     if not isinstance(func, types.FunctionType):
    #         raise RPW_TypeError(types.FunctionType, type(func))
    #
    #     passing_elements = []
    #     for element in self:
    #         element = Element(element) if wrapped else element
    #         if func(element):
    #             passing_elements.append(element)
    #
    #     return passing_elements

    def __iter__(self):
        """ Uses iterator to reduce unecessary memory usage """
        for element in self._collector:
            yield element

    @property
    def elements(self):
        """ Returns list with all elements instantiated using :any:`Element.Factory`
        """
        return [element for element in self.__iter__()]

    @property
    def wrapped_elements(self):
        """ Returns list with all elements instantiated using :any:`Element.Factory`
        """
        return [Element(el) for el in self.__iter__()]


    @property
    def first(self):
        """ TODO
        """
        try:
            return self[0]
        except IndexError:
            return None

    @property
    def element_ids(self):
        """ Returns list with all elements instantiated using :any:`Element.Factory`
        """
        return [element_id for element_id in self._collector.ToElementIds()]

    def __getitem__(self, index):
        for n, element in enumerate(self.__iter__()):
            if n == index:
                return element
        else:
            raise IndexError('Index {} does not exist in collector {}'.format(index, self))

    def __bool__(self):
        """ Evaluates to `True` if Collector.elements is not empty [] """
        return bool(self.elements)

    def __len__(self):
        """ Returns length of collector.elements """
        return self._collector.GetElementCount()

    def __repr__(self):
        return super(Collector, self).__repr__(data={'count':len(self)})


class ParameterFilter(BaseObjectWrapper):
    """ Parameter Filter Wrapper.
    Used to build a parameter filter to be used with the Collector.

    Usage:
        >>> param_id = DB.ElemendId(DB.BuiltInParameter.TYPE_NAME)
        >>> parameter_filter = ParameterFilter(param_id, equals='Wall 1')
        >>> collector = Collector(parameter_filter=parameter_filter)

    Returns:
        FilterRule: A filter rule object, depending on arguments.
    """
    _revit_object_class = DB.ElementParameterFilter

    RULES = {
            'equals': 'CreateEqualsRule',
            'not_equals': 'CreateEqualsRule',
            'contains': 'CreateContainsRule',
            'not_contains': 'CreateContainsRule',
            'begins': 'CreateBeginsWithRule',
            'not_begins': 'CreateBeginsWithRule',
            'ends': 'CreateEndsWithRule',
            'not_ends': 'CreateEndsWithRule',
            'greater': 'CreateGreaterRule',
            'not_greater': 'CreateGreaterRule',
            'greater_equal': 'CreateGreaterOrEqualRule',
            'not_greater_equal': 'CreateGreaterOrEqualRule',
            'less': 'CreateLessRule',
            'not_less': 'CreateLessRule',
            'less_equal': 'CreateLessOrEqualRule',
            'not_less_equal': 'CreateLessOrEqualRule',
           }

    CASE_SENSITIVE = True
    FLOAT_PRECISION = 0.0013020833333333

    def __init__(self, parameter_reference, **conditions):
        """
        Creates Parameter Filter Rule

        >>> param_rule = ParameterFilter(param_id, equals=2)
        >>> param_rule = ParameterFilter(param_id, not_equals='a', case_sensitive=True)
        >>> param_rule = ParameterFilter(param_id, not_equals=3, reverse=True)

        Args:
            param_id(DB.ElementID): ElemendId of parameter
            **conditions: Filter Rule Conditions and options.

            conditions:
                | ``equals``
                | ``contains``
                | ``begins``
                | ``ends``
                | ``greater``
                | ``greater_equal``
                | ``less``
                | ``less_equal``
                | ``not_equals``
                | ``not_contains``
                | ``not_begins``
                | ``not_ends``
                | ``not_greater``
                | ``not_greater_equal``
                | ``not_less``
                | ``not_less_equal``

            options:
                | ``case_sensitive``: Enforces case sensitive, String only
                | ``reverse``: Reverses result of Collector

        """
        parameter_id = self.coerce_param_reference(parameter_reference)
        reverse = conditions.get('reverse', False)
        case_sensitive = conditions.get('case_sensitive', ParameterFilter.CASE_SENSITIVE)
        precision = conditions.get('precision', ParameterFilter.FLOAT_PRECISION)

        for condition in conditions.keys():
            if condition not in ParameterFilter.RULES:
                raise RPW_Exception('Rule not valid: {}'.format(condition))

        rules = []
        for condition_name, condition_value in conditions.iteritems():

            # Returns on of the CreateRule factory method names above
            rule_factory_name = ParameterFilter.RULES.get(condition_name)
            filter_value_rule = getattr(DB.ParameterFilterRuleFactory, rule_factory_name)

            args = [condition_value]

            if isinstance(condition_value, str):
                args.append(case_sensitive)

            if isinstance(condition_value, float):
                args.append(precision)

            filter_rule = filter_value_rule(parameter_id, *args)
            if 'not_' in condition_name:
                filter_rule = DB.FilterInverseRule(filter_rule)
            ##################################################################
            # FILTER DEBUG INFO - TODO: MOVE TO FUNCTION
            ##################################################################
            # logger.critical('Conditions: {}'.format(conditions))
            # logger.critical('Case sensitive: {}'.format(case_sensitive))
            # logger.critical('Reverse: {}'.format(self.reverse))
            # logger.critical('ARGS: {}'.format(args))
            # logger.critical(filter_rule)
            # logger.critical(str(dir(filter_rule)))
            ##################################################################
            rules.append(filter_rule)
        if not rules:
            raise RPW_Exception('malformed filter rule: {}'.format(conditions))

        _revit_object = DB.ElementParameterFilter(List[DB.FilterRule](rules), reverse)
        super(ParameterFilter, self).__init__(_revit_object)
        self.conditions = conditions

    def coerce_param_reference(self, parameter_reference):
        if isinstance(parameter_reference, str):
            param_id = BipEnum.get_id(parameter_reference)
        elif isinstance(parameter_reference, DB.ElementId):
            param_id = parameter_reference
        else:
            RPW_CoerceError(parameter_reference, ElementId)
        return param_id

    @staticmethod
    def from_element_and_parameter(element, param_name, **conditions):
        # TEST: parameter_filter from object+param name to skip having to get param_id
        #       basically an alternative constructor that takes elemement + parameter name
        #       instead of param_id, which is a pain in the ass
        #       >>> parameter_filter = ParameterFilter.from_element(element,param_name, less_than=10)
        parameter = element.LookupParameter(param_name)
        param_id = parameter.Id
        return ParameterFilter(param_id, **conditions)

    def __repr__(self):
        return super(ParameterFilter, self).__repr__(data=self.conditions)

# print("Collector Loaded")
