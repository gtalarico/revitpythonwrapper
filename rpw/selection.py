from rpw import doc, uidoc
from rpw.wrappers import BaseObjectWrapper
from rpw.logger import logger

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

    >>> selection.RevitProperty
    >>> selection.RevitMethod()

    self._element = Revit.UI
    """

    def __init__(self):
        """ Stores uidoc.Selection in element so attributes can be accessed"""
        super(Selection, self).__init__(uidoc.Selection)

    @property
    def element_ids(self):
        """
        List of elemend ids

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

    def __getitem__(self, index):
        """
        Retrieves element using index. If Index is out range,
        None is returned

        Args:
            index(int): Integer representing list index.

        returns: Element, None
        Usage:
        selection[0]
        """
        return self.elements[index]

    def __len__(self):
        """ Number items of Selection """
        return len(self.element_ids)

    def __repr__(self):
        """ Adds data to Base __repr__ to add selection count"""
        return super(Selection, self).__repr__(len(self))
