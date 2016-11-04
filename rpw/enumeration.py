from rpw import DB, doc
from rpw.exceptions import RPW_ParameterNotFound

class BuiltInParameterEnum():
    """ Enumeration Wrapper """

    parameters = DB.BuiltInParameter

    @classmethod
    def by_name(cls, parameter_name):
        """ Gets Built In Parameter.
        returns: Parameter
        """
        return getattr(BuiltInParameterEnum.parameters,
                       parameter_name)

class BuiltInCategoryEnum():
    """ Enumeration Wrapper """

    categories = DB.BuiltInCategory

    @classmethod
    def by_name(cls, category_name):
        """ Gets Built In Category.
        returns: Category
        """

        return getattr(BuiltInCategoryEnum.categories, category_name)
