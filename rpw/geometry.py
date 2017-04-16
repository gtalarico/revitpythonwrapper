
import rpw
from rpw import doc, DB
from rpw.element import Element
from rpw.base import BaseObject

class Point(Element):
    """
    `DB.XYZ` Wrapper


    >>> some_point = XYZ(0,0,0)
    >>> pt = rpw.Point(some_point)
    >>> pt.as_tuple
    (0,0,0)
    >>> pt.at_z(5)
    <RPW_Point: 0,0,5>

    Attribute:
        _revit_object (DB.XYZ): Wrapped ``DB.XYZ``
    """
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
        super(Point, self).__init__(xyz, enforce_type=DB.XYZ)

    @property
    def x(self):
        return self._revit_object.X

    @property
    def y(self):
        return self._revit_object.Y

    @property
    def z(self):
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
        """
        Returns:
            (DB.XYZ): a XYZ point with the assigned z value.

        Args:
            z (float): Z Elevation
        """
        return Point(self.x, self.y, z)

    @property
    def as_tuple(self):
        """
        Returns:
            (tuple): tuple float of XYZ values
        """
        return (self.x, self.y, self.z)

    def __repr__(self):
        return super(Point, self).__repr__(data=self.as_tuple)



class PointCollection(BaseObject):
    """ A Collection of Point

        points = [p1,p2,p3,p4, ...]
        point_collection = PointCollection(*points)
            or
            point_collection = PointCollection(pt1, pt2, pt)
            or
            point_collection = PointCollection() - then

        Attributes:
            point_collection.average
            point_collection.min
            point_collection.max
    """
    def __init__(self, points=None):
        self.points = points if points is not None else []

    def __iter__(self):
        for point in self.points:
            yield point

    @property
    def average(self):
        """ Returns PointElement representing average of point collection.

        >>> points = [XYZ(0,0,0), XYZ(4,4,2)]
        >>> points.average
        (2,2,1)

        """
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        z_values = [point.z for point in self.points]
        x_avg = sum(x_values) / len(x_values)
        y_avg = sum(y_values) / len(y_values)
        z_avg = sum(z_values) / len(z_values)

        return Point(x_avg, y_avg, z_avg)

    @property
    def max(self):
        """ Returns PointElement representing MAXIMUM of point collection.

        >>> points = [(0,0,5), (2,2,2)]
        >>> points.max
        (2,2,5)

        """
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        z_values = [point.z for point in self.points]
        x_max = max(x_values)
        y_max = max(y_values)
        z_max = max(z_values)
        return Point(x_max, y_max, z_max)

    @property
    def min(self):
        """ Returns PointElement representing MINIMUM of point collection.
        PointElement objects must support X,Y,Z attributes.
        Example:
        points = [(0,0,5), (2,2,2)]
        points.min = (0,0,2)
        """
        x_values = [point.x for point in self.points]
        y_values = [point.y for point in self.points]
        z_values = [point.z for point in self.points]
        x_min = min(x_values)
        y_min = min(y_values)
        z_min = min(z_values)
        return Point(x_min, y_min, z_min)

    def sorted_by(self, x_y_z):
        sorted_points = self.points[:]
        sorted_points.sort(key=lambda p: getattr(p, x_y_z))
        return sorted_points

    def __len__(self):
        return len(self.points)

    def __repr__(self):
        return super(PointCollection, self).__repr__(data=len(self))


# class BoundingBox(object):
#     """ BoundingBoxElement receives a Revit Object for access to properties.
#     Usage:
#     bbox = BoundingBoxElement(element)
#     bbox.element: element
#     Properties:
#     bbox.min: min coordinate of bounding box
#     bbox.max: min coordinate of bounding box
#     bbox.average: min coordinate of bounding box
#     """
#
#     def __init__(self, element):
#         self.element = element
#         self.bbox = element.get_BoundingBox(doc.ActiveView)
#
#     @property
#     def min(self):
#         x, y, z = self.bbox.Min.X, self.bbox.Min.Y, self.bbox.Min.Z
#         return PointElement(x, y, z)
#
#     @property
#     def max(self):
#         x, y, z = self.bbox.Max.X, self.bbox.Max.Y, self.bbox.Max.Z
#         return PointElement(x, y, z)
#
#     @property
#     def average(self):
#         return PointCollection(self.min, self.max).average
#
#     def __repr__(self):
#         return '<BB: MIN{} MAX={} CENTER={}>'.format(self.min, self.max,
#                                                      self.center)
#
#     def __str__(self):
#         return repr(self)
#
# class Curve():
#     pass
