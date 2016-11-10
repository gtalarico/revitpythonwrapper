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
        elif isinstance(element, DB.ElementId) \
             or isinstance(element, DB.ElementId.InvalidElementId):
             element_ids.append(element)

    return element_ids
