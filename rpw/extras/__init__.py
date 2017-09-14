import sys
import os.path as op

sys.path.append(op.dirname(__file__))

import clr

# noinspection PyUnresolvedReferences
import System


clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
clr.AddReferenceByName('Rhino3dmIO')
from Rhino import *
rhg = Geometry
