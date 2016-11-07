from rpw import DB, doc
from rpw.base import BaseObjectWrapper
from rpw.exceptions import RPW_ParameterNotFound


class BuiltInParameterEnum():
    """ Enumeration Wrapper """

    parameters = DB.BuiltInParameter

    @classmethod
    def by_name(cls, parameter_name, as_id=False):
        """ Gets Built In Parameter by Name
        Args:
            str: Name of Parameter

        Returns:
            DB.BuiltInParameter: BuiltInParameter Enumeration Member

        Usage:
            >>> builtin_parameter = BuiltInParameterEnum.by_name('Commnets')
            Revit.DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS
        """

        try:
            enum = getattr(BuiltInParameterEnum.parameters, parameter_name)
        except AttributeError:
            raise RPW_ParameterNotFound(BuiltInParameterEnum.parameters, parameter_name)
        else:
            if not as_id:
                return enum
            return DB.ElementId(enum)


class BuiltInCategoryEnum():
    """ Enumeration Wrapper """

    categories = DB.BuiltInCategory

    @classmethod
    def by_name(cls, category_name, as_id=False):
        """ Gets Built In Category by Name
        Args:
            str: Name of Category

        Returns:
            DB.BuiltInCategory: BuiltInCategory Enumeration Member

        Usage:
            >>> builtin_category = BuiltInCategoryEnum.by_name('OST_Room')
            Revit.DB.BuiltInCategory.OST_Room
        """
        try:
            enum = getattr(BuiltInCategoryEnum.categories, category_name)
        except AttributeError:
            raise RPW_ParameterNotFound(BuiltInCategoryEnum.categories, category_name)
        else:
            if not as_id:
                return enum
            return DB.ElementId(enum)
