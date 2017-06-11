from rpw import DB
from rpw.base import BaseObjectWrapper


class XYZ(BaseObjectWrapper):
    """
    `DB.XYZ` Wrapper

    Allows setting of properties

    >>> some_point = XYZ(0,0,0)
    >>> pt = rpw.Point(some_point)
    >>> pt.as_tuple
    (0,0,0)
    >>> pt.x = 10
    <RPW_Point: 0,0,10>
    >>> pt.at_z(5)
    <RPW_Point: 0,0,5>

    Attributes:
        _revit_object (DB.XYZ): Wrapped ``DB.XYZ``
    """

    _revit_object_class = DB.XYZ

    def __init__(self, *xyz_or_tuple):
        """
        Args:
            instance (``DB.XYZ``): Instance of XYZ to be wrapped
        """
        if len(xyz_or_tuple) == 3:
            xyz = DB.XYZ(*xyz_or_tuple)
        elif len(xyz_or_tuple) == 2:
            xyz = DB.XYZ(xyz_or_tuple[0], xyz_or_tuple[1], 0)
        elif len(xyz_or_tuple) == 1 and isinstance(xyz_or_tuple[0], tuple):
            # Assumes one arg, tuple
            xyz = DB.XYZ(*xyz_or_tuple[0])
        else:
            # Assumes one arg, DB.XYZ
            xyz = xyz_or_tuple[0]
        super(XYZ, self).__init__(xyz)

    @property
    def x(self):
        """X Value"""
        return self._revit_object.X

    @property
    def y(self):
        """Y Value"""
        return self._revit_object.Y

    @property
    def z(self):
        """Z Value"""
        return self._revit_object.Z

    @x.setter
    def x(self, value):
        self._revit_object = DB.XYZ(value, self.y, self.z)

    @y.setter
    def y(self, value):
        self._revit_object = DB.XYZ(self.x, value, self.z)

    @z.setter
    def z(self, value):
        self._revit_object = DB.XYZ(self.x, self.y, value)

    def at_z(self, z):
        """ Returns a new point at the passed Z value

        Args:
            z(float): Elevation of new Points

        Returns:
            (:any:`Point`): New Points
        """
        return XYZ(self.x, self.y, z)

    @property
    def as_tuple(self):
        """
        Tuple representing the xyz coordinate of the Point

        Returns:
            (tuple): tuple float of XYZ values

        """
        return (self.x, self.y, self.z)

    def __repr__(self):
        return super(XYZ, self).__repr__(data=self.as_tuple,
                                         to_string='Autodesk.Revit.DB.XYZ')
