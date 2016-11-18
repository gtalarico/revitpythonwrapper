"""
Element Wrappers

>>> rpw.Element(SomeRevitElement)

"""


from rpw import doc, uidoc, DB
from rpw.parameter import Parameter, ParameterSet
from rpw.base import BaseObjectWrapper

from rpw.exceptions import RPW_Exception, RPW_WrongStorageType
from rpw.exceptions import RPW_ParameterNotFound, RPW_TypeError
from rpw.utils.logger import logger

from rpw.enumeration import BicEnum

# TODO: Decide if should return wrapped


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
            :any:`Element`: Instance of Wrapped Element

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


class Instance(Element):
    """ ``DB.FamilyInstance`` Wrapper

    Attribute:
        _revit_object (DB.FamilyInstance): Wrapped ``DB.FamilyInstance`` or
        other placeable such as DB.Wall
    """
    def __init__(self, family):
        super(Instance, self).__init__(family, enforce_type=DB.FamilyInstance)

    @property
    def symbol(self):
        """ Wrapped ``DB.FamilySymbol`` of the ``DB.FamilyInstance``
        """
        symbol = self._revit_object.Symbol
        return Symbol(symbol)

    @property
    def family(self):
        """ Wrapped ``DB.Family`` of the ``DB.FamilyInstance``
        """
        symbol = self._revit_object.Symbol
        return Family(self.symbol.family)

    @property
    def siblings(self):
        """ Other ``DB.FamilyInstance`` of the same ``DB.FamilySymbol`` """
        return self.symbol.instances

    def __repr__(self):
        return super(Instance, self).__repr__(self.symbol.name)


class Symbol(Element):
    """ ``DB.FamilySymbol`` Wrapper

    Attribute:
        _revit_object (DB.FamilySymbol): Wrapped ``DB.FamilySymbol``
    """

    def __init__(self, family):
        super(Symbol, self).__init__(family, enforce_type=DB.FamilySymbol)

    @property
    def family(self):
        """ Wrapped ``DB.Family`` of the ``DB.Symbol`` """
        return Family(self._revit_object.Family)

    @property
    def name(self):
        from Autodesk.Revit import DB
        # FIXME: But requires re-importing it
        # https://github.com/IronLanguages/main/issues/1540#issuecomment-260426990
        # http://stackoverflow.com/questions/40580471/net-assembly-loses-some-methods-when-imported-from-one-python-file-into-another
        return DB.Element.Name.GetValue(self._revit_object)

    @property
    def instances(self):
        """ Gets instances of the ``DB.FamilySymbol`` """
        print('Getting instances: {}'.format(self._revit_object))
        return rpw.Collector(symbol=self._revit_object.Id).elements

    @property
    def siblings(self):
        """ Gets sibling Symbols of the same``DB.Family`` """
        symbols_ids = self._revit_object.GetSimilarTypes()
        return [doc.GetElement(i) for i in symbols_ids]
        # Same as: return self.family.symbols, but the above also works for walls

    def __repr__(self):
        return super(Symbol, self).__repr__(self.name)


class Family(Element):
    """
    Attribute:
        _revit_object (DB.Family): Wrapped ``DB.Family``
    """

    def __init__(self, family):
        super(Family, self).__init__(family, enforce_type=None)

    @property
    def name(self):
        return self._revit_object.Name

    @property
    def symbols(self):
        """ Gets Symbols of the ``DB.Family`` """
        symbols_ids = self._revit_object.GetFamilySymbolIds()
        return [doc.GetElement(i) for i in symbols_ids]

    @property
    def instances():
        return rpw.Collector(of_class=self.category._revit_object,
                             is_not_type=True).elements

    @property
    def category(self):
        return Category(self._revit_object.FamilyCategory)

    @property
    def siblings(self):
        return self.category.families

    def __repr__(self):
        return super(Family, self).__repr__(self.name)


class Category(BaseObjectWrapper):
    """
    Attribute:
        _revit_object (DB.Family): Wrapped ``DB.Category``
    """

    @property
    def name(self):
        return self._revit_object.Name

    @property
    def families(self):
        return rpw.Collector(of_category=self._revit_object,
                             is_type=True).elements

    @property
    def symbols(self):
        bic = Bic
        return rpw.Collector(of_category=self._revit_object,
                             is_type=True).elements

    @property
    def instances(self):
        return rpw.Collector(of_category=self._revit_object,
                             is_not_type=True).elements

    def __repr__(self):
        return super(Category, self).__repr__(self.name)

# class InstanceFactory(object):
#     MAP = {
#            'Autodesk.Revit.DB.FamilyInstance': Instance,
#            'Autodesk.Revit.DB.Wall': Wall,
#            'Autodesk.Revit.DB.FamilySymbol': Symbol,
#            'Autodesk.Revit.DB.WallType': Symbol,
#            'Autodesk.Revit.DB.Family': Family,
#           }
#
# class Wall(rpw.Element):
#     @property
#     def symbol(self):
#         return WallSymbol(self._revit_object.kind)
#
#
# class WallSymbol(Symbol):
#
#     @property
#     def family(self):
#         """ Wrapped ``DB.Family`` of the ``DB.Symbol`` """
#         return WallFamily(DB.Wall)
#
#     @property
#     def name(self):
#         return DB.ElementType.Name.GetValue(self._revit_object)
#
#
# class WallFamily(Family):
#
#     @property
#     def symbols(self):
#         """ Gets Symbols of the ``DB.Wall`` """
#         return rpw.Collector(of_class=DB.WallType, is_type=True).elements
#
#     @property
#     def instances():
#         return rpw.Collector(of_class=DB.Wall, is_not_type=True).elements
#
#     @property
#     def category(self):
#         return Category(BicEnum.get('OST_Walls'))
         # category = DB.Category.GetCategory(doc, self._revit_object.Id)
