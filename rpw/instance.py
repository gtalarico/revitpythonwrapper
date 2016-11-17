"""
Instance Tree

Helps navigate an Instance > FamilySymbol > Family > Category Tree

# TODO: How does this relate to rpw.Element? All these Inherit from Element,
except Category


# TODO: Finish wall specific handler
# TODO: Add tests to symbol collector

from rpw.instance import Instance

for element in rpw.Selection():
    instance = Instance(element)
    print(element)

    logger.title('Instance:')
    print(instance)
    logger.title('Symbol:')
    print(instance.symbol)
    logger.title('Instances:')
    print(instance.symbol.instances)
    logger.title('Symbol Name:')
    print(instance.symbol.name)
    logger.title('Family:')
    print(instance.symbol.family)
    logger.title('Family Name:')
    print(instance.symbol.family.name)
    logger.title('Symbol Siblings:')
    print(instance.symbol.siblings)
    logger.title('Familly Siblings (Other Symbols):')
    print(instance.symbol.family.symbols)
    logger.title('Category:')
    print(instance.symbol.family.category)
    logger.title('Category Name:')
    print(instance.symbol.family.category.name)

sys.exit()

"""

import rpw
from rpw import doc, DB
from rpw.exceptions import RPW_TypeError
from Autodesk.Revit import DB
# FIXME: But requires re-importing it
# TODO: Decide if should return wrapped


class Instance(rpw.Element):
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


class Symbol(rpw.Element):
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


class Family(rpw.Element):
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
        # category = DB.Category.GetCategory(doc, self._revit_object.Id)
        # return Category(category)

    @property
    def siblings(self):
        return self.category.families

    def __repr__(self):
        return super(Family, self).__repr__(self.name)


class Category(rpw.base.BaseObjectWrapper):
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
        return rpw.Collector(of_category=self._revit_object,
                             is_type=True).elements

    @property
    def instances(self):
        return rpw.Collector(of_category=self._revit_object,
                             is_not_type=True).elements

    @property
    def parent(self):
        return self._revit_object.Parent
        # return Category(self._revit_object.Parent)

    @property
    def type(self):
        """
        CategoryType Enumeration:
        | CategoryType.Model, CategoryType.Annotation
        | CategoryType.Invalid, CategoryType.Annotation,
        | CategoryType.AnalyticalModel
        """
        return self._revit_object.CategoryType

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
#         # TODO: As on forum, why FamilySymbol.Name doesn't work ?
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
