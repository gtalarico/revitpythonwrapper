import clr

# noinspection PyUnresolvedReferences
import System

clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
clr.AddReferenceByName('Rhino3dmIO')

from Rhino import *
