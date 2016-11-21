"""
All Wrappers inherit from this base class, which has 4 responsibilities:

* Instantiates Class and storing wrapped element.
* Provides a ``unwrap()`` method, which returns the wrapped object.
* Provides access to all original methods and attributes of the
  wrapped object.
* Create a ``__repr__()`` method for consistent representation

Because access to original methods and properties is maintained, you can keep
the elements wrapped throughout your code. You would only need to unwrap when
when passing the element into function where the original Type is expected.

>>> wrapped = BaseObjectWrapper(SomeObject)
>>> wrapped
<RPW_BaseOBjectWrapper:>
>>> wrapped.unwrap()
SomeObject
>>> wrapped.SomeOriginalMethod()
# Method will run.

"""

from rpw.exceptions import RPW_TypeError


class BaseObjectWrapper(object):
    """
    Arguments:
        element(APIObject): Revit Element to store
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
        return '<RPW_{class_name}:{optional_data} [{eid}]>'.format(
                                            class_name=self.__class__.__name__,
                                            optional_data=data,
                                            eid=self._revit_object.Id.ToString())
