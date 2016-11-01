"""
Python Wrapper For the Revit API
Base wrappers.

"""

from rpw import doc, uidoc
from rpw.logger import logger


class BaseClass(object):
    """
    RPW Base Class
    """


class Element():
    """
    Revit Element Wrapper
    """
    # def __init___(self, baseclass):
    # self.__class__ = type(__class__.__name)


class Parameter(BaseWrapper):
    """
    Revit Parameter Wrapper
    """
    def __init__(self, parameter):
        pass


class FamilyInstance(BaseWrapper):
    """ Generic Family Instance Wrapper """
    # Get Type
    # Get Symbol
    # Get Elements
    # @transaction(name)
    def move(self, translation):
        pass


class FamilyType(BaseWrapper):
    """ Generic Family Instance Wrapper """
    # Get Type
    # Get Symbol
    # Get Elements
