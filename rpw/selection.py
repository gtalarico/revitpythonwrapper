"""
`uidoc.Selection` Wrapper
"""

from rpw import doc, uidoc, DB
from rpw import List
from rpw.base import BaseObjectWrapper
from rpw.exceptions import RPW_TypeError
from rpw.utils.logger import logger


class Selection(BaseObjectWrapper):
    """
    >>> selection = Selection()
    >>> selection[0]
    FirstElement
    >>> selection.element_ids
    [ SomeElementId, SomeElementId, ...]
    >>> selection.elements
    [ SomeElement, SomeElement, ...]
    >>> len(selection)
    2

    Wrapped Element:
        self._revit_object = `Revit.UI.Selection`
    """

    def __init__(self, elements=None):
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
        if not isinstance(elements_or_ids, list):
            elements_or_ids = [elements_or_ids]
        if all([isinstance(e, DB.ElementId) for e in elements_or_ids]):
            element_ids = elements_or_ids
        elif all([isinstance(e, DB.Element) for e in elements_or_ids]):
            element_ids = [e.Id for e in elements_or_ids]
        elif all([isinstance(e, int) for e in elements_or_ids]):
            element_ids = [DB.ElementId(e) for e in elements_or_ids]
        else:
            raise RPW_TypeError(list, type(elements_or_ids[0]))

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
