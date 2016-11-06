from copy import copy
from functools import reduce

from rpw import uidoc, doc, DB
from rpw.logger import logger
from rpw.base import BaseObjectWrapper
from rpw.enumeration import BuiltInCategoryEnum

from System.Collections.Generic import List


class Collector(BaseObjectWrapper):
    """
    Revit FilteredElement Collector Wrapper

    Usage:
        >>> collector = Collector()
        >>> elements = collector.filter(of_class=View)

        Multiple Filters:

        >>> collector = Collector()
        >>> elements = collector.filter(of_category=BuiltInCategory.OST_Walls,
                                        is_element_type=True)

        Chain Preserves Previous Results:

        >>> collector = Collector()
        >>> walls = collector.filter(of_category=BuiltInCategory.OST_Walls)
        >>> walls.filter(is_element_type=True)

        Use Enumeration member or string shortcut:

        >>> collector.filter(of_category='OST_Walls')
        >>> collector.filter(of_category='ViewType')

    Returns:
        Collector: Returns collector Class

    Attributes:
        collector.elements: Returns list of all *collected* elements
        collector.first: Returns first found element, or `None`

    Wrapped Element:
        self._revit_object = `Revit.DB.FilteredElementCollector`

    """

    def __init__(self, **filters):
        """
        Args:
            view (Revit.DB.View) = View Scope (Optional)
        """
        if 'view' in filters:
            view = filters['view']
            collector = DB.FilteredElementCollector(doc, view.Id)
        else:
            collector = DB.FilteredElementCollector(doc)
        super(Collector, self).__init__(collector)

        self.elements = []
        self._filters = filters

        self.filter = _Filter(self)
        # Allows Class to Excecute on Construction, if filters are present.
        if filters:
            self.filter(**filters)

    @property
    def first(self):
        """ Returns the first element in collector, or None"""
        try:
            return self.elements[0]
        except IndexError:
            return None

    def __bool__(self):
        """ Evaluates to `True` if Collector.elements is not empty [] """
        return bool(self.elements)

    def __len__(self):
        """ Returns length of collector.elements """
        return len(self.elements)

    def __repr__(self):
        return super(Collector, self).__repr__(len(self))


class _Filter():
    """ Filter for Collector class.
    Not to be confused with the Filter Class.
    """
    MAP = {
             'of_class': 'OfClass',
             'of_category': 'OfCategory',
             'is_element': 'WhereElementIsNotElementType',
             'is_element_type': 'WhereElementIsElementType',
             'is_view_independent': 'WhereElementIsViewIndependent',
             'parameter_filter': 'WherePasses',
            }

    def __init__(self, collector):
        self._collector = collector

    def __call__(self, **filters):
        """
        collector = Collector().filter > ._Filter(filters)
        filters = {'of_class'=Wall}
        """
        filters = self.coerce_filter_values(filters)

        for key, value in filters.iteritems():
            self._collector._filters[key] = value

        filtered_collector = self.chain(self._collector._filters)
        self._collector.elements = [element for element in filtered_collector]
        return self._collector

    def chain(self, filters, filtered_collector=None):
        """ Chain filters together.

        Converts this syntax: `collector.filter(of_class=X, is_element=True)`
        into: `FilteredElementCollector.OfClass(X).WhereElementisNotElementType()`

        A copy of the filters is copied after each pass so the Function
        can be called recursevily in a queue.

        TODO:
            Right now, using is_element=True is same as is_element=False
        """
        # Firt Loop
        if not filtered_collector:
            filtered_collector = self._collector._revit_object

        # Stack is track filter chainning queue
        filter_stack = copy(filters)
        for key, value in filters.iteritems():
            collector_filter = getattr(filtered_collector, _Filter.MAP[key])
            if isinstance(value, bool):
                collector_results = collector_filter()
            elif isinstance(value, ParameterFilter):
                collector_results = collector_filter(value._revit_object)
            else:
                collector_results = collector_filter(value)
            filter_stack.pop(key)
            filtered_collector = self.chain(filter_stack, filtered_collector=filtered_collector)

        return filtered_collector

    def coerce_filter_values(self, filters):
        """ Allows value to be either Enumerate or string.

        Usage:
            >>> elements = collector.filter(of_category=BuiltInCategory.OST_Walls)
            >>> elements = collector.filter(of_category='OST_Walls')

            >>> elements = collector.filter(of_class=WallType)
            >>> elements = collector.filter(of_class='WallType')

        Note:
            String Connversion for `of_class` only works for the Revit.DB
            namespace.

        """
        category_name = filters.get('of_category')
        if category_name and isinstance(category_name, str):
            filters['of_category'] = BuiltInCategoryEnum.by_name(category_name)

        class_name = filters.get('of_class')
        if class_name and isinstance(class_name, str):
            filters['of_class'] = getattr(DB, class_name)

        return filters


class ParameterFilter(BaseObjectWrapper):
    """ Parameter Filter Wrapper

    Usage:
        >>> parameter_filter = ParameterFilter('Type Name', equals='Wall 1')
        >>> collector = Collector(parameter_filter=parameter_filter)

        >>> parameter_filter = ParameterFilter('Height', less_than=10)
        >>> collector = Collector(parameter_filter=parameter_filter)
    """

    LOGICAL_FILTERS = {
                        'equals': '', 'not_equal': '',
                        'contains': '', 'not_contains': '',
                        'begins': '', 'not_begins': '',
                        'ends': '', 'not_ends': '',
                        'greater': '', 'greater_equal': '',
                        'less': '', 'less_equal': '',

                        'or': 'LogicalAndFilter ',
                        'and': 'LogicalOrFilter ',
                      }

    def __init__(self, parameter_name, **conditions):
        self.parameter_name = parameter_name
        self.conditions = conditions
        self.reverse = conditions.get('reverse', False)

        # self.element_parameter_filter =

        DB.ElementParamterFilter(FilterRule, self.reverse)
        DB.ElementParamterFilter(IList[FilterRule](), self.reverse)
