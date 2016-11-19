"""
Something
"""

import rpw
from rpw import doc, uidoc, DB
from rpw.parameter import Parameter, ParameterSet
from rpw.base import BaseObjectWrapper

from rpw.exceptions import RPW_Exception, RPW_WrongStorageType
from rpw.exceptions import RPW_ParameterNotFound, RPW_TypeError
from rpw.utils.logger import logger

from rpw.enumeration import BicEnum, BipEnum


class Element(BaseObjectWrapper):
    """
    All Element Base Objects inherit from this class and have the attributes and methods listed below.

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

        parameters (:any:`ParameterSet`): Access :any:`ParameterSet` class.
        parameters['ParamName'] (:any:`Parameter`): Returns :any:`Parameter` class instance if match is found.
        parameters.builtins['BuiltInName'] (:any:`Parameter`): BuitIn :any:`Parameter` object

        unwrap(): Wrapped Revit Reference

    """

    def __init__(self, element, enforce_type=None):
        """
        Args:
            element (Element Reference): Can be ``DB.Element``, ``DB.ElementId``, or ``int``.

        Returns:
            :class:`Element`: Instance of Wrapped Element

        Usage:
            >>> wall = Element(SomeElementId)
            >>> wall.parameters['Height']
            >>> wall.parameters.builtins['WALL_LOCATION_LINE']
        """
        super(Element, self).__init__(element, enforce_type=enforce_type)
        self.parameters = ParameterSet(element)

    @property
    def id_as_int(self):
        """ Example of mapping existing properties"""
        return self._revit_object.Id.IntegerValue

    @staticmethod
    def from_int(id_int):
        element = doc.GetElement(DB.ElementId(id_int))
        return Element(element)

    @staticmethod
    def from_id(element_id):
        element = doc.GetElement(element_id)
        return Element(element)

    @staticmethod
    def Factory(element):
        """
        This Factory function is used to Classes can be instantiated
        generically, without knowing the type will come through later.
        This is primarily used to keep the base Instance, Symbol, and Family Classes
        generic.
        """
        CLASS_MAP = {
                      'FamilyInstance': Instance,
                      'FamilySymbol': Symbol,
                      'Family': Family,
                      'Category': Category,
                      'Wall': WallInstance,
                      'WallType': WallSymbol,
                      'WallKind': WallFamily,
                      'WallKind': WallFamily,
                    }

        element_class = CLASS_MAP[element.__class__.__name__]
        return element_class(element)

    def __repr__(self, data=None):
        data = data if data else self._revit_object
        return super(Element, self).__repr__(str(data))


class Instance(Element):
    """
    ``DB.FamilyInstance`` Wrapper

    Attribute:
        _revit_object (DB.FamilyInstance): Wrapped ``DB.FamilyInstance`` or
        other placeable such as DB.Wall
    """
    def __init__(self, instance, enforce_type=DB.FamilyInstance):
        super(Instance, self).__init__(instance, enforce_type=enforce_type)

    @property
    def symbol(self):
        """ Wrapped ``DB.FamilySymbol`` of the ``DB.FamilyInstance`` """
        symbol = self._revit_object.Symbol
        return Symbol(symbol)

    @property
    def family(self):
        """ Wrapped ``DB.Family`` of the ``DB.FamilyInstance`` """
        return self.symbol.family

    @property
    def category(self):
        """ Wrapped ``DB.Family`` of the ``DB.Symbol`` """
        return self.family.category

    @property
    def siblings(self):
        """ Other ``DB.FamilyInstance`` of the same ``DB.FamilySymbol`` """
        return self.symbol.instances

    def __repr__(self):
        return super(Instance, self).__repr__(self.symbol.name)


class Symbol(Element):
    """
    ``DB.FamilySymbol`` Wrapper

    Attribute:
        _revit_object (DB.FamilySymbol): Wrapped ``DB.FamilySymbol``
    """

    def __init__(self, symbol, enforce_type=DB.FamilySymbol):
        """
        Usage:
            >>> symbol = Symbol(SomeFamilySymbol)
        """
        super(Symbol, self).__init__(symbol, enforce_type=enforce_type)

    @property
    def name(self):
        return self.parameters.builtins['SYMBOL_NAME_PARAM'].value
        # return self.parameters.builtins['ALL_MODEL_TYPE_NAME'].value

    @property
    def family(self):
        """ Wrapped ``DB.Family`` of the ``DB.Symbol`` """
        return Family(self._revit_object.Family)

    @property
    def category(self):
        """ Wrapped ``DB.Family`` of the ``DB.Symbol`` """
        return self.family.category

    @property
    def instances(self):
        """ Returns ``DB.FamilyInstance`` instances in of this Symbol """
        return rpw.Collector(symbol=self._revit_object.Id).elements

    @property
    def siblings(self):
        """ Gets sibling Symbols of the same``DB.Family`` """
        symbols_ids = self._revit_object.GetSimilarTypes()
        return [doc.GetElement(i) for i in symbols_ids]
        # Same as: return self.family.symbols

    def __repr__(self):
        return super(Symbol, self).__repr__(self.name)


class Family(Element):
    """
    ``DB.Family`` Wrapper

    Attribute:
        _revit_object (DB.Family): Wrapped ``DB.Family``
    """

    def __init__(self, family, enforce_type=DB.Family):
        super(Family, self).__init__(family, enforce_type=enforce_type)

    @property
    def name(self):
        """ Returns name of the Family """
        # This BIP only exist in symbols, so we retrieve a symbol first.
        # The Alternative is to use Element.Name.GetValue(), but I am
        # avoiding it due to the import bug in ironpython
        try:
            symbol = self.symbols[0]
        except IndexError:
            raise RPW_Exception('Family [{}] has no symbols'.format(self.name))
        return Element.Factory(symbol).parameters.builtins['SYMBOL_FAMILY_NAME_PARAM'].value
        # Alternative: ALL_MODEL_FAMILY_NAME

    @property
    def instances(self):
        """ Returns ``DB.FamilyInstace`` instances of this Family """
        # There has to be a better way
        instances = []
        for symbol in self.symbols:
            symbol_instances = Element.Factory(symbol).instances
            instances.append(symbol_instances)
        return instances

    @property
    def symbols(self):
        """ Returns ``DB.FamilySymbol`` symbols in family """
        symbols_ids = self._revit_object.GetFamilySymbolIds()
        return [doc.GetElement(i) for i in symbols_ids]

    @property
    def category(self):
        """ Returns ``DB.Category`` of this Family """
        return Category(self._revit_object.FamilyCategory)

    @property
    def siblings(self):
        """ Returns ``DB.Family`` in the same category """
        return self.category.families

    def __repr__(self):
        return super(Family, self).__repr__(self.name)


class Category(BaseObjectWrapper):
    """
    ``DB.Category`` Wrapper

    Attribute:
        _revit_object (DB.Family): Wrapped ``DB.Category``
    """
    def __init__(self, category, enforce_type=DB.Category):
        super(Category, self).__init__(category, enforce_type=enforce_type)

    @property
    def name(self):
        """ Returns name of the Category """
        return self._revit_object.Name

    @property
    def families(self):
        """ Returns ``DB.Family`` family elements in the category """
        # There has to be a better way, but perhaps not: https://goo.gl/MqdzWg
        symbols = self.symbols
        unique_family_ids = set()
        for symbol in symbols:
            symbol_family = Element.Factory(symbol).family
            unique_family_ids.add(symbol_family.Id)
        return [doc.GetElement(family_id) for family_id in unique_family_ids]

    @property
    def symbols(self):
        return rpw.Collector(of_category=self._builtin_enum, is_type=True).elements

    @property
    def instances(self):
        return rpw.Collector(of_category=self._builtin_enum, is_not_type=True).elements

    @property
    def _builtin_enum(self):
        return BicEnum.from_category_id(self._revit_object.Id)

    def __repr__(self):
        return super(Category, self).__repr__(self.name)


class WallInstance(Instance):

    def __init__(self, wall_instance):
        super(WallInstance, self).__init__(wall_instance, enforce_type=DB.Wall)

    @property
    def symbol(self):
        wall_type_id = self._revit_object.GetTypeId()
        wall_type = doc.GetElement(wall_type_id)
        return WallSymbol(wall_type)


class WallSymbol(Symbol):

    def __init__(self, wall_symbol):
        super(WallSymbol, self).__init__(wall_symbol, enforce_type=DB.WallType)

    @property
    def family(self):
        """ Wrapped ``DB.Family`` of the ``DB.Symbol`` """
        return WallFamily(self._revit_object.Kind)

    @property
    def instances(self):
        """ Returns ``DB.FamilyInstance`` instances in of this Symbol """
        bip = BipEnum.get_id('SYMBOL_NAME_PARAM')
        param_filter = rpw.collector.ParameterFilter(bip, equals=self.name)
        return rpw.Collector(of_class=DB.Wall, parameter_filter=param_filter,
                             is_not_type=True).elements

    @property
    def siblings(self):
        """ Gets sibling Symbols of the same``DB.Family``
        """
        return self.family.symbols


class WallFamily(Family):

    def __init__(self, wall_family):
        super(WallFamily, self).__init__(wall_family, enforce_type=DB.WallKind)

    @property
    def symbols(self):
        """ Gets Symbols of the ``DB.Wall`` """
        symbols = rpw.Collector(of_class=DB.WallType, is_type=True).elements
        return [symbol for symbol in symbols if symbol.Kind == self._revit_object]

    @property
    def instances(self):
        """ Retrieves Instances of the family """
        return rpw.Collector(of_class=DB.Wall, is_not_type=True).elements

    @property
    def category(self):
        """ Retrieves Category of Wall Types """
        wall_type = rpw.Collector(of_class=DB.WallType, is_type=True).first
        return WallCategory(wall_type.Category)

    @property
    def siblings(self):
        """ Gets sibling Symbols of the same``DB.Family``
        """
        return self.category.families


class WallCategory(Category):

    def __init__(self, wall_category):
        super(WallCategory, self).__init__(wall_category)

    @property
    def families(self):
        """ Returns ``DB.WallKind`` elements in the category """
        wall_kinds = []
        for member in dir(DB.WallKind):
            if type(getattr(DB.WallKind, member)) is DB.WallKind:
                wall_kinds.append(getattr(DB.WallKind, member))
        return wall_kinds
