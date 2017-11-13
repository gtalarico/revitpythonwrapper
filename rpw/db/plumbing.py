# coding: utf8

"""
Plumbing Wrapper
"""

from rpw.db import Element
from rpw import revit, DB


class FluidType(Element):
    """ Autodesk.Revit.DB.Plumbing.FluidType wrapper
    Inherits from rpw.db.Element
    >>> from rpw.db import FluidType

    Example to return a dictionary of fluids in use with system as key
    >>> FluidType.in_use_dict() # return format: {system.name:{'name':fluid.name, 'temperature':temperature}
    {'Hydronic Return': {'name': 'Water', 'temperature': 283.15000000000003}, ...}

    FluidType wrapper is collectible:
    >>> FluidType.collect()
    <rpw:Collector % FilteredElementCollector [count:19]>
    """
    _revit_object_class = DB.Plumbing.FluidType
    _collector_params = {'of_class': _revit_object_class, 'is_type': True}

    def __repr__(self, data=None):
        """ Adds data to Base __repr__ to add Parameter List Name """
        if not data:
            data = {}
        data['name'] = self.name
        return super(FluidType, self).__repr__(data=data)

    @staticmethod
    def in_use_dict(doc=revit.doc):
        """ Return a dictionary of fluids in use with system as key
        >>> FluidType.in_use_dict() # return format: {system.name:{'name':fluid.name, 'temperature':temperature}
        {'Hydronic Return': {'name': 'Water', 'temperature': 283.15000000000003}, ...}
        """
        result = {}
        for system in DB.FilteredElementCollector(doc).OfClass(DB.Plumbing.PipingSystemType):
            rpw_system = Element(system)
            rpw_fluid_type = Element.from_id(system.FluidType)
            result[rpw_system.name] = {'name': rpw_fluid_type.name, 'temperature': rpw_system.FluidTemperature}
        return result

    @property
    def fluid_temperatures(self):
        """ Return an iterable of all FluidTemperature in current FluidType as native GetFluidTemperatureSetIterator
        method is not very intuitive
        >>> fluid_type.fluid_temperatures
        <Autodesk.Revit.DB.Plumbing.FluidTemperatureSetIterator object at 0x00000000000002E9...
        >>> for fluid_temperature in fluid_type.fluid_temperatures:
        >>>     fluid_temperature
        <Autodesk.Revit.DB.Plumbing.FluidTemperature object at 0x00000000000002EC...
        <Autodesk.Revit.DB.Plumbing.FluidTemperature object at 0x00000000000002ED...
        ...
        """
        return self.GetFluidTemperatureSetIterator()

    @property
    def temperatures(self):
        """ Return (list) a sorted list of temperatures (double) in current FluidType
        [272.15000000000003, 277.59444444444449, 283.15000000000003, 288.70555555555563, ...]
        """
        return sorted([temp.Temperature for temp in self.fluid_temperatures])
