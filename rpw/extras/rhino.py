""" 
Rhino Importer 

Usage:
    >>> from rpw.extras.rhino import Rhino
"""
from rpw.utils.dotnet import clr
clr.AddReference('Rhino3dmIO')

import Rhino