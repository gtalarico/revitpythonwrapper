from rpw import uidoc, doc, DB
from rpw import List


def elements_to_element_ids(elements):
    """ Coerces list of elements into element ids.
    Args:
        elements ([DB.Element]) = Iterable list of DB.Elements
    """
    element_ids = []
    for element in elements:
        if isinstance(element, DB.Element):
            element_ids.append(element.Id)
        elif (isinstance(element, DB.ElementId) or
              isinstance(element, DB.ElementId.InvalidElementId)):
            element_ids.append(element)

    return element_ids


def element_reference_to_element_ids(element_reference):
    """ Coerces element reference (``int``, or ``ElementId``) into ``DB.Element``.
    Remains unchanged if it's already ``DB.Element``.
    """
    if isinstance(element_reference, DB.ElementId):
        element = doc.GetElement(element_reference)

    if isinstance(element_reference, DB.Element):
        element = element_reference

    if isinstance(element_reference, int):
        element = doc.GetElement(DB.ElementId(element_reference))

    if not isinstance(element, DB.Element):
        raise RPW_TypeError('Element, ElementId, or int', type(element_reference))

    return element
