from rpw import doc, DB
from rpw.logger import logger
from rpw.base import BaseObjectWrapper


class Transaction(object):
    """ Transaction Context Manager.

    Simplifies transactions by applying ``Transaction.Start()`` and
    ``Transaction.Commit`` before and after the context.
    Automatically rolls back if exception is raised.

    Usage:
        >>> with Transaction('Move Wall'):
        >>>     wall.move()

    Wrapped Element:
        self._revit_object = `Revit.DB.Transaction`

    """
    def __init__(self, name):
        self.transaction = DB.Transaction(doc, name)

    def __enter__(self):
        self.transaction.Start()

    def __exit__(self, exception, exception_value, traceback):
        if exception:
            self.transaction.RollBack()
        else:
            try:
                self.transaction.Commit()
            except:
                self.transaction.RollBack()
                raise
