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

    def __init__(self, element):
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
        super(Element, self).__init__(element)
        if isinstance(element, DB.Element):
            # WallKind Inherits from Family/Element, but is not Element,
            # so ParameterSet fails.
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
            return rpw.db.Collector(**_collector_params)
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
                      'Wall': rpw.db.wall.WallInstance,
                      'WallType': rpw.db.wall.WallSymbol,
                      'WallKind': rpw.db.wall.WallFamily,
                      'Room': rpw.db.spatial_element.Room,
                      'Area': rpw.db.spatial_element.Area,
                      'AreaScheme': rpw.db.spatial_element.AreaScheme,
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
        return rpw.db.Collector(symbol=self._revit_object.Id, is_not_type=True).elements

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
        return rpw.db.Collector(of_category=self._builtin_enum, is_type=True).elements

    @property
    def instances(self):
        """Returns:
            [``DB.FamilyInstance``]: List of Symbol Instances in the Category (unwrapped)
        """
        return rpw.db.Collector(of_category=self._builtin_enum, is_not_type=True).elements

    @property
    def _builtin_enum(self):
        """ Returns BuiltInCategory of the Category """
        return BicEnum.from_category_id(self._revit_object.Id)

    def __repr__(self):
        return super(Category, self).__repr__(self.name)
