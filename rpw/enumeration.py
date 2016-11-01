from Autodesk.Revit import DB


class BuiltInParameterEnum():
    """ Enumeration Wrapper """

    parameters = DB.BuiltInParameter

    def by_name(cls, built_in_parameter_name):
        """ Gets Built In Parameter.
        returns: Parameter, or None
        """
        return getattr(BuiltInParameterEnum.parameters, built_in_parameter_name)

    def find(cls, query):
        raise NotImplemented
