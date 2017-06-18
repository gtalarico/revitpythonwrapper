"""
`uidoc.Selection` Wrapper
"""

import rpw
from rpw.revit import revit, DB, UI
from rpw.utils.dotnet import List
from rpw.base import BaseObjectWrapper, BaseObject
from rpw.exceptions import RpwTypeError
from rpw.utils.logger import logger
from rpw.utils.coerce import to_element_ids, to_elements, to_iterable
from rpw.db.collections_ import ElementSet

ObjectType = UI.Selection.ObjectType
PickObjects = revit.uidoc.Selection.PickObjects
PickObject = revit.uidoc.Selection.PickObject

class Selection(BaseObjectWrapper, ElementSet):
    """
    >>> selection = rpw.ui.Selection()
    >>> selection[0]
    FirstElement
    >>> selection.element_ids
    [ SomeElementId, SomeElementId, ...]
    >>> selection.elements
    [ SomeElement, SomeElement, ...]
    >>> len(selection)
    2

    Wrapped Element:
        _revit_object = `Revit.UI.Selection`
    """

    _revit_object_class = UI.Selection.Selection

    def __init__(self, elements_or_ids=None, uidoc=revit.uidoc):
        """
        Initializes Selection. Elements or ElementIds are optional.
        If no elements are provided on intiialization,
        selection handler will be created with selected elements.

        Args:
            elements ([DB.Element or DB.ElementID]): Elements or ElementIds

        >>> selection = Selection(SomeElement)
        >>> selection = Selection(SomeElementId)
        >>> selection = Selection([Element, Element, Element, ...])

        """

        BaseObjectWrapper.__init__(self, uidoc.Selection)
        self.uidoc = uidoc

        if not elements_or_ids:
            elements_or_ids = [e for e in uidoc.Selection.GetElementIds()]

        ElementSet.__init__(self, elements_or_ids, doc=uidoc.Document)

    def add(self, elements_or_ids):
        """ Adds elements to selection.

        Args:
            elements ([DB.Element or DB.ElementID]): Elements or ElementIds

        >>> selection = Selection()
        >>> selection.add(SomeElement)
        >>> selection.add([elements])
        >>> selection.add([element_ids])
        """
        ElementSet.add(self, elements_or_ids)
        self.reset()

    # def update(self):
    #     """ Updates Selection() object to match current selection state"""
    #     Selection.__init__(self, uidoc=self.uidoc)

    def reset(self):
        """ Forces UI selection to match the Selection() object """
        self.uidoc.Selection.SetElementIds(self.as_element_id_list())

    def clear(self):
        """ Clears Selection

        >>> selection = Selection()
        >>> selection.clear()

        Returns:
            None
        """
        ElementSet.clear(self)
        self.reset()

    def __bool__(self):
        """
        Returns:
            bool: `False` if selection  is empty, `True` otherwise

        >>> len(selection)
        2
        >>> Selection() is True
        True
        """
        return bool(len(self))

    def __repr__(self):
        """ Adds data to Base __repr__ to add selection count"""
        return super(Selection, self).__repr__(data={'count': len(self)})


    def _pick(self, obj_type, msg='', multiple=False, world=None):
        if multiple:
            picked = PickObjects(obj_type, msg)
        else:
            picked = PickObject(obj_type, msg)

        elements = to_elements(picked)
        self.add(elements)
        rpw.ui.Console()
        if world:
            picked = [ref.GlobalPoint for ref in picked]
        elif world is False:
            picked = [ref.UVPoint for ref in picked]

        return self.elements if multiple else self.elements[0]

        # else:
        #     return_values = \
        #         [doc.GetElement(ref).GetGeometryObjectFromReference(ref)
        #          for ref in self._refs]

    def pick_element(self, msg='', multiple=False):
        return self._pick(ObjectType.Element, msg=msg, multiple=multiple)

    def pick_element_point(self, msg='', world=False):
        return self._pick(ObjectType.PointOnElement, msg=msg, world=world)

    def pick_point(self, msg=''):
        return revit.wauidoc.Selection.PickPoint(msg)

    def pick_edge(self, msg=''):
        return self._pick(ObjectType.Edge, msg=msg)

    def pick_edges(self, msg=''):
        return self._pick(ObjectType.Edge, msg, multiple=True)

    def pick_face(self, msg=''):
        return self._pick(ObjectType.Face, msg)

    def pick_faces(self, msg=''):
        return self._pick(ObjectType.Face, msg, multiple=True)

    def pick_linked_element(self, msg=''):
        return self._pick(ObjectType.LinkedElement, msg)

    def pick_linked_elements(self, msg=''):
        return self._pick(ObjectType.LinkedElement, msg, multiple=True)

    def pick_point_on_element(self, msg='', world=False):
        return self._pick(ObjectType.PointOnElement, msg, multiple=True, world=world)
