"""
DB Namespace Wrappers
==============================================

"""

from rpw import doc, uidoc, version
from rpw.logger import logger
from rpw.enumeration import BuiltInParameterEnum
from rpw.exceptions import RPWException, RPW_WrongStorageType

from rpw import DB

class BaseWrapper(object):
    """ Base Object Wrapper Class.
    Does not require any arguemnts.
    Allows access to all original attributes and methods of original object.

    """

    def __getattr__(self, attr):
        """
        Access original methods and properties or the element.
        """
        return getattr(self._element, attr)

    def __repr__(self, data=''):
        return '<RPW_{}:{}>'.format(self.__class__.__name__, data)


class BaseElementWrapper(BaseWrapper):
    """ Base Element Wrapper Class
    Initializes using a Revit Element.
    This element is stored in the projected _element attribute
    Arguments:
        element(APIObject): Revit Element to store

    Note:
        There might are few cases were this class is used
        on non-elements. ParameterSet for instance, does
        not inherit from Element, but uses this class
        so it can store a reference to the element and uses
        other Parameter related methods that are not store in
        Parameters such as element.get_Parameter or element.LookupParameter
    """
    def __init__(self, element):
        """
        Child classes can use self._element to refer back to Revit Element
        Element is used loosely to refer to all Revit Elements.
        """
        self._element = element

    @property
    def unwrapped(self):
        return self._element


class ElementId(BaseElementWrapper):
    """ Element Id Wrapper

    Arguments:
        ElementId(DB.ElementId): Creates a Wrapped ElementId

    Returns:
        ElementId: Intance
    """

    def __init__(self, element):
        super(ElementId, self).__init__(element)

    @property
    def empty(self):
        return self._element.Id.InvalidElementId

    def __int__(self):
        return self._element.Id.IntegerValue

    def __str__(self):
        return self._element.Id.ToString()

    def __repr__(self):
        return super(ElementId, self).__repr__(self._element.Id.IntegerValue)


class Element(BaseElementWrapper):
    """
    Generic Revit Element Wrapper

    Usage:

        >>> wall = Element(RevitWallElement)
        >>> wall.id
        >>> wall.parameters['Height']

    """
    def __init__(self, element):
        """Google Style.

        Extended description of function.

        Args:
            element (API Object): Revit API Object

        Returns:
            Element: Instance of Wrapped Element

        Attributes:
            parameters (_ParameterSet): Access Wrapped ParameterSet Class :class:'._ParameterSet'

            parameters['ParamName'] (_Parameter): Get Paramter

            parameters.builtins['BuiltInName'] (_Parameter): Buit In :obj:_Parameter



        """
        super(Element, self).__init__(element)
        self.parameters = _ParameterSet(element)

    @property
    def id(self):
        """ Example of mapping existing properties"""
        return ElementId(self._element)

    def __repr__(self):
        return super(Element, self).__repr__(str(self._element.ToString()))


class _ParameterSet(BaseElementWrapper):
    """
    Revit Element Parameter List Wrapper.
    Allows you to treat an element parameters as if it was a dictionary.

    """

    def __init__(self, element):
        """ Setup element"""
        super(_ParameterSet, self).__init__(element)
        self.builtins = _BuiltInParameters(self._element)

    def __getitem__(self, param_name):
        """ Get's parameter by name.

        returns: the first parameter found with a matching name (wrapper),
        or None if there is no matching parameters.

        """
        parameter = self._element.LookupParameter(param_name)
        return _Parameter(parameter) if parameter else None

    def all(self):
        return [_Parameter(parameter) for parameter in self._element.Parameters]

    def __len__(self):
        return len(self.all())

    def __repr__(self):
        """ Adds data to Base __repr__ to add Parameter List Name """
        return super(_ParameterSet, self).__repr__(len(self))


class _BuiltInParameters(BaseElementWrapper):

    def __getitem__(self, name):
        """ Retrieves Built In Parameter. """
        bip_parameter = BuiltInParameterEnum.by_name(name)
        parameter = self._element.get_Parameter(bip_parameter)
        return _Parameter(parameter) if parameter else None


class _Parameter(BaseElementWrapper):
    """
    Revit Element Parameter Wrapper.

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
                    'ElementId': ElementId,
                    'None': None,
                     }

    @property
    def type(self):
        """ Results the Python Type of the Parameter

        returns: python built in type
        """
        storage_type_name = self._element.StorageType.ToString()
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
            return self._element.AsString()
        if self.type is float:
            return self._element.AsDouble()
        if self.type is int:
            return self._element.AsInteger()
        if self.type is ElementId:
            return self._element.AsElementId()

    @value.setter
    def value(self, value):
        print('TYPE: ' + str(self.type))
        # Check if value provided matches storage type
        if not isinstance(value, self.type):
            if value is None and self.type is str:
                value = ''
            if value is not None and self.type is str:
                value = str(value)
            elif value is None and self.type is ElementId:
                value = DB.ElementId.InvalidElementId
            elif isinstance(value, int) and self.type is float:
                value = float(value)
            elif isinstance(value, float) and self.type is int:
                value = int(value)
            else:
                raise RPW_WrongStorageType(self.type, value)

        param = self._element.Set(value)

    def __repr__(self):
        """ Adds data to Base __repr__ to add selection count"""
        return super(_Parameter, self).__repr__(self.value)


class FamilyInstance(BaseElementWrapper):
    """ Generic Family Instance Wrapper """
    # Get Type
    # Get Symbol
    # Get Elements
    # @transaction(name)
    def move(self, translation):
        pass


class FamilyType(BaseElementWrapper):
    """ Generic Family Instance Wrapper """
    # Get Type
    # Get Symbol
    # Get Elements

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
