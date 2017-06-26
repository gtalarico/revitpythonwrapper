# Revit Python Wrapper - Console Demo
import sys
sys.path.append(r'D:\Dropbox\Shared\dev\repos\revitpythonwrapper\revitpythonwrapper.lib')

import rpw
from rpw.db import Collector
from rpw.ui.forms import Console
from rpw.ui import Selection

walls = Collector(of_class='Wall', is_type=False)
for n, wall in enumerate(walls.elements):
    if n == 2:
        x = 'something'
        Console(context=locals())# << Breakpoint


OUT = walls.elements
