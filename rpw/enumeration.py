"""

>>> BipEnum.get('WALL_LOCATION_LINE')
Revit.DB.BuiltInParameter.WALL_LOCATION_LINE
>>> BipEnum.get_id('WALL_LOCATION_LINE')
Revit.DB.ElementId

Note:
    These classes were originally create to be used internally,
    but the :func:`get_id()` is often helpful.

"""

from rpw import DB, doc, Enum
from rpw.base import BaseObjectWrapper
from rpw.exceptions import RPW_ParameterNotFound

class BipEnum(type):
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


class BicEnum(type):
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
    def from_category_id(cls, category_id):
        """ Casts ``DB.BuiltInCategory`` Enumeration member from ``DB.ElementId`` """
        return Enum.ToObject(DB.BuiltInCategory, category_id.IntegerValue)
