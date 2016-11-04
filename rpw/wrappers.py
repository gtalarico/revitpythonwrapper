"""
DB Namespace Wrappers
==============================================

"""

from rpw import doc, uidoc, DB
from rpw.logger import logger
from rpw.enumeration import BuiltInParameterEnum
from rpw.exceptions import RPW_Exception, RPW_WrongStorageType
from rpw.exceptions import RPW_ParameterNotFound, RPW_TypeError

class BaseObjectWrapper(object):
    """ Base Object Wrapper Class.

    This element is stored in the projected _revit_object attribute
    Arguments:
        element(APIObject): Revit Element to store

    Note:
        There might are few cases were this class is used
        on non-elements. ParameterSet for instance, does
        not inherit from Element, but uses this class
        so it can store a reference to the element and uses
        other Parameter related methods that are not store in
        Parameters such as element.get_Parameter or element.LookupParameter
    Allows access to all original attributes and methods of original object.

    """

    def __init__(self, revit_object):
        """
        Child classes can use self._revit_object to refer back to Revit Element
        Element is used loosely to refer to all Revit Elements.
        """
        self._revit_object = revit_object

    def __getattr__(self, attr):
        """
        Access original methods and properties or the element.
        """
        return getattr(self._revit_object, attr)

    def __repr__(self, data=''):
        return '<RPW_{}:{}>'.format(self.__class__.__name__, data)


class Element(BaseObjectWrapper):
    """
    Generic Revit Element Wrapper

    self._revit_object = DB.Element

    Usage:

        >>> wall = Element(RevitWallElement)
        >>> wall.id
        >>> wall.parameters['Height']

    """
    def __init__(self, element):
        """
        Element Class Wrapper

        Usage:
            wall = Element(Revit.DB.Wall)
            wall.parameters['Height']
            wall.parameters.builtins['WALL_LOCATION_LINE']

        Args:
            element (API Object): Revit API Object

        Returns:
            Element: Instance of Wrapped Element

        Attributes:
            parameters (_ParameterSet): Access Wrapped ParameterSet Class :class:`._ParameterSet`

            parameters['ParamName'] (_Parameter): Get Parameter

            parameters.builtins['BuiltInName'] (_Parameter): Buit In :obj:_Parameter

        """
        if not isinstance(element, type(DB.APIObject)):
            raise RPW_TypeError('cannot wrap non-APIObject: {}'.format(type(element)))
        super(Element, self).__init__(element)
        self.parameters = _ParameterSet(element)

    @property
    def id(self):
        """ Example of mapping existing properties"""
        return self._revit_object.Id

    @property
    def id_as_int(self):
        """ Example of mapping existing properties"""
        return self._revit_object.Id.IntegerValue

    @classmethod
    def by_id(cls, element_id):
        """ Allows to retrieve element by Id

        element = doc.GetElement(element_id)
        return Element(element)

        """
        raise NotImplemented

    def __repr__(self):
        return super(Element, self).__repr__(str(self._revit_object.ToString()))


class _ParameterSet(BaseObjectWrapper):
    """
    Revit Element Parameter List Wrapper.

    Allows you to treat an element parameters as if it was a dictionary.
    Keeping element store so other methods beyond Parameters can be used.

    self._revit_object = DB.Element

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

        returns: the first parameter found with a matching name (wrapper),
        or None if there is no matching parameters.

        """
        parameter = self._revit_object.LookupParameter(param_name)
        # return _Parameter(parameter) if parameter else None
        if not parameter:
            raise RPW_ParameterNotFound(self, param_name)
        return _Parameter(parameter)

    def __setitem__(self, param_name, param_value):
        """ Allows to set parameter directly to Parameter Set.
         Usage:
            >>> elemenet.parameters['Height'] = 3
            >>> elemenet.parameters['Height'] = 3
         """
        parameter = self.__getitem__(param_name)
        parameter.value = param_value

    @property
    def all(self):
        """ Returns: Flat list of wrapped parameter elements
        """
        return [_Parameter(parameter) for parameter in self._revit_object.Parameters]

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
    """

    def __getitem__(self, builtin_enum):
        """ Retrieves Built In Parameter. """
        if isinstance(builtin_enum, str):
            builtin_enum = BuiltInParameterEnum.by_name(builtin_enum)
        parameter = self._revit_object.get_Parameter(builtin_enum)
        return _Parameter(parameter) if parameter else None

    def __setitem__(self, name, param_value):
        """ Sets value for an element's built in parameter. """
        builtin_parameter = self.__getitem__(name)
        builtin_parameter.value = param_value

    def __repr__(self):
        """ Adds data to Base __repr__ to add Parameter List Name """
        return super(_BuiltInParameterSet, self).__repr__()


class _Parameter(BaseObjectWrapper):
    """
    Revit Element Parameter Wrapper.

    self._parameter = DB.Parameter

    Handles the following types:

    * Autodesk.Revit.DB.StorageType.String
    * Autodesk.Revit.DB.StorageType.Double
    * Autodesk.Revit.DB.StorageType.ElementId
    * Autodesk.Revit.DB.StorageType.Integer
    * Autodesk.Revit.DB.StorageType.None
    """
    storage_types = {
                    'String': str,
                    'Double': float,
                    'Integer': int,
                    'ElementId': DB.ElementId,
                    'None': None,
                     }

    @property
    def type(self):
        """ Returns the Python Type of the Parameter

        returns: python built in type
        """
        storage_type_name = self._revit_object.StorageType.ToString()
        return _Parameter.storage_types[storage_type_name]

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
    def builtin(self):
        """ Returns the BuiltInParameter name of Parameter.

        Usage:
            >>> element.parameters['Comments'].builtin_name

        Returns:
            Revit.DB.BuiltInParameter: ALL_MODEL_INSTANCE_COMMENTS
        """
        return self._revit_object.Definition.BuiltInParameter

    def __repr__(self):
        """ Adds data to Base __repr__ to add selection count"""
        return super(_Parameter, self).__repr__(self.value)


#
# class FamilyInstance(BaseObjectWrapper):
#     """ Generic Family Instance Wrapper """
#     # Get Type
#     # Get Symbol
#     # Get Elements
#     # @transaction(name)
#     def move(self, translation):
#         pass
#
#
# class FamilyType(BaseObjectWrapper):
#     """ Generic Family Instance Wrapper """
#     # Get Type
#     # Get Symbol
#     # Get Elements

# class DynamoUtils(object):
#     # Coerce/Wrap/Unwrap
#     # Create object that can act as both?
#     pass
#
#
# class BoundingBox(object):
#     """ Revit BoundingBox Wrapper """
#     # GetCenter
#     # FromObject()
#     pass
#
# class UI(object):
#   pass
#
#
# class Doc(object):
#   pass
