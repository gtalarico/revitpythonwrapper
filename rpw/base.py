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

from rpw.exceptions import RPW_TypeError, RPW_Exception
from rpw import logger


class BaseObject(object):

        def __init__(self, *args, **kwargs):
            pass

        def __repr__(self, data=''):
            if data == '':
                data = self._revit_object.__class__.__name__
            return '<RPW_{class_name}: {data}>'.format(
                                        class_name=self.__class__.__name__,
                                        data=data
                                        )

class BaseObjectWrapper(BaseObject):
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

        object.__setattr__(self, '_revit_object', revit_object)

    def __getattr__(self, attr):
        """
        Getter for original methods and properties or the element.
        This method is only called if the attribute name does not
        already exists.
        """
        try:
            return getattr(self.__dict__['_revit_object'], attr)
        except KeyError:
            raise RPW_Exception('BaseObjectWrapper is missing _revit_object: {}'.format(self))

    def __setattr__(self, attr, value):
        """
        Setter allows setting of wrapped object properties, for example
        ```WrappedWall.Pinned = True``
        """
        if hasattr(self._revit_object, attr):
            self._revit_object.__setattr__(attr, value)
        else:
            object.__setattr__(self, attr, value)

    def unwrap(self):
        return self._revit_object
