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
    def __init__(self, element):
        """
        Args:
            element (API Object): Revit API Object

        Returns:
            Element: Instance of Wrapped Element

        Usage:
            >>> wall = Element(Revit.DB.Wall)
            >>> wall.parameters['Height']
            >>> wall.parameters.builtins['WALL_LOCATION_LINE']

        """
        if not isinstance(element, DB.Element):
            logger.error(isinstance(element, DB.Element))
            raise RPW_TypeError('cannot wrap non-APIObject: {}'.format(
                                                            DB.Element,
                                                            type(element)
                                                            ))
        super(Element, self).__init__(element)
        self.parameters = ParameterSet(element)

    @property
    def id_as_int(self):
        """ Example of mapping existing properties"""
        return self._revit_object.Id.IntegerValue

    @classmethod
    def from_id(cls, element_id):
        """
        Allows to create ``rpw.Element`` from an
        element by Id (``int`` or ``DB.ElementId``)

        Args:
            element_id (int, DB.ElementId): ElementId or Integer of element to wrap.
        """
        # IDEA: Just move this to __init__

        if isinstance(element_id, int):
            element_id = DB.ElementId(element_id)

        element = doc.GetElement(element_id)
        return Element(element)

    def __repr__(self):
        return super(Element, self).__repr__(str(self._revit_object.ToString()))



# Get ElementType Name
# >>> element_type.FamilyName
# 'Floor'
# Element.Name.GetValue(element_type)
# 'Floor 1'
# http://forums.autodesk.com/t5/revit-api-forum/extracting-family-name-and-type-from-object/td-p/3093998


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
    ## Help with Family name, symbol name, etc
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
