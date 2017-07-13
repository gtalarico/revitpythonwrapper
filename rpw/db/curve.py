""" Line Wrapper """

from math import pi as PI

from rpw import revit, DB
from rpw.base import BaseObjectWrapper
from rpw.db.element import Element
from rpw.db.xyz import XYZ


class Curve(BaseObjectWrapper):
    """ Curve Wrapper """

    def create_detail(self, view=None, doc=revit.doc):
        """
        Args:
            view (``DB.View``): Optional View. Default: ``uidoc.ActiveView``
            doc (``DB.Document``): Optional Document. Default: ``doc``
        """
        # TODO: Accept Detail Type (GraphicStyle)
        view = view or revit.active_view.unwrap()
        return doc.Create.NewDetailCurve(view, self._revit_object)

    def create_model(self, view=None, doc=revit.doc):
        # http://www.revitapidocs.com/2017.1/b880c4d7-9841-e44e-2a1c-36fefe274e2e.htm
        raise NotImplemented


class Line(Curve):

    """

    >>> line = rpw.db.Line([-10,0], [10,0])
    >>> line.create()

    """
    _revit_object_class = DB.Line

    def __init__(self, pt1, pt2):
        """
        Args:
            point1 (``point``): Point like object. See :any:`XYZ`
            point2 (``point``): Point like object. See :any:`XYZ`
        """
        pt1 = XYZ(pt1)
        pt2 = XYZ(pt2)
        line = DB.Line.CreateBound(pt1.unwrap(), pt2.unwrap())
        super(Line, self).__init__(line)


class Ellipse(Curve):

    """

    >>> ellipse = rpw.db.Ellipse([-10,0], [10,0])
    >>> ellipse.create()

    """
    _revit_object_class = DB.Ellipse

    def __init__(self, center,
                 x_radius, y_radius,
                 x_axis=None, y_axis=None,
                 start_param=0.0, end_param=2*PI):
        """
        Args:
            point1 (``point``): Point like object. See :any:`XYZ`
            point2 (``point``): Point like object. See :any:`XYZ`
        """
        center = XYZ(center).unwrap()
        x_axis = DB.XYZ(1,0,0) if x_axis is None else XYZ(x_axis).unwrap().Normalize()
        y_axis = DB.XYZ(0,1,0) if y_axis is None else XYZ(y_axis).unwrap().Normalize()

        start_param = start_param or 0.0
        end_param = start_param or PI*2

        ellipse = DB.Ellipse.Create(center, x_radius, y_radius, x_axis, y_axis, start_param, end_param)
        super(Ellipse, self).__init__(ellipse)


class DetailCurve():
    """ """

    def __init__():
        raise NotImplemented

    def get_curve():
        return self._revit_object.GeometryCurve
