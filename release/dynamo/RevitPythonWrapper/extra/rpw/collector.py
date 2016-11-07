from rpw import uidoc, doc, DB
from rpw import List
from rpw.logger import logger
from rpw.base import BaseObjectWrapper
from rpw.exceptions import RPW_Exception
from rpw.enumeration import BuiltInCategoryEnum, BuiltInParameterEnum


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
        filters = self._coerce_filter_values(filters)

        for key, value in filters.iteritems():
            self._collector._filters[key] = value

        filtered_collector = self._chain(self._collector._filters)
        # TODO: This should return iterator to save memory
        self._collector.elements = [element for element in filtered_collector]
        return self._collector

    def _chain(self, filters, collector=None):
        """ Chain filters together.

        Converts this syntax: `collector.filter(of_class=X, is_element=True)`
        into: `FilteredElementCollector.OfClass(X).WhereElementisNotElementType()`

        A copy of the filters is copied after each pass so the Function
        can be called recursevily in a queue.

        """
        # First Loop
        if not collector:
            collector = self._collector._revit_object

        # Stack is track filter chainning queue
        filter_stack = filters.copy()
        for filter_name, filter_value in filters.iteritems():
            collector_filter = getattr(collector, _Filter.MAP[filter_name])

            if filter_name not in _Filter.MAP:
                raise RPW_Exception('collector filter rule does not exist: {}'.format(filter_name))

            elif isinstance(filter_value, bool):
                if filter_value is True:
                    collector_results = collector_filter()
            elif isinstance(filter_value, ParameterFilter):
                collector_results = collector_filter(filter_value._revit_object)
            else:
                collector_results = collector_filter(filter_value)
            filter_stack.pop(filter_name)
            collector = self._chain(filter_stack, collector=collector)

        return collector

    def _coerce_filter_values(self, filters):
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

    Returns:
        FilterRule: A filter rule object, depending on arguments.

    Note:

        The FilterRule returned will be one of the following:

            * FilterDoubleRule
            * FilterElementIdRule
            * FilterCategoryRule
            * FilterStringRule
            * FilterIntegerRule
            * SharedParameterApplicableRule

        Internally, the class uses the ParameterFilterRuleFactory Class:

            * ParameterFilterRuleFactory.CreateBeginsWithRule(param_id, value, case_sensitive)
            * ParameterFilterRuleFactory.CreateContainsRule(param_id, value, case_sensitive)
            * ParameterFilterRuleFactory.CreateEndsWithRule(param_id, value, case_sensitive)
            * ParameterFilterRuleFactory.CreateEqualsRule(param_id, value)
            * ParameterFilterRuleFactory.CreateGreaterOrEqualRule(param_id, value)
            * ParameterFilterRuleFactory.CreateGreaterRule(param_id, value)
            * ParameterFilterRuleFactory.CreateLessOrEqualRule(param_id, value)
            * ParameterFilterRuleFactory.CreateLessRule(param_id, value)
            * ParameterFilterRuleFactory.CreateNotBeginsWithRule(param_id, value)
            * ParameterFilterRuleFactory.CreateNotContainsRule(param_id, value)
            * ParameterFilterRuleFactory.CreateNotEqualsRule(param_id, value)
            * ParameterFilterRuleFactory.CreateSharedParameterApplicableRule(param_name)

    """

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

    def __init__(self, parameter_id, **conditions):
        """
        Creates Parameter Filter Rule

        Args:
            param_id(DB.ElementID): ElemendId of parameter
            **conditions: Filter Rule Conditions

            conditions:
                | equals
                | contains
                | begins
                | ends
                | greater
                | greater_equal
                | less
                | less_equal
                | not_equals
                | not_contains
                | not_begins
                | not_ends
                | not_greater
                | not_greater_equal
                | not_less
                | not_less_equal

            options:
                case_sensitive: Enforces case sensitive, String only
                reverse: Reverses result of Collector

        Usage:
            >>> param_rule = ParameterFilter(param_id, equals=2)
            >>> param_rule = ParameterFilter(param_id, not_equals='a', case_sensitive=True)
            >>> param_rule = ParameterFilter(param_id, not_equals=3, reverse=True)

        """
        self.parameter_id = parameter_id
        self.conditions = conditions
        self.reverse = conditions.get('reverse', False)
        self.case_sensitive = conditions.get('case_sensitive', ParameterFilter.CASE_SENSITIVE)
        self.precision = conditions.get('precision', ParameterFilter.FLOAT_PRECISION)

        valid_rule = [x for x in conditions if x in ParameterFilter.RULES]
        valid_rules = []
        for condition_name in valid_rule:
            condition_value = conditions[condition_name]

            # Returns on of the CreateRule factory method names above
            rule_factory_name = ParameterFilter.RULES.get(condition_name)
            filter_value_rule = getattr(DB.ParameterFilterRuleFactory, rule_factory_name)

            args = [condition_value]

            if isinstance(condition_value, str):
                args.append(self.case_sensitive)

            if isinstance(condition_value, float):
                args.append(self.precision)

            filter_rule = filter_value_rule(parameter_id, *args)
            if 'not_' in condition_name:
                filter_rule = DB.FilterInverseRule(filter_rule)
            # DEBUG INFO:
            # logger.critical('Conditions: {}'.format(conditions))
            # logger.critical('Case sensitive: {}'.format(self.case_sensitive))
            # logger.critical('Reverse: {}'.format(self.reverse))
            # logger.critical('ARGS: {}'.format(args))
            # logger.critical(filter_rule)
            # logger.critical(str(dir(filter_rule)))
            valid_rules.append(filter_rule)
        if not valid_rule:
            raise RPW_Exception('malformed filter rule: {}'.format(conditions))
        self._revit_object = DB.ElementParameterFilter(List[DB.FilterRule](valid_rules),
                                                       self.reverse)

    def __repr__(self):
        return super(ParameterFilter, self).__repr__(self.conditions)
