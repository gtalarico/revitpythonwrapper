"""
Parameter Wrapper
==============================================

"""

from rpw import DB
from rpw.logger import logger
from rpw.enumeration import BipEnum
from rpw.exceptions import RPW_Exception, RPW_WrongStorageType
from rpw.exceptions import RPW_ParameterNotFound, RPW_TypeError
from rpw.base import BaseObjectWrapper


class _ParameterSet(BaseObjectWrapper):
    """
    Revit Element Parameter List Wrapper.

    Allows you to treat an element parameters as if it was a dictionary.
    Keeping element store so other methods beyond Parameters can be used.

    This class lives at an elemnt's .parameters attribute.

    Attributes:
        _revit_object (DB.Element) = Revit Reference

    Usage:
        >>> element.parameters.all()
        >>> element.parameters['Comments'].value
        >>> element.parameters['Comments'].value = 'My Comment'
        >>> element.parameters['Comments'].type

    """

    def __init__(self, element):
        """ Setup element"""
        super(_ParameterSet, self).__init__(element)
        self.builtins = _BuiltInParameterSet(self._revit_object)

    def __getitem__(self, param_name):
        """ Get's parameter by name.

        Returns:
            The first parameter found with a matching name (wrapper),

        Raises:
            :class:`RPW_ParameterNotFound`

        """
        parameter = self._revit_object.LookupParameter(param_name)
        # return _Parameter(parameter) if parameter else None
        if not parameter:
            raise RPW_ParameterNotFound(self._revit_object, param_name)
        return Parameter(parameter)

    def __setitem__(self, param_name, value):
        """ Sets value to element's parameter

        >>> element.parameter['Height'] = value
        """
        parameter = self.__getitem__(param_name)
        parameter.value = value

    @property
    def all(self):
        """ Returns: Flat list of wrapped parameter elements
        """
        return [Parameter(parameter) for parameter in self._revit_object.Parameters]

    def __len__(self):
        return len(self.all)

    def __repr__(self):
        """ Adds data to Base __repr__ to add Parameter List Name """
        return super(_ParameterSet, self).__repr__(len(self))


class _BuiltInParameterSet(BaseObjectWrapper):
    """ Built In Parameter Manager

    Usage:

        location_line = element.parameters.builtins['WALL_LOCATION_LINE']

    Note:
        Item Getter can take the BuilInParameter name string, or the Enumeration.
        >>> element.parameters.builtins['WALL_LOCATION_LINE']

        or

        >>>element.parameters.builtins[Revit.DB.BuiltInParameter.WALL_LOCATION_LINE]

    Attributes:
        _revit_object (DB.Element) = Revit Reference

    """

    def __getitem__(self, builtin_enum):
        """ Retrieves Built In Parameter. """
        if isinstance(builtin_enum, str):
            builtin_enum = BipEnum.get(builtin_enum)
        parameter = self._revit_object.get_Parameter(builtin_enum)
        if not parameter:
            raise RPW_ParameterNotFound(self._revit_object, builtin_enum)
        return Parameter(parameter)

    def __setitem__(self, name, param_value):
        """ Sets value for an element's built in parameter. """
        builtin_parameter = self.__getitem__(name)
        builtin_parameter.value = param_value

    def __repr__(self):
        """ Adds data to Base __repr__ to add Parameter List Name """
        return super(_BuiltInParameterSet, self).__repr__()


class Parameter(BaseObjectWrapper):
    """
    Revit Element Parameter Wrapper.

    This class is used heavily by the Element Wrapper, but can also be used
    to wrap Parameter Elements.

    Usage:
        >>> parameter = Parameter(some_revit_parameter_object)
        >>> paramter.type
        <type: str>
        >>> paramter.type
        'Some String'
        >>> paramter.name
        'Parameter Name'
        >>> paramter.builtin
        Revit.DB.BuiltInParameter.SOME_BUILT_IN_NAME

    Attributes:
        _revit_object (DB.Parameter) = Revit Reference

    Note:

        Parameter Wrapper handles the following types:

        | Autodesk.Revit.DB.StorageType.String
        | Autodesk.Revit.DB.StorageType.Double
        | Autodesk.Revit.DB.StorageType.ElementId
        | Autodesk.Revit.DB.StorageType.Integer
        | Autodesk.Revit.DB.StorageType.None


    """
    storage_types = {
                    'String': str,
                    'Double': float,
                    'Integer': int,
                    'ElementId': DB.ElementId,
                    'None': None,
                     }

    def __init__(self, parameter):
        """ Parameter Wrapper Constructor

        Args:
            DB.Parameter: Parameter to be wrapped

        Returns:
            Parameter: Wrapped Parameter Class
        """
        if not isinstance(parameter, DB.Parameter):
            raise RPW_TypeError(DB.Parameter, type(parameter))
        super(Parameter, self).__init__(parameter)

    @property
    def type(self):
        """ Returns the Python Type of the Parameter

        Returns:
            type: Python Built in type

        Usage:
            >>> element.parameters['Height'].type
            <type: float>
        """
        storage_type_name = self._revit_object.StorageType.ToString()
        return Parameter.storage_types[storage_type_name]

    @property
    def id(self):
        return self._revit_object.Id

    @property
    def value(self):
        """
        Get Parameter Value
        Returns:
            type: parameter value in python type

        Usage:
            >>> desk.parameter['Height'].value
            >>> 3.0

        Set Parameter Value

        Usage:
            >>> desk.parameter['Height'].value = 3

        Note:

            Certain types are automatically coerced

            * storagetype:value > result
            * str:None > ''
            * str:type > str(value)
            * ElementId:None > ElemendId.InvalidElementId
            * int:float > int
            * float:int > float
        """
        if self.type is str:
            return self._revit_object.AsString()
        if self.type is float:
            return self._revit_object.AsDouble()
        if self.type is int:
            return self._revit_object.AsInteger()
        if self.type is DB.ElementId:
            return self._revit_object.AsElementId()

        raise RPW_Exception('could not get storage type: {}'.format(self.type))

    @value.setter
    def value(self, value):
        # Check if value provided matches storage type
        if not isinstance(value, self.type):
            # If not, try to handle
            if self.type is str and value is None:
                value = ''
            if self.type is str and value is not None:
                value = str(value)
            elif self.type is DB.ElementId and value is None:
                value = DB.ElementId.InvalidElementId
            elif isinstance(value, int) and self.type is float:
                value = float(value)
            elif isinstance(value, float) and self.type is int:
                value = int(value)
            else:
                raise RPW_WrongStorageType(self.type, value)

        param = self._revit_object.Set(value)

    @property
    def name(self):
        """
        Returns Parameter name

        >>> element.parameters['Comments'].name
        >>> 'Comments'
        """
        return self._revit_object.Definition.Name

    @property
    def builtin(self):
        """ Returns the BuiltInParameter name of Parameter.
        Same as DB.Parameter.Definition.BuiltIn

        Usage:
            >>> element.parameters['Comments'].builtin_name
            Revit.DB.BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS

        Returns:
            Revit.DB.BuiltInParameter: BuiltInParameter Enumeration Member
        """
        return self._revit_object.Definition.BuiltInParameter

    def __repr__(self):
        """ Adds data to Base __repr__ to add selection count"""
        return super(Parameter, self).__repr__(self.value)
