# coding: utf8
"""
Plumbing Wrapper
"""
from rpw.base import BaseObjectWrapper
from rpw import revit, DB, doc


class FluidType(BaseObjectWrapper):
    """
    Allow you to treat fluids as dictionnary
    >>> # TODO: make an example
    """
    _revit_object_class = DB.Plumbing.FluidType

    def __init__(self, fluidtype):
        super(FluidType, self).__init__(fluidtype)

    # def __repr__(self):
    #     """ Adds data to Base __repr__ to add Parameter List Name """
    #     name = self.name
    #     return super(FluidType, self).__repr__(data={'name':name})

    @staticmethod
    def all(document=doc):
        return [FluidType(fluid) for fluid in DB.FilteredElementCollector(document).OfClass(DB.Plumbing.FluidType)]

    def all_name_dict(self, document=doc):
        return {fluidtype.name:fluidtype for fluidtype in self.all(document)}

    @property
    def name(self):
        return DB.Element.Name.GetValue(self._revit_object)

    @property
    def all_names(self):
        return [DB.Element.Name.GetValue(fluid) for fluid in self.all()]

    @property
    def fluid_dict(self):
        return {DB.Element.Name.GetValue(fluid):FluidType(fluid) for fluid in self.all()}

    @property
    def revit_temperatures(self):
        """
        :return: temperatures of fluid
        """
        return list(self.revit_fluid.GetFluidTemperatureSetIterator())

    @property
    def temperatures_dict(self):
        d = {}
        for temp in self.revit_fluid.GetFluidTemperatureSetIterator():
            d[temp.Temperature]=temp
        return d

    @property
    def viscosity_dict(self):
        d = {}
        for temp in self.revit_fluid.GetFluidTemperatureSetIterator():
            d[temp.Viscosity]=temp
        return d

    @property
    def density_dict(self):
        d = {}
        for temp in self.revit_fluid.GetFluidTemperatureSetIterator():
            d[temp.Density]=temp
        return d

