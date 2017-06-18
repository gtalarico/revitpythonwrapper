import sys
import imp

class MockObject(object):

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', None)

    def __getattr__(self, *args, **kwargs):
        return MockObject(*args, **kwargs)

    def __iter__(self):
        yield iter(self)

    def AddReference(self, *args):
        logger.info("Mock.clr.AddReference('{}')".format(args[0]))

    def __call__(self, *args, **kwargs):
        return MockObject(*args, **kwargs)

class DotNetMockImporter(object):
    # https://github.com/gtalarico/revitpythonwrapper/issues/3
    # http://dangerontheranger.blogspot.com/2012/07/how-to-use-sysmetapath-with-python.html
    # http://blog.dowski.com/2008/07/31/customizing-the-python-import-system/

    # Using Explicit Module Names to avoid swallowing ImportErrors
    dotnet_modules = ['clr',
                      'Autodesk',
                      'RevitServices',
                      'IronPython',
                      'System',
                      ]

    def find_module(self, fullname, path=None):
        """
        This method is called by Python if this class
        is on sys.path. fullname is the fully-qualified
        name of the module to look for, and path is either
        __path__ (for submodules and subpackages) or None (for
        a top-level module/package).

        Note that this method will be called every time an import
        statement is detected (or __import__ is called), before
        Python's built-in package/module-finding code kicks in.
        Also note that if this method is called via pkgutil, it is possible
        that path will not be passed as an argument, hence the default value.
        Thanks to Damien Ayers for pointing this out!"""
        logger.debug('Loading : {}'.format(fullname))
        for module in self.dotnet_modules:
            if fullname.startswith(module):
                return self

        # If we don't provide the requested module, return None, as per
        # PEP #302.
        return None

    def load_module(self, fullname):
        """This method is called by Python if CustomImporter.find_module
           does not return None. fullname is the fully-qualified name
           of the module/package that was requested."""
        if fullname in sys.modules:
            return sys.modules[fullname]
        else:
            logger.info('Importing Mock Module: {}'.format(fullname))
            # mod = imp.new_module(fullname)
            # mod.__loader__ = self
            # mod.__file__ = fullname
            # mod.__path__ = [fullname]
            # return mod
            sys.modules[fullname] = MockObject(name=fullname)
            return MockObject(name=fullname)

from rpw.utils.logger import logger
# Attempt to Import clr
try:
    import clr
# Running Sphinx. Import MockImporter
except ImportError:
    logger.warning('Error Importing CLR. Loading Mock Importer')
    sys.meta_path.append(DotNetMockImporter())
    import clr

import clr
clr.AddReference('System')
clr.AddReference('System.Collections')

from System import Enum
from System.Collections.Generic import List
from System.Diagnostics import Process
