""" Collection of Class Mixins """

from rpw import revit, DB
from rpw.db.element import Element
from rpw.exceptions import RpwCoerceError


class ByNameCollectMixin():

    @classmethod
    def by_name(cls, name):
        """ Mixin to provide instantiating by a name for classes that are collectible """
        first = cls.collect(where=lambda e: e.Name == name).first
        if first:
            return cls(first)
        else:
            raise RpwCoerceError('by_name({})'.format(name), cls)


    @classmethod
    def by_name_or_element_ref(cls, reference, doc=revit.doc):
        """
        Mixin for collectible elements.
        This is to help cast elements from name, elemente, or element_id
        """
        if isinstance(reference, str):
            return cls.by_name(reference)
        elif isinstance(reference, DB.ElementId):
            return Element.from_id(reference)
        else:
            return cls(reference)
