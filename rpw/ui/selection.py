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
ObjectSnapTypes = UI.Selection.ObjectSnapTypes
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
            # Is List of elements is not provided, uses uidoc selection
            elements_or_ids = [e for e in uidoc.Selection.GetElementIds()]

        ElementSet.__init__(self, elements_or_ids, doc=self.uidoc.Document)

    def add(self, elements_or_ids):
        """ Adds elements to selection.

        Args:
            elements ([DB.Element or DB.ElementID]): Elements or ElementIds

        >>> selection = Selection()
        >>> selection.add(SomeElement)
        >>> selection.add([elements])
        >>> selection.add([element_ids])
        """
        # Call Set for proper adding into set.
        ElementSet.add(self, elements_or_ids)
        self.update()

    # def update(self):
    #     """ Updates Selection() object to match current selection state"""
    #     Selection.__init__(self, uidoc=self.uidoc)

    def update(self):
        """ Forces UI selection to match the Selection() object """
        self._revit_object.SetElementIds(self.as_element_id_list())

    def clear(self):
        """ Clears Selection

        >>> selection = Selection()
        >>> selection.clear()

        Returns:
            None
        """
        ElementSet.clear(self)
        self.update()

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
        return super(Selection, self).__repr__(data={'count': len(self)})

    # Other Selection Methods - Keep with Selection? Seems to make sense
    def pick_box(self, msg, style='directional'):
        """ Pick Box Style """
        PICK_STYLE = {'crossing': UI.Selection.PickBoxStyle.Crossing,
                      'enclosing': UI.Selection.PickBoxStyle.Enclosing,
                      'directional': UI.Selection.PickBoxStyle.Directional,
                      }

        refs = self._revit_object.PickBox(PICK_STYLE[style])
        return refs

    def pick_by_rectangle(self, msg):
        # TODO: Implement ISelectFilter overload
        refs = self._revit_object.PickElementsByRectangle(msg)

    def _pick(self, obj_type, msg='Pick:', multiple=False):
        # TODO: Implement ISelectFilter overload
        """ Note: Moved Reference Logic to Referenc Wrapper."""
        if multiple:
            references = PickObjects(obj_type, msg)
        else:
            references = PickObject(obj_type, msg)

        self.add(references)
        return references

    def pick_element(self, msg='Pick Element(s)', multiple=False):
        return self._pick(ObjectType.Element, msg=msg, multiple=multiple)

    def pick_pt_on_element(self, msg='Pick Pt On Element(s)', multiple=False):
        return self._pick(ObjectType.PointOnElement, msg=msg, multiple=multiple)

    def pick_edge(self, msg='Pick Edge(s)', multiple=False):
        return self._pick(ObjectType.Edge, msg=msg, multiple=multiple)

    def pick_face(self, msg='Pick Face(s)', multiple=False):
        return self._pick(ObjectType.Face, msg=msg, multiple=multiple)

    def pick_linked_element(self, msg='Pick Linked Element', multiple=False):
        return self._pick(ObjectType.LinkedElement, msg=msg, multiple=multiple)

    def pick_pt(self, msg='Pick Point', snap=None):
        """ Selects a XYZ This does not add eleents to selection """

        SNAPS = {'none': ObjectSnapTypes.None,
                 'endpoints':ObjectSnapTypes.Endpoints,
                 'midpoints':ObjectSnapTypes.Midpoints,
                 'nearest':ObjectSnapTypes.Nearest,
                 'workplanegrid':ObjectSnapTypes.WorkPlaneGrid,
                 'intersections':ObjectSnapTypes.Intersections,
                 'centers':ObjectSnapTypes.Centers,
                 'perpendicular':ObjectSnapTypes.Perpendicular,
                 'tangents':ObjectSnapTypes.Tangents,
                 'quadrants':ObjectSnapTypes.Quadrants,
                 'points':ObjectSnapTypes.Points,
                 }
        if snap:
            return self._revit_object.PickPoint(SNAPS[snap], msg)
        else:
            return self._revit_object.PickPoint(msg)


class SelectionFilter(UI.Selection.ISelectionFilter):
    # http://www.revitapidocs.com/2017.1/d552f44b-221c-0ecd-d001-41a5099b2f9f.htm
    # Also See Ehsan's Implemented
    def __init__(self):
        raise NotImplemented
