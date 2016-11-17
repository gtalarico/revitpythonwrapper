"""

Enumeration Wrappers

>>> BipEnum.get('WALL_LOCATION_LINE')
Revit.DB.BuiltInParameter.WALL_LOCATION_LINE
>>> BipEnum.get_id('WALL_LOCATION_LINE')
Revit.DB.ElementId

Note:
    These classes were originally create to be used internally,
    but the :func:`get_id()` is often helpful.

"""

from rpw import DB, doc
from rpw.base import BaseObjectWrapper
from rpw.exceptions import RPW_ParameterNotFound


class _MetaBipEnum(type):
    """
    Enumeration Wrapper

    Usage:
        >>> BipEnum.get('WALL_LOCATION_LINE')
        Revit.DB.BuiltInParameter.WALL_LOCATION_LINE
        >>> BipEnum.get_id('WALL_LOCATION_LINE')
        Revit.DB.ElementId
    """

    @classmethod
    def get(cls, parameter_name):
        """ Gets Built In Parameter by Name
        Args:
            str: Name of Parameter

        Returns:
            DB.BuiltInParameter: BuiltInParameter Enumeration Member

        """
        try:
            enum = getattr(DB.BuiltInParameter, parameter_name)
        except AttributeError:
            raise RPW_ParameterNotFound(DB.BuiltInParameter, parameter_name)
        return enum

    @classmethod
    def get_id(cls, parameter_name):
        """ Gets ElementId of Category by name
        Args:
            str: Name of Built In Parameter

        Returns:
            DB.BuitInParameter: BuiltInParameter Enumeration Member
        """
        enum = cls.get(parameter_name)
        return DB.ElementId(enum)


class BipEnum(object):
    """ Allows access to __getattr__ of class """
    # TODO: Remove this, no longer needed since getattr is not used.
    __metaclass__ = _MetaBipEnum


class _MetaBicEnum(type):
    """
    Enumeration Wrapper

    Usage:
        >>> BicEnum.get('OST_Room')
        Revit.DB.BuiltInCategory.OST_Room
        >>> BicEnum.get_id('OST_Room')
        Revit.DB.ElementId
        """

    @classmethod
    def get(cls, category_name):
        """ Gets Built In Category by Name
        Args:
            str: Name of Category

        Returns:
            DB.BuiltInCategory: BuiltInCategory Enumeration Member
        """
        try:
            enum = getattr(DB.BuiltInCategory, category_name)
        except AttributeError:
            raise RPW_ParameterNotFound(DB.BuiltInCategory, category_name)
        return enum

    @classmethod
    def get_id(cls, category_name):
        """ Gets ElementId of Category by name
        Args:
            str: Name of Category

        Returns:
            DB.BuiltInCategory: BuiltInCategory Enumeration Member
        """
        enum = cls.get(category_name)
        return DB.ElementId(enum)

    @classmethod
    def from_id(cls, element_id):
        """ Gets ``DB.BuiltInCategory`` Enumeration member from ``DB.ElementId`` """
        for bic_name in dir(DB.BuiltInCategory):
            if element_id == DB.ElementId(bic):
                return cls.get(bic)
        else:
            raise RPW_ParameterNotFound(element_id, category_name)

    @classmethod
    def from_category(cls, category):
        """ Get's BuiltInCategory Enumeration member from 11DB.Category`` """
        return cls.from_id(category.Id)

class BicEnum(object):
    """ Allows access to __getattr__ of class """
    # TODO: Remove this, no longer needed since getattr is not used.
    __metaclass__ = _MetaBicEnum
