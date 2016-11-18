"""
All Wrappers inherit from this class. It has 4 responsibilities:

* Instantiate Class and store wrapped element in the private attribute ``_revit_object``
* Provide access to all original methods and attributes of the
  wrapped object throught the ``__getitem__`` method
* Provide a ``unwrap()`` method, which returns the wrapped object
* Create a ``__repr__()`` method for consistent representation

"""

from rpw.exceptions import RPW_TypeError


class BaseObjectWrapper(object):
    """ Base Object Wrapper Class.

    This element is stored in the projected _revit_object attribute
    Arguments:
        element(APIObject): Revit Element to store

    Note:
        There might are few cases were this class is used
        on non-elements. ParameterSet for instance, does
        not inherit from Element, but uses this class
        so it can store a reference to the element and uses
        other Parameter related methods that are not store in
        Parameters such as element.get_Parameter or element.LookupParameter

        Allows access to all original attributes and methods of original object.

    """

    def __init__(self, revit_object, enforce_type=None):
        """
        Child classes can use self._revit_object to refer back to Revit Element
        Element is used loosely to refer to all Revit Elements.
        """

        if enforce_type and not isinstance(revit_object, enforce_type):
            raise RPW_TypeError(enforce_type, type(revit_object))

        self._revit_object = revit_object

    def __getattr__(self, attr):
        """
        Access original methods and properties or the element.
        """
        return getattr(self._revit_object, attr)

    def unwrap(self):
        return self._revit_object

    def __repr__(self, data=''):
        return '<RPW_{}:{}>'.format(self.__class__.__name__, data)
