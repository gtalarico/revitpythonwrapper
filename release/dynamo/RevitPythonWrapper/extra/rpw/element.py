"""
>>> rpw.Element()
"""

from rpw import doc, uidoc, DB
from rpw.parameter import Parameter, _ParameterSet
from rpw.base import BaseObjectWrapper

from rpw.logger import logger
from rpw.enumeration import BuiltInParameterEnum
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
        _revit_object (DB.Element) = Revit Reference

    """
    def __init__(self, element):
        """
        Element Class Wrapper

        Usage:
            >>> wall = Element(Revit.DB.Wall)
            >>> wall.parameters['Height']
            >>> wall.parameters.builtins['WALL_LOCATION_LINE']

        Args:
            element (API Object): Revit API Object

        Returns:
            Element: Instance of Wrapped Element

        Attributes:
            parameters (_ParameterSet): Access Wrapped ParameterSet Class :class:`._ParameterSet`

            parameters['ParamName'] (_Parameter): Get Parameter

            parameters.builtins['BuiltInName'] (_Parameter): Buit In :obj:_Parameter

        """
        if not isinstance(element, DB.Element):
            logger.error(isinstance(element, DB.Element))
            raise RPW_TypeError('cannot wrap non-APIObject: {}'.format(
                                                            DB.Element,
                                                            type(element)
                                                            ))
        super(Element, self).__init__(element)
        self.parameters = _ParameterSet(element)

    @property
    def id_as_int(self):
        """ Example of mapping existing properties"""
        return self._revit_object.Id.IntegerValue

    def unwrap():
        return self._revit_object

    @classmethod
    def by_id(cls, element_id):
        """ Allows to retrieve element by Id

        element = doc.GetElement(element_id)
        return Element(element)

        """
        raise NotImplemented

    def __repr__(self):
        return super(Element, self).__repr__(str(self._revit_object.ToString()))


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
