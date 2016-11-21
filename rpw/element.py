"""
Element Wrappers provide helpful to accessing parameters and properties
as shown below.

The ``Element`` class is the base class for all Revit objects that inherit from Element.

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
    Inheriting from element extends wrapped elements with a new :class:`parameters`
    attribute, well as the :func:`unwrap` method inherited from the :any:`BaseObjectWrapper` class.

    It can be created by instantiating ``rpw.Element`` , or one of the helper
    static methods shown below.

    Most importantly, all other `Element-related` classes inhert from this class
    so it can provide parameter access.

    >>> element = rpw.Element(SomeElement)
    >>> element = rpw.Element.from_id(ElementId)
    >>> element = rpw.Element.from_int(Integer)

    >>> wall = rpw.Element(RevitWallElement)
    >>> wall.Id
    >>> wall.parameters['Height'].value
    10.0

    Attributes:

        parameters (:any:`ParameterSet`): Access :any:`ParameterSet` class.
        parameters['ParamName'] (:any:`Parameter`): Returns :any:`Parameter` class instance if match is found.
        parameters.builtins['BuiltInName'] (:any:`Parameter`): BuitIn :any:`Parameter` object

    Methods:
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
        This Factory function is used to Construct classes witout specifying the
        exact class. On instantiation, it will attempt to map the type provided,
        if a match is not found an exception is raised.

        This is generically, without knowing the type will come through later.
        This is primarily used to keep the base Instance, Symbol, and Family Classes
        generic.

        >>> wall_instance = Element.Factory(SomeWallInstance)
        >>> type(wall_instance)
        rpw.element.WallInstance
        >>> wall_symbol = Element.Factory(SomeWallSymbol)
        >>> type(wall_symbol)
        rpw.element.WallSymbol
        """
        CLASS_MAP = {
                      'FamilyInstance': Instance,
                      'FamilySymbol': Symbol,
                      'Family': Family,
                      'Category': Category,
                      'Wall': WallInstance,
                      'WallType': WallSymbol,
                      'WallKind': WallFamily,
                    }

        element_class = CLASS_MAP[element.__class__.__name__]
        return element_class(element)

    def __repr__(self, data=None):
        data = data if data else self._revit_object
        return super(Element, self).__repr__(str(data))


class Instance(Element):
    """
    `DB.FamilyInstance` Wrapper

    >>> instance = rpw.Instance(SomeFamilyInstance)
    <RPW_Symbol:72" x 36">
    >>> instance.symbol.name
    '72" x 36"'
    >>> instance.family
    <RPW_Family:desk>
    >>> instance.siblings
    [<RPW_Instance:72" x 36">, <RPW_Instance:72" x 36">, ... ]

    Attribute:
        _revit_object (DB.FamilyInstance): Wrapped ``DB.FamilyInstance``
    """
    def __init__(self, instance, enforce_type=DB.FamilyInstance):
        """
        Args:
            instance (``DB.FamilyInstance``): Instance of FamilyInstance to be wrapped
        """
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
        """ Wrapped ``DB.Category`` of the ``DB.Symbol`` """
        return self.family.category

    @property
    def siblings(self):
        """ Other ``DB.FamilyInstance`` of the same ``DB.FamilySymbol`` """
        return self.symbol.instances

    def __repr__(self):
        return super(Instance, self).__repr__(self.symbol.name)


class Symbol(Element):
    """
    `DB.FamilySymbol` Wrapper

    >>> symbol = rpw.Symbol(SomeSymbol)
    <RPW_Symbol:72" x 36">
    >>> instance.symbol.name
    '72" x 36"'
    >>> instance.family
    <RPW_Family:desk>
    >>> instance.siblings
    <RPW_Instance:72" x 36">, <RPW_Instance:72" x 36">, ... ]

    Attribute:
        _revit_object (DB.FamilySymbol): Wrapped ``DB.FamilySymbol``
    """

    def __init__(self, symbol, enforce_type=DB.FamilySymbol):
        """
        Args:
            symbol (``DB.FamilySymbol``): Instance of FamilySymbol to be wrapped
        """
        super(Symbol, self).__init__(symbol, enforce_type=enforce_type)

    @property
    def name(self):
        """ Returns the name of the Symbol """
        return self.parameters.builtins['SYMBOL_NAME_PARAM'].value
        # return self.parameters.builtins['ALL_MODEL_TYPE_NAME'].value

    @property
    def family(self):
        """Returns:
            :any:`Family`: Wrapped ``DB.Family`` of the symbol """
        return Family(self._revit_object.Family)

    @property
    def instances(self):
        """Returns:
            [``DB.FamilyInstance``]: List of model instances of the symbol (unwrapped)
        """
        return rpw.Collector(symbol=self._revit_object.Id, is_not_type=True).elements

    @property
    def siblings(self):
        """Returns:
            [``DB.FamilySymbol``]: List of symbol Types of the same Family (unwrapped)
        """
        symbols_ids = self._revit_object.GetSimilarTypes()
        return [doc.GetElement(i) for i in symbols_ids]
        # Same as: return self.family.symbols

    @property
    def category(self):
        """Returns:
        :any:`Category`: Wrapped ``DB.Category`` of the symbol """
        return self.family.category

    def __repr__(self):
        return super(Symbol, self).__repr__(self.name)


class Family(Element):
    """
    `DB.Family` Wrapper

    Attribute:
        _revit_object (DB.Family): Wrapped ``DB.Family``
    """

    def __init__(self, family, enforce_type=DB.Family):
        """Args:
            family (``DB.FamilySymbol``): Instance of FamilySymbol to be wrapped
        """
        super(Family, self).__init__(family, enforce_type=enforce_type)

    @property
    def name(self):
        """ Returns:
            ``str``: name of the Family """
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
        """Returns:
            [``DB.FamilyInstance``]: List of model instances in this family (unwrapped)
        """
        # There has to be a better way
        instances = []
        for symbol in self.symbols:
            symbol_instances = Element.Factory(symbol).instances
            instances.append(symbol_instances)
        return instances

    @property
    def symbols(self):
        """Returns:
            [``DB.FamilySymbol``]: List of Symbol Types in the family (unwrapped)
        """
        symbols_ids = self._revit_object.GetFamilySymbolIds()
        return [doc.GetElement(i) for i in symbols_ids]

    @property
    def category(self):
        """Returns:
            :any:`Category`: Wrapped ``DB.Category`` of the Family """
        return Category(self._revit_object.FamilyCategory)

    @property
    def siblings(self):
        """Returns:
            [``DB.Family``]: List of Family elements in the same category (unwrapped)
        """
        return self.category.families

    def __repr__(self):
        return super(Family, self).__repr__(self.name)


class Category(BaseObjectWrapper):
    """
    `DB.Category` Wrapper

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
        """Returns:
            [``DB.Family``]: List of Family elements in this same category (unwrapped)
        """
        # There has to be a better way, but perhaps not: https://goo.gl/MqdzWg
        symbols = self.symbols
        unique_family_ids = set()
        for symbol in symbols:
            symbol_family = Element.Factory(symbol).family
            unique_family_ids.add(symbol_family.Id)
        return [doc.GetElement(family_id) for family_id in unique_family_ids]

    @property
    def symbols(self):
        """Returns:
            [``DB.FamilySymbol``]: List of Symbol Types in the Category (unwrapped)
        """
        return rpw.Collector(of_category=self._builtin_enum, is_type=True).elements

    @property
    def instances(self):
        """Returns:
            [``DB.FamilyInstance``]: List of Symbol Instances in the Category (unwrapped)
        """
        return rpw.Collector(of_category=self._builtin_enum, is_not_type=True).elements

    @property
    def _builtin_enum(self):
        """ Returns BuiltInCategory of the Category """
        return BicEnum.from_category_id(self._revit_object.Id)

    def __repr__(self):
        return super(Category, self).__repr__(self.name)


class WallInstance(Instance):
    """
    Inherits base ``Instance`` and overrides symbol attribute to
    get `Symbol` equivalent of Wall `(GetTypeId)`
    """
    def __init__(self, wall_instance):
        super(WallInstance, self).__init__(wall_instance, enforce_type=DB.Wall)

    @property
    def symbol(self):
        wall_type_id = self._revit_object.GetTypeId()
        wall_type = doc.GetElement(wall_type_id)
        return WallSymbol(wall_type)


class WallSymbol(Symbol):
    """
    Inherits from :any:`Symbol` and overrides:
        * :func:`family` to get the `Family` equivalent of Wall `(.Kind)`
        * Uses a different method to get instances.
    """
    def __init__(self, wall_symbol):
        super(WallSymbol, self).__init__(wall_symbol, enforce_type=DB.WallType)

    @property
    def family(self):
        """ Returns ``DB.Family`` of the Symbol """
        return WallFamily(self._revit_object.Kind)

    @property
    def instances(self):
        """ Returns all Instances of this Wall Types """
        bip = BipEnum.get_id('SYMBOL_NAME_PARAM')
        param_filter = rpw.collector.ParameterFilter(bip, equals=self.name)
        return rpw.Collector(of_class=DB.Wall, parameter_filter=param_filter,
                             is_not_type=True).elements

    @property
    def siblings(self):
        return self.family.symbols


class WallFamily(Family):
    """
    Inherits base ``Family`` and overrides methods for Wall Instance`
    """
    def __init__(self, wall_family):
        super(WallFamily, self).__init__(wall_family, enforce_type=DB.WallKind)

    @property
    def symbols(self):
        symbols = rpw.Collector(of_class=DB.WallType, is_type=True).elements
        return [symbol for symbol in symbols if symbol.Kind == self._revit_object]

    @property
    def category(self):
        wall_type = rpw.Collector(of_class=DB.WallType, is_type=True).first
        return WallCategory(wall_type.Category)


class WallCategory(Category):

    def __init__(self, wall_category):
        super(WallCategory, self).__init__(wall_category)
    """
    ``DB.Category`` Wall Category Wrapper

    Attribute:
        _revit_object (DB.Family): Wrapped ``DB.Category``
    """
    @property
    def families(self):
        """ Returns ``DB.WallKind`` elements in the category """
        wall_kinds = []
        for member in dir(DB.WallKind):
            if type(getattr(DB.WallKind, member)) is DB.WallKind:
                wall_kinds.append(getattr(DB.WallKind, member))
        return wall_kinds
