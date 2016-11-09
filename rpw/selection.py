from rpw import doc, uidoc, DB
from rpw import List
from rpw.base import BaseObjectWrapper
from rpw.logger import logger
from rpw.exceptions import RPW_TypeError


class Selection(BaseObjectWrapper):
    """
    Revit uidoc.Selection Wrapper
    Makes easier to manipulate Active Selection.

    Usage:
        >>> selection = Selection()
        >>> selection[0]
        >>> selection.element_ids
        >>> selection.elements
        >>> len(selection)

    Wrapped Element:
        self._revit_object = `Revit.UI.Selection`
    """

    def __init__(self, elements=None):
        """
        Initializes Selection.

        Args:
            (DB.Element, DB.ElementID): Elements or ElementIds

        >>> selection = Selection(SomeElement)
        >>> selection = Selection(SomeElementId)
        >>> selection = Selection([Element, Element, Element, ...])

        """
        super(Selection, self).__init__(uidoc.Selection)
        if elements:
            self.add(elements)

    def add(self, elements_or_ids):
        """ Adds elements to selection. Takes elements or element ids

        Args:
            (DB.Element, DB.ElementID): Elements or ElementIds

        >>> selection = Selection()
        >>> selection.add(SomeElement)
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
        all_ids = current_selection.append(element_ids)
        uidoc.Selection.SetElementIds(List[DB.ElementId](element_ids))

    @property
    def element_ids(self):
        """
        List of `ElemendId` objects

        Returns:
            [DB.ElementId]: List of ElementIds Objects """
        return [eid for eid in self._revit_object.GetElementIds()]

    @property
    def elements(self):
        """
        List of Elements.

        Returns:
            [DB.Element]: List of Elements """
        return [doc.GetElement(eid) for eid in self.element_ids]

    def clear(self):
        """ Clears Selection

        Returns:
            None
        """
        uidoc.Selection.SetElementIds(List[DB.ElementId]())

    def __getitem__(self, index):
        """
        Retrieves element using index.
        If Index is out range, `None` is returned

        Args:
            int: Integer representing list index.

        Returns:
            `DB.Element`, `None`

        >>> selection[0]
        < Revit.DB.Element >
        """
        return self.elements[index]


    def __bool__(self):
        return bool(self.elements)

    def __len__(self):
        """ Number items of Selection """
        return len(self.element_ids)

    def __repr__(self):
        """ Adds data to Base __repr__ to add selection count"""
        return super(Selection, self).__repr__(len(self))
