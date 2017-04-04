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
from rpw import logger

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

        # __dict__ used to prevent recursion
        object.__setattr__(self, '_revit_object', revit_object)
        # self._custom_attrs = {}

    def __getattr__(self, attr):
        """
        Getter for original methods and properties or the element.
        """
        # object.__getattribute__(self, '_revit_object')
        # return self._revit_object
        return getattr(self._revit_object, attr)

    # Setter allows for WrappedWall.Pinned = True
    def __setattr__(self, attr, value):
        """
        # Setter original methods and properties or the element.
        # """
        try:
            object.__setattr__(self._revit_object, attr, value)
        except AttributeError:
            object.__setattr__(self, attr, value)

        # if attr == '_revit_object':
            # self.__dict__['_revit_object'] = value
        # _revit_object = self.__dict__.get('_revit_object')
        # if _revit_object:
            # if hasattr(_revit_object, attr):
                # try:
                    # setattr(_revit_object, attr, value)
                # except AttributeError:
                    # self.__dict__[attr] = value

    def unwrap(self):
        return self._revit_object

    def __repr__(self, data=''):
        if not data:
            data = self._revit_object.__class__.__name__
        return '<RPW_{class_name}: {optional_data}>'.format(
                                            class_name=self.__class__.__name__,
                                            optional_data=data)
