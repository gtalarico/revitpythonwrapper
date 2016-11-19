from rpw import uidoc, doc, DB
from rpw import List
from rpw.exceptions import RPW_TypeError


def to_element_ids(elements):
    """ Coerces an element or list of elements into element ids. Elements remain unchanged.

    Args:
        elements (``DB.Element``): Iterable list (``list`` or ``set``) or single of ``Element``, ``int``.

    Returns:
        [``DB.ElementId``, ... ]: List of Element Ids.
    """
    if not isinstance(elements, list) and not isinstance(elements, set):
        elements = [elements]

    element_ids = []
    for element in elements:
        if isinstance(element, DB.Element):
            element_ids.append(element.Id)
        elif isinstance(element, int):
            element_ids.append(DB.ElementId(element))
        elif isinstance(element, DB.ElementId):
            element_ids.append(element)
        elif isinstance(element, DB.ElementId.InvalidElementId):
            element_ids.append(element)
        else:
            raise RPW_TypeError('Element, ElementId, or int', type(element_reference))

    return element_ids


def to_elements(element_references):
    """ Coerces element reference (``int``, or ``ElementId``) into ``DB.Element``.
    Remains unchanged if it's already ``DB.Element``. Accepts single object or lists

    Args:
        element_references ([``DB.ElementId``, ``int``, ``DB.Element``]): Element Reference, single or list

    Returns:
        [``DB.Element``]: Elements
    """
    if not isinstance(element_references, list):
        element_references = [element_references]

    elements = []

    for element_reference in element_references:

        if isinstance(element_reference, DB.ElementId):
            element = doc.GetElement(element_reference)

        elif isinstance(element_reference, int):
            element = doc.GetElement(DB.ElementId(element_reference))

        elif isinstance(element_reference, DB.Element):
            element = element_reference

        else:
            raise RPW_TypeError('Element, ElementId, or int', type(element_reference))

        elements.append(element)

    return elements
