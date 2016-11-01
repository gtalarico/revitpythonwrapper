from rpw import DB

class BuiltInParameterEnum():
    """ Enumeration Wrapper """

    parameters = DB.BuiltInParameter

    @classmethod
    def by_name(cls, built_in_parameter_name):
        """ Gets Built In Parameter.
        returns: Parameter, or None
        """
        return getattr(BuiltInParameterEnum.parameters, built_in_parameter_name)
