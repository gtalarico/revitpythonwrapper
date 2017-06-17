"""
`uidoc.Selection` Wrapper
"""

from rpw.revit import revit, DB, UI
from rpw.utils.dotnet import List
from rpw.base import BaseObjectWrapper
from rpw.exceptions import RPW_TypeError
from rpw.utils.logger import logger
from rpw.utils.coerce import to_element_ids
from rpw.db.collections_ import ElementSet

doc, uidoc = revit.doc, revit.uidoc


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
        uidoc.Selection.SetElementIds(List[DB.ElementId](self.element_ids))

    def clear(self):
        """ Clears Selection

        >>> selection = Selection()
        >>> selection.clear()

        Returns:
            None
        """
        ElementSet.clear(self)
        uidoc.Selection.SetElementIds(List[DB.ElementId]())

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
        return bool(len(self))

    def __repr__(self):
        """ Adds data to Base __repr__ to add selection count"""
        return super(Selection, self).__repr__(data={'count': len(self)})


class Pick():

    @staticmethod
    def _pick_obj(obj_type, msg='', multiple=False, world=False):
        # PICK_MAP = {multiple: }
        # try:
            # logger.debug('Picking elements: {} '
            #              'pick_message: {} '
            #              'multiple: {} '
            #              'world: {}'.format(obj_type, pick_message,
            #                                 multiple, world))
            # if multiple:
            #     self._refs = list(uidoc.Selection.PickObjects(obj_type,
            #                                                   msg))
            # else:
            #     self._refs = []
            selected = uidoc.Selection.PickObject(obj_type, msg)

            # if not self._refs:
            #     logger.debug('Nothing picked by user...Returning None')
            #     return None
            #
            # logger.debug('Picked elements are: {}'.format(self._refs))
            #
            # if obj_type == UI.Selection.ObjectType.Element:
            #     return_values = [doc.GetElement(ref) for ref in self._refs]
            # elif obj_type == UI.Selection.ObjectType.PointOnElement:
            #     if world:
            #         return_values = [ref.GlobalPoint for ref in self._refs]
            #     else:
            #         return_values = [ref.UVPoint for ref in self._refs]
            # else:
            #     return_values = \
            #         [doc.GetElement(ref).GetGeometryObjectFromReference(ref)
            #          for ref in self._refs]
            #
            # logger.debug('Processed return elements are: {}'
            #              .format(return_values))
            #
            # if type(return_values) is list:
            #     if len(return_values) > 1:
            #         return return_values
            #     elif len(return_values) == 1:
            #         return return_values[0]
            # else:
            #     logger.error('Error processing picked elements. '
            #                  'return_values should be a list.')
        # except:
            # return None
    #
    #
    @staticmethod
    def element(msg=''):
        return Pick._pick_obj(UI.Selection.ObjectType.Element, msg=msg)

    @staticmethod
    def element_point(msg='', world=False):
        return Pick._pick_obj(UI.Selection.ObjectType.PointOnElement, msg=msg, world=world)

    @staticmethod
    def edge(msg=''):
        return Pick._pick_obj(UI.Selection.ObjectType.Edge, msg=msg)
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
