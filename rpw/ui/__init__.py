from rpw.utils.logger import logger

from rpw.ui.selection import Selection, Pick
from rpw.ui.console import Console

try:
    import forms
except ImportError as errmsg:
    logger.critical('Could Not load Forms dependencies')
    logger.warning(errmsg)
