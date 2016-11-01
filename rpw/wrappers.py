""" Python Wrapper For the Revit API """

import clr

from rpw import doc, uidoc, version
from rpw.logger import logger
from rpw.enumeration import BuiltInParameterEnum


class BaseWrapper(object):
    """ Base Class"""

    def __init__(self, element):
        """
        Child classes can use self._element to refer back to Revit Element
        Element is used loosely to refer to all Revit Elements.
        """
        self._element = element

    def __getattr__(self, attr):
        """
        Allows you to access original methods and properties or the element.
        """
        return getattr(self._element, attr)

    def __repr__(self, data=''):
        return '<RPW_{}:{}>'.format(self.__class__.__name__, data)


class ElementId(BaseWrapper):
    """ Element Id Wrapper """

    def __int__(self):
        return self._element.IntegerValue

    def __str__(self):
        return self._element.ToString()

    def __repr__(self):
        return super(ElementId, self).__repr__(self._element.IntegerValue)


class Element(BaseWrapper):
    """
    Generic Revit Element Wrapper
    """
    def __init__(self, element):
        """ Setup element"""
        super(Element, self).__init__(element)
        self.parameters = _Parameters(element)

    @property
    def id(self):
        """ Example of mapping existing properties"""
        return ElementId(self._element.Id)

    def __repr__(self):
        return super(Element, self).__repr__(str(self._element.ToString()))


class _Parameters(BaseWrapper):
    """
    Revit Element Parameter List Wrapper.
    Allows you to treat an element parameters as if it was a dictionary.
    """

    def __init__(self, parameters):
        """ Setup element"""
        super(_Parameters, self).__init__(parameters)
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
        return super(_Parameters, self).__repr__(len(self))


class _BuiltInParameters(BaseWrapper):
    def __getitem__(self, name):
        """ Retrieves Built In Parameter. """
        bip_parameter = BuiltInParameterEnum.by_name(name)
        parameter = self._element.get_Parameter(bip_parameter)
        return _Parameter(parameter) if parameter else None


class _Parameter(BaseWrapper):
    """
    Revit Element Parameter Wrapper.
    Types:
    Autodesk.Revit.DB.StorageType.String
    Autodesk.Revit.DB.StorageType.Double
    Autodesk.Revit.DB.StorageType.ElementId
    Autodesk.Revit.DB.StorageType.Integer
    Autodesk.Revit.DB.StorageType.None
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
        if self.type is str:
            return self._element.AsString()
        if self.type is float:
            return self._element.AsDouble()
        if self.type is int:
            return self._element.AsInteger()
        if self.type is ElementId:
            return self._element.AsElementId()
        if self.type is None:
            return None

    def __repr__(self):
        """ Adds data to Base __repr__ to add selection count"""
        return super(_Parameter, self).__repr__(self.value)


class Selection(BaseWrapper):
    """
    Revit uidoc.Selection Wrapper
    Makes easier to manipulate Active Selection.

    Usage:

    selection = Selection()
    selection.element_ids
    selection.elements
    len(selection)

    selection.RevitProperty
    selection.RevitMethod()
    """

    def __init__(self):
        """ Stores uidoc.Selection in element so attributes can be accessed"""
        super(Selection, self).__init__(uidoc.Selection)

    @property
    def element_ids(self):
        """ returns: List of ElementIds Objects """
        return [eid for eid in self._element.GetElementIds()]

    @property
    def elements(self):
        """ returns: List of Elements """
        return [doc.GetElement(eid) for eid in self.element_ids]

    def __getitem__(self, index):
        """ Retrieves element using index. If Index is out range,
        None is returned

        :param index: Integer representing list index.

        returns: Element, None
        Usage:
        selection[0]
        """
        try:
            return self.elements[index]
        except IndexError:
            return None

    def __len__(self):
        """ Number items of Selection """
        return len(self.element_ids)

    def __repr__(self):
        """ Adds data to Base __repr__ to add selection count"""
        return super(Selection, self).__repr__(len(self))


class FamilyInstance(BaseWrapper):
    """ Generic Family Instance Wrapper """
    # Get Type
    # Get Symbol
    # Get Elements
    # @transaction(name)
    def move(self, translation):
        pass


class FamilyType(BaseWrapper):
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
