import sys
import unittest

import os
repos = os.getenv('REPOS')
path = os.path.join(repos, 'revitpythonwrapper')
sys.path.append(path)

from rpw import DB, UI, doc, uidoc
from rpw.wrappers import Element
from rpw.selection import Selection
from rpw.transaction import Transaction
from rpw.collector import Collector, ParameterFilter
from rpw.exceptions import RPW_ParameterNotFound, RPW_WrongStorageType
from rpw.logger import logger
from rpw.enumeration import BuiltInParameterEnum

from System.Collections.Generic import List

# logger.verbose(True)
logger.disable()


# sys.exit()
