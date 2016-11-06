from copy import copy
from functools import reduce

from rpw import uidoc, doc, DB
from rpw.logger import logger
from rpw.wrappers import BaseObjectWrapper
from rpw.enumeration import BuiltInCategoryEnum


class Collector(BaseObjectWrapper):
    """
    Revit FilteredElement Collector Wrapper

    Usage:
        >>> collector = Collector()
        >>> elements = collector.filter(of_class=View)

        # Multiple Filters

        >>> collector = Collector()
        >>> elements = collector.filter(of_category=BuiltInCategory.OST_Walls,
                                        is_element_type=True)

        # Chain Preserves Previous Results

        >>> collector = Collector()
        >>> walls = collector.filter(of_category=BuiltInCategory.OST_Walls)
        >>> walls.filter(is_element_type=True)

        # Use Enumeration member or string shortcut:

        >>> collector.filter(of_category='OST_Walls')
        >>> collector.filter(of_category='ViewType')


    Returns:
        Collector: Returns collector Class

    Attributes:
        collector.elements: Returns list of all *collected* elements
        collector.first: Returns first found element, or `None`

    """

    def __init__(self, view=None):
        """
        Args:
            view (Revit.DB.View) = View Scope (Optional)
        """
        if view:
            collector = DB.FilteredElementCollector(doc, view.Id)
        else:
            collector = DB.FilteredElementCollector(doc)
        super(Collector, self).__init__(collector)
        self.elements = []
        self._filters = {}

        self.filter = _Filter(self)

    @property
    def first(self):
        """ Returns the first element in collector, or None"""
        try:
            return self.elements[0]
        except IndexError:
            return None

    def __len__(self):
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
            else:
                collector_results = collector_filter(value)
            filter_stack.pop(key)
            filtered_collector = self.chain(filter_stack, filtered_collector=filtered_collector)

        return filtered_collector

    def coerce_filter_values(self, filters):
        """ Allows value to be either Enumerate or string.

        >>> elements = collector.filter(of_category=BuiltInCategory.OST_Walls)
        >>> elements = collector.filter(of_category='OST_Walls')
        and
        >>> elements = collector.filter(of_class=WallType)
        >>> elements = collector.filter(of_class='WallType')

        """
        category_name = filters.get('of_category')
        if category_name and isinstance(category_name, str):
            filters['of_category'] = BuiltInCategoryEnum.by_name(category_name)

        class_name = filters.get('of_class')
        if class_name and isinstance(class_name, str):
            filters['of_class'] = getattr(DB, class_name)
            # filters['of_class'] = reduce(getattr, class_name.split('.'), DB)
            # This would allow deeper members DB.Architecture.Room

        return filters
