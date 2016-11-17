"""
Element Wrappers

>>> rpw.Element(SomeRevitElement)

"""

from rpw import doc, uidoc, DB
from rpw.parameter import Parameter, ParameterSet
from rpw.base import BaseObjectWrapper

from rpw.logger import logger
from rpw.exceptions import RPW_Exception, RPW_WrongStorageType
from rpw.exceptions import RPW_ParameterNotFound, RPW_TypeError


class Element(BaseObjectWrapper):
    """
    Generic Revit Element Wrapper

    Usage:

        >>> wall = Element(RevitWallElement)
        >>> wall.Id
        >>> wall.parameters['Height'].value
        10.0

        >>> wall.parameters['Height'].type
        <type: float>

        >>> with Transaction('Set Height'):
        >>>     wall.parameters['Height'].value = 5

    Attributes:

        parameters (ParameterSet): Access :class:`.ParameterSet` class.
        parameters['ParamName'] (_Parameter): Returns :class:`_Parameter` class instance if match is found.
        parameters.builtins['BuiltInName'] (_Parameter): Buit In :obj:_Parameter
        _revit_object (DB.Element) = Wrapped Revit Reference

    """
    def __init__(self, element, enforce_type=None):
        """
        Args:
            element (Element Reference): Can be ``DB.Element``, ``DB.ElementId``, or ``int``.

        Returns:
            rpw.Element: Instance of Wrapped Element

        Usage:
            >>> wall = Element(SomeElementId)
            >>> wall.parameters['Height']
            >>> wall.parameters.builtins['WALL_LOCATION_LINE']
        """
        # This class isn't very useful right now, except for adding the .parameters attribute.
        # The parameter could be used along: Consider removing if a use is not found.
        if enforce_type and not isinstance(element, enforce_type):
            raise RPW_TypeError(enforce_type, type(element))

        super(Element, self).__init__(element)
        self.parameters = ParameterSet(element)

    @property
    def id_as_int(self):
        """ Example of mapping existing properties"""
        return self._revit_object.Id.IntegerValue

    @classmethod
    def from_int(cls, id_int):
        element = doc.GetElement(DB.ElementId(id_int))
        return Element(element)

    @classmethod
    def from_id(cls, element_id):
        element = doc.GetElement(element_id)
        return Element(element)

    def __repr__(self, data=None):
        data = data if data else self._revit_object
        return super(Element, self).__repr__(str(data))

# class Create(self):
#     try:
#         # API 2016:
#         DB.Level.Create(doc, 10)
#     except:
#         # API 2015:
#         doc.Create.NewLevel(10)

#
# class FamilyInstance(BaseObjectWrapper):
#     """ Generic Family Instance Wrapper """
#  Help with Family name, symbol name, etc
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
