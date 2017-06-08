"""
Element Wrappers provide a consitent interface for acccessing parameters and properties
of commonly used elements.

Note:
    These wrappers are located in the module ``rpw.elements``,
    but all of them are imported by into the main module so they can be accessed
    using ``rpw.Element``, ``rpw.Instance``, etc.

"""
import inspect

import rpw
from rpw import revit, DB
from rpw.db.parameter import Parameter, ParameterSet
from rpw.base import BaseObjectWrapper

doc, uidoc = revit.doc, revit.uidoc

from rpw.exceptions import RPW_Exception, RPW_WrongStorageType
from rpw.exceptions import RPW_ParameterNotFound, RPW_TypeError
from rpw.utils.logger import logger

from rpw.db.builtins import BicEnum, BipEnum


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

    _revit_object_class = DB.Element

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

    @classmethod
    def collect(cls, **kwargs):
        """ Collect all elements of the wrapper, using the default collector.

        Collector will use default params for that Element (ie: Room ``{'of_category': 'OST_rooms'}``).
        These can be overriden by passing keyword args to the collectors call.


        >>> rooms = rpw.Rooms.collect()
        [<RPW_Room: Room:1>]
        >>> rooms = rpw.Area.collect()
        [<RPW_Area: Rentable:30.2>]
        >>> rooms = rpw.WallInstance.collect()
        [<RPW_WallInstance: Basic Wall>]

        """
        _collector_params = getattr(cls, '_collector_params', None)

        if _collector_params:
            _collector_params.update(**kwargs)
            return rpw.Collector(**_collector_params)
        else:
            raise RPW_Exception('Wrapper cannot collect by class: {}'.format(cls.__name__))

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
        if a match is not found, an Element will be used.
        If the element does not inherit from DB.Element, and exception is raised.

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

        # TODO: Auto-detect by iterating over types in element.py
        CLASS_MAP = {
                      'FamilyInstance': Instance,
                      'FamilySymbol': Symbol,
                      'Family': Family,
                      'Category': Category,
                      'Wall': WallInstance,
                      'WallType': WallSymbol,
                      'WallKind': WallFamily,
                      'Room': Room,
                      'Area': Area,
                      'AreaScheme': AreaScheme,
                    }
        element_class_name = element.__class__.__name__
        element_class = CLASS_MAP.get(element_class_name)
        if not element_class:
            if DB.Element in inspect.getmro(element.__class__):
                return Element(element)
            else:
                raise RPW_Exception('Factory does not support type: {}'.format(element_class_name))
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

    _revit_object_class = DB.FamilyInstance
    _collector_params = {'of_class': _revit_object_class, 'is_not_type': True}


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
    _revit_object_class = DB.FamilySymbol
    _collector_params = {'of_class': _revit_object_class, 'is_type': True}

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

    _revit_object_class = DB.Family
    _collector_params = {'of_class': _revit_object_class, 'is_type': True}

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
        # Uses generic factory so it can be inherited by others
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

    _revit_object_class = DB.Category

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

    _revit_object_category = DB.BuiltInCategory.OST_Walls
    _revit_object_class = DB.Wall
    _collector_params = {'of_class': _revit_object_class, 'is_not_type': True}

    def __init__(self, wall_instance, enforce_type=DB.Wall):
        super(WallInstance, self).__init__(wall_instance, enforce_type=enforce_type)

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

    _revit_object_class = DB.WallType
    _collector_params = {'of_class': _revit_object_class, 'is_type': True}

    def __init__(self, wall_symbol, enforce_type=DB.WallType):
        super(WallSymbol, self).__init__(wall_symbol, enforce_type=enforce_type)

    @property
    def family(self):
        """ Returns ``DB.Family`` of the Symbol """
        return WallFamily(self._revit_object.Kind)

    @property
    def instances(self):
        """ Returns all Instances of this Wall Types """
        bip = BipEnum.get_id('SYMBOL_NAME_PARAM')
        param_filter = rpw.collector.ParameterFilter(bip, equals=self.name)
        return rpw.Collector(parameter_filter=param_filter,
                             **WallInstance._collector_params).elements

    @property
    def siblings(self):
        return self.family.symbols


class WallFamily(Family):
    """
    Inherits base ``Family`` and overrides methods for Wall Instance`
    """

    _revit_object_class = DB.WallKind

    def __init__(self, wall_family, enforce_type=None):
        if not enforce_type:
            enforce_type = self.__class__._revit_object_class
        super(WallFamily, self).__init__(wall_family, enforce_type=enforce_type)

    @property
    def symbols(self):
        symbols = rpw.Collector(**WallSymbol._collector_params).elements
        return [symbol for symbol in symbols if symbol.Kind == self._revit_object]

    @property
    def category(self):
        wall_type = rpw.Collector(of_class=DB.WallType, is_type=True).first
        return WallCategory(wall_type.Category)


class WallCategory(Category):
    """
    ``DB.Category`` Wall Category Wrapper

    Attribute:
        _revit_object (DB.Family): Wrapped ``DB.Category``
    """

    _revit_object_class = DB.Category

    @property
    def families(self):
        """ Returns ``DB.WallKind`` elements in the category """
        wall_kinds = []
        for member in dir(DB.WallKind):
            if type(getattr(DB.WallKind, member)) is DB.WallKind:
                wall_kinds.append(getattr(DB.WallKind, member))
        return wall_kinds


class Room(Element):
    """
    `DB.Architecture.Room` Wrapper
    Inherits from :any:`Element`

    >>> room = rpw.Room(SomeRoom)
    <RPW_Room: Office:122>
    >>> room.name
    'Office'
    >>> room.number
    '122'
    >>> room.is_placed
    True
    >>> room.is_bounded
    True

    Attribute:
        _revit_object (DB.Architecture.Room): Wrapped ``DB.Architecture.Room``
    """

    _revit_object_class = DB.Architecture.Room
    _revit_object_category = DB.BuiltInCategory.OST_Rooms
    _collector_params = {'of_category': _revit_object_category,
                         'is_not_type': True}

    def __init__(self, room, enforce_type=None):
        """
        Args:
            room (``DB.Architecture.Room``): Room to be wrapped
        """
        if not enforce_type:
            enforce_type = self.__class__._revit_object_class
        super(Room, self).__init__(room, enforce_type=enforce_type)

    @property
    def name(self):
        """ Room Name as parameter Value: ``ROOM_NAME`` built-in parameter"""
        # Note: For an unknown reason, roominstance.Name does not work on IPY
        return self.parameters.builtins['ROOM_NAME'].value

    @name.setter
    def name(self, value):
        self.parameters.builtins['ROOM_NAME'].value = value

    @property
    def number(self):
        """ Room Number as parameter Value: ``ROOM_NUMBER`` built-in parameter"""
        return self.parameters.builtins['ROOM_NUMBER'].value

    @number.setter
    def number(self, value):
        self.parameters.builtins['ROOM_NUMBER'].value = value

    @property
    def is_placed(self):
        """ ``bool`` for whether Room is Placed.
        Uses result of ``Room.Location`` attribute to define if room is Placed.
        """
        return bool(self._revit_object.Location)

    @property
    def is_bounded(self):
        """ ``bool`` for whether Room is Bounded.
        Uses result of ``Room.Area`` attribute to define if room is Bounded.
        """
        return self._revit_object.Area > 0

    def __repr__(self):
        return super(Room, self).__repr__(data='{}:{}'.format(self.name, self.number))


class Area(Room):
    """
    `DB.Area` Wrapper
    Inherits from :any:`Room`

    >>> area = rpw.Area(SomeArea)
    <RPW_Room: Office:122>
    >>> area.name
    'Rentable'
    >>> area.is_placed
    True
    >>> area.is_bounded
    True

    Attribute:
        _revit_object (DB.Area): Wrapped ``DB.Area``
    """

    _revit_object_class = DB.Area
    _revit_object_category = DB.BuiltInCategory.OST_Areas
    _collector_params = {'of_category': _revit_object_category,
                         'is_not_type': True}

    def __init__(self, area, enforce_type=None):
        """
        Args:
            area (``DB.Area``): Area Instance to be wrapped
        """
        super(Area, self).__init__(area, enforce_type=enforce_type)

    @property
    def name(self):
        """ Area Scheme Name: Area attribute parameter"""
        return self.scheme.name

    @property
    def scheme(self):
        """ Area Scheme: Wrapped Area Scheme"""
        return AreaScheme(self._revit_object.AreaScheme)

    @property
    def area(self):
        """ Area: .Area attribute"""
        return self._revit_object.Area

    def __repr__(self):
        return super(Element, self).__repr__(data='{}:{}'.format(self.name, self.area))

class AreaScheme(Element):
    """
    `DB.AreaScheme` Wrapper
    Inherits from :any:`Element`

    >>>

    Attribute:
        _revit_object (DB.AreaScheme): Wrapped ``DB.AreaScheme``
    """

    _revit_object_class = DB.AreaScheme
    _collector_params = {'of_class': _revit_object_class}

    def __init__(self, area_scheme):
        """
        Args:
            area (``DB.Area``): Area Instance to be wrapped
        """
        enforce_type = self.__class__._revit_object_class
        super(AreaScheme, self).__init__(area_scheme, enforce_type=enforce_type)

    @property
    def name(self):
        """ Area Scheme Name: Area attribute parameter"""
        return self._revit_object.Name

    @property
    def areas(self):
        """ Returns all Area Instances of this Area Scheme """
        bip = BipEnum.get_id('AREA_SCHEME_ID')
        param_filter = rpw.collector.ParameterFilter(bip, equals=self._revit_object.Id)
        collector = rpw.Collector(parameter_filter=param_filter,
                                  **Area._collector_params)
        return collector.wrapped_elements

    def __repr__(self):
        return super(AreaScheme, self).__repr__(data='{}'.format(self.name))
