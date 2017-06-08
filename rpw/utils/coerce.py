"""
Type Casting Utilities

"""


from rpw.revit import revit, DB
from rpw.utils.dotnet import List
from rpw.exceptions import RPW_TypeError


def to_element_ids(element_references):
    """ Coerces an element or list of elements into element ids. Elements remain unchanged.

    >>> from rpw.utils.coerce import to_element_ids
    >>> to_element_ids(DB.Element)
    [ DB.ElementId ]
    >>> to_element_ids(20001)
    [ DB.ElementId ]
    >>> to_element_ids([20001, 20003])
    [ DB.ElementId, DB.ElementId ]

    Args:
        elements (``DB.Element``): Iterable list (``list`` or ``set``) or single of ``Element``, ``int``.

    Returns:
        [``DB.ElementId``, ... ]: List of Element Ids.
    """
    if not isinstance(element_references, list) and not isinstance(element_references, set):
        element_references = [element_references]

    element_ids = []
    for reference in element_references:
        if isinstance(reference, DB.Element):
            element_ids.append(reference.Id)
        elif isinstance(reference, int):
            element_ids.append(DB.ElementId(reference))
        elif isinstance(reference, DB.ElementId):
            element_ids.append(reference)
        elif isinstance(reference, DB.ElementId.InvalidElementId):
            element_ids.append(reference)
        else:
            raise RpwTypeError('Element, ElementId, or int', type(item))

    return element_ids


def to_elements(element_references, doc=revit.doc):
    """ Coerces element reference (``int``, or ``ElementId``) into ``DB.Element``.
    Remains unchanged if it's already ``DB.Element``. Accepts single object or lists

    >>> from rpw.utils.coerce import to_elements
    >>> to_elements(DB.ElementId)
    [ DB.Element ]
    >>> to_elements(20001)
    [ DB.Element ]
    >>> to_elements([20001, 20003])
    [ DB.Element, DB.Element ]

    Args:
        element_references ([``DB.ElementId``, ``int``, ``DB.Element``]): Element Reference, single or list

    Returns:
        [``DB.Element``]: Elements
    """
    if not isinstance(element_references, list):
        element_references = [element_references]

    elements = []

    for reference in element_references:

        if isinstance(reference, DB.ElementId):
            element = doc.GetElement(reference)

        elif isinstance(reference, int):
            element = doc.GetElement(DB.ElementId(reference))

        elif isinstance(reference, DB.Element):
            element = reference

        else:
            raise RPW_TypeError('Element, ElementId, or int', type(element_reference))

        elements.append(element)

    return elements
