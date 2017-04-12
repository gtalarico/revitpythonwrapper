
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
    def __init__(self, xyz_or_tuple, enforce_type=DB.XYZ):
        """
        Args:
            instance (``DB.XYZ``): Instance of XYZ to be wrapped
        """
        if isinstance(xyz_or_tuple, DB.XYZ):
            xyz = xyz_or_tuple
        elif isinstance(tuple):
            xyz = DB.XYZ(*xyz_or_tuple)
        super(Point, self).__init__(instance, enforce_type=enforce_type)

    @property
    def at_z(self, z):
        """
        Returns:
            (DB.XYZ): a XYZ point with the assigned z value.

        Args:
            z (float): Z Elevation
        """
        return DB.XYZ(self._revit_object.X, self._revit_object.Y, z)

    @property
    def as_tuple(self):
        """
        Returns:
            (tuple): tuple float of XYZ values
        """
        return (self._revit_object.X,
                self._revit_object.Y,
                self._revit_object.Z)

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
        x_values = [point.X for point in self.points]
        y_values = [point.Y for point in self.points]
        z_values = [point.Z for point in self.points]
        x_avg = sum(x_values) / len(x_values)
        y_avg = sum(y_values) / len(y_values)
        z_avg = sum(z_values) / len(z_values)

        return PointElement(x_avg, y_avg, z_avg)

    @property
    def max(self):
        """ Returns PointElement representing MAXIMUM of point collection.

        >>> points = [(0,0,5), (2,2,2)]
        >>> points.max
        (2,2,5)

        """
        x_values = [point.X for point in self.points]
        y_values = [point.Y for point in self.points]
        z_values = [point.Z for point in self.points]
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
        x_values = [point.X for point in self.points]
        y_values = [point.Y for point in self.points]
        z_values = [point.Z for point in self.points]
        x_min = min(x_values)
        y_min = min(y_values)
        z_min = min(z_values)
        return PointElement(x_min, y_min, z_min)

    def sort_points(self, align_axis):
        sorted_points = self.points
        sorted_points.sort(key=lambda p: getattr(p, align_axis))
        self.points = sorted_points

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
