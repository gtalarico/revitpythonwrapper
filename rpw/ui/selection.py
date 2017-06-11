"""
`uidoc.Selection` Wrapper
"""

from rpw.revit import revit, DB, UI
from rpw.utils.dotnet import List
from rpw.base import BaseObjectWrapper
from rpw.exceptions import RPW_TypeError
from rpw.utils.logger import logger
from rpw.utils.coerce import to_element_ids

doc, uidoc = revit.doc, revit.uidoc

class Selection(BaseObjectWrapper):
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

    def __init__(self, elements=None, uidoc=revit.uidoc):
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
        super(Selection, self).__init__(uidoc.Selection)
        if elements:
            self.add(elements)

    def add(self, elements_or_ids):
        """ Adds elements to selection.

        Args:
            elements ([DB.Element or DB.ElementID]): Elements or ElementIds

        >>> selection = Selection()
        >>> selection.add(SomeElement)
        >>> selection.add([elements])
        >>> selection.add([element_ids])
        """
        if not isinstance(elements_or_ids, (list, set)):
            elements_or_ids = [elements_or_ids]
        element_ids = to_element_ids(elements_or_ids)

        current_selection = [e for e in uidoc.Selection.GetElementIds()]
        new_selection = element_ids + current_selection
        uidoc.Selection.SetElementIds(List[DB.ElementId](new_selection))

    @property
    def element_ids(self):
        """
        Gets list of ```ElemendId`` in selection

        Returns:
            [DB.ElementId]: List of ElementIds Objects """
        return [eid for eid in self._revit_object.GetElementIds()]

    @property
    def elements(self):
        """
        Gets list of ```Elemend`` in selection

        Returns:
            [DB.Element]: List of Elements """
        return [doc.GetElement(eid) for eid in self.element_ids]


    def clear(self):
        """ Clears Selection

        >>> selection = Selection()
        >>> selection.clear()

        Returns:
            None
        """
        uidoc.Selection.SetElementIds(List[DB.ElementId]())

    def __getitem__(self, index):
        """
        Retrieves element in seleciton using index.
        If Index is out range, ``None`` is returned

        Args:
            int: Integer representing item index in ``selection.elements``

        Returns:
            ``DB.Element``, ``None``: Item at Index, or None

        >>> selection[0]
        < Revit.DB.Element >
        """
        return self.elements[index]

    def __contains__(self, element_reference):
        """
        Checks if selection contains the element Reference.
        Args:
            Reference: Element, ElementId, or Integer
        Returns:
            bool: ``True`` or ``False``
        """
        element_ids = to_element_ids(element_reference)
        if len(element_ids) != 1:
            raise RPW_TypeError('element_reference', type(element_reference))
        element_id = element_ids[0]
        return any([e == element_id for e in self.element_ids])

    def __bool__(self):
        """
        Returns:
            bool: `False` if selection  is empty, `True` otherwise

        >>> len(selection)
        2
        >>> Selection() is True
        True
        >>> bool(selection)
        True
        >>> selection.clear()
        >>> bool(selection)
        False
        """
        return bool(self.elements)

    def __len__(self):
        """ Number items of Selection

        >>> selection = Selection(OneElement)
        >>> len(selection)
        1
        """
        return len(self.element_ids)

    def __repr__(self):
        """ Adds data to Base __repr__ to add selection count"""
        return super(Selection, self).__repr__(len(self))
    #
    #
    # def _pick_obj(self, obj_type, pick_message, multiple=False, world=False):
    #     PICK_MAP = {multiple: }
    #     try:
    #         # logger.debug('Picking elements: {} '
    #         #              'pick_message: {} '
    #         #              'multiple: {} '
    #         #              'world: {}'.format(obj_type, pick_message,
    #         #                                 multiple, world))
    #         if multiple:
    #             self._refs = list(uidoc.Selection.PickObjects(obj_type,
    #                                                           pick_message))
    #         else:
    #             self._refs = []
    #             self._refs.append(uidoc.Selection.PickObject(obj_type,
    #                                                          pick_message))
    #
    #         if not self._refs:
    #             logger.debug('Nothing picked by user...Returning None')
    #             return None
    #
    #         logger.debug('Picked elements are: {}'.format(self._refs))
    #
    #         if obj_type == ObjectType.Element:
    #             return_values = [doc.GetElement(ref) for ref in self._refs]
    #         elif obj_type == ObjectType.PointOnElement:
    #             if world:
    #                 return_values = [ref.GlobalPoint for ref in self._refs]
    #             else:
    #                 return_values = [ref.UVPoint for ref in self._refs]
    #         else:
    #             return_values = \
    #                 [doc.GetElement(ref).GetGeometryObjectFromReference(ref)
    #                  for ref in self._refs]
    #
    #         logger.debug('Processed return elements are: {}'
    #                      .format(return_values))
    #
    #         if type(return_values) is list:
    #             if len(return_values) > 1:
    #                 return return_values
    #             elif len(return_values) == 1:
    #                 return return_values[0]
    #         else:
    #             logger.error('Error processing picked elements. '
    #                          'return_values should be a list.')
    #     except:
    #         return None
    #
    #
    # def pick_element(self, message=''):
    #     return self._pick_obj(ObjectType.Element, message)
    #
    # def pick_elementpoint(self, message='', world=False):
    #     return self._pick_obj(ObjectType.PointOnElement, message, world=world)
    #
    # def pick_edge(self, message=''):
    #     return self._pick_obj(ObjectType.Edge, message)
    #
    # def pick_face(self, message=''):
    #     return self._pick_obj(ObjectType.Face, message)
    #
    # def pick_linked(self, message=''):
    #     return self._pick_obj(ObjectType.LinkedElement, message)
    #
    # def pick_elements(self, message=''):
    #     return self._pick_obj(ObjectType.Element, message, multiple=True)
    #
    # def pick_elementpoints(self, message='', world=False):
    #     return self._pick_obj(ObjectType.PointOnElement, message, multiple=True, world=world)
    #
    # def pick_edges(self, message=''):
    #     return self._pick_obj(ObjectType.Edge, message, multiple=True)
    #
    # def pick_faces(self, message=''):
    #     return self._pick_obj(ObjectType.Face, message, multiple=True)
    #
    # def pick_linkeds(self, message=''):
    #     return self._pick_obj(ObjectType.LinkedElement, message, multiple=True)
    #
    # # @staticmethod
    # # def pick_point(message=''):
    # #     try:
    # #         return uidoc.Selection.PickPoint(pick_message)
    # #     except:
    # #         return None
    #
    # @property
    # def references(self):
    #     return self._refs
