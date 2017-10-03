.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


==================
Known Issues
==================

* Inconsisten Returns
    The library is not consistent with its return types. Sometimes a wrapped
    element is returned, sometimes is unwrapped.
    Since fixing this would be a breaking change, I am panning on
    fixing this on the next major release (2.0)
    The main change will be that attributes that were previously properties,
    will become a get method with an optional kwarg for wrapped:

    >>> # Previous
    >>> instance.family
    >>> # 2.0
    >>> instance.get_family()

* Case Sensitive ElementParameterFilter

    | The boolean argument for case_sensitive string comparison has no effect
    | I achieved the same result using the RevitPythonShell, so this could
    | be either a RevitAPI bug, or a IronPython/API issue.

    To Reproduce:

        >>> Assumes an element with a parameter with string value: "Test"
        >>> param_id = SomeElementId
        >>> value = 'test'
        >>> case_sensitive = True

        >>> rule = DB.ParameterFilterRuleFactory.CreateBeginsWithRule(param_id, value, case_sensitive)
        >>> filter_rule = DB.ElementParameterFilter(rule)
        >>> col = FilteredElementCollector(doc).WherePasses(filter_rule)

    Expected:

        `col` would not include element with parameter with value 'Test' with
        case_sensitive is True.

    Result:
        `col` always is always case insensitive.

.. disqus
