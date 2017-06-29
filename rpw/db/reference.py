"""
Reference Wrappers

"""

import rpw
from rpw import revit, DB
from rpw.db.element import Element
from rpw.db.xyz import XYZ
from rpw.utils.logger import logger
# from rpw.db.builtins import BipEnum


class Reference(Element):
    """
    `DB.Reference` Wrapper
    Inherits from :any:`Element`

    >>>

    Attribute:
        _revit_object (DB.Reference): Wrapped ``DB.Reference``
    """

    _revit_object_class = DB.Reference
    # _revit_object_category = DB.BuiltInCategory.OST_Rooms
    # _collector_params = {'of_category': _revit_object_category,
                        #  'is_not_type': True}

    def __init__(self, reference, doc=revit.doc):
        super(Reference, self).__init__(reference)
        self.doc = doc

    def __repr__(self):
        return super(Reference, self).__repr__(data={'id': self.id})

    @property
    def as_global_pt(self):
        pt = self._revit_object.GlobalPoint
        if pt:
            return XYZ(pt)

    @property
    def as_uv_pt(self):
        pt = self._revit_object.UVPoint
        if pt:
            #TODO XYZ needs to handle XYZ
            return pt
            # return XYZ(pt)

    @property
    def id(self):
        return self._revit_object.ElementId

    def get_element(self):
        return self.doc.GetElement(self.id)

    def get_geometry(self):
        ref = self._revit_object
        return self.doc.GetElement(ref).GetGeometryObjectFromReference(ref)
