"""
Consolidate all imports and resources for other forms based classes to use.

"""

import sys

from abc import ABCMeta

from rpw import revit
from rpw.utils.dotnet import clr
from rpw.utils.logger import logger

if revit.host == 'Dynamo':
    sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Platforms\Net40')

# WPF/Form Imports
clr.AddReference("PresentationFramework")  # System.Windows: Controls, ?
clr.AddReference("WindowsBase")            # System.Windows.Input
clr.AddReference("System.Drawing")         # FontFamily

import System.Windows
from System.Windows import Window
from System.IO import StringReader

# Console
from System.Environment import Exit, NewLine
from System.Drawing import FontFamily
from System.Windows.Input import Key

# FlexForm Imports
from System.Windows import Controls, Window
from System.Windows import HorizontalAlignment, VerticalAlignment, Thickness

clr.AddReference('IronPython')
clr.AddReference('IronPython.Wpf')  # 2.7clr.AddReference('IronPython.Modules')
from IronPython.Modules import Wpf as wpf
