from rpw import doc, DB, platform
from rpw.logger import logger
from rpw.base import BaseObjectWrapper
from rpw.exceptions import RPW_Exception


class Transaction(object):
    """ Transaction Context Manager.

    Simplifies transactions by applying ``Transaction.Start()`` and
    ``Transaction.Commit()`` before and after the context.
    Automatically rolls back if exception is raised.

    Usage:
        >>> with Transaction('Move Wall'):
        >>>     wall.DoSomething()

    Wrapped Element:
        self._revit_object = `Revit.DB.Transaction`

    """
    def __init__(self, name=None):
        if name is None:
            name = 'RPW Transaction'
        self.transaction = DB.Transaction(doc, name)

    def __enter__(self):
        self.transaction.Start()

    def __exit__(self, exception, exception_value, traceback):
        if exception:
            self.transaction.RollBack()
            logger.warning('Transaction has rolled back.')
        else:
            try:
                self.transaction.Commit()
            except:
                self.transaction.RollBack()

    @staticmethod
    def ensure(transaction_name):
        """ Transaction Manager Decorator

        Decorate any function with ``@Transaction.ensure('Transaction Name')``
        and the funciton will run withing a Transaction Context.

        Args:
            transaction_name (str): Name of the Transaction

        Usage:

            >>> @Transaction.ensure('Do Something')
            >>> def set_some_parameter(wall, value):
            >>>     wall.parameters['Comments'].value = value
            >>>
            >>> set_some_parameter(wall, value)
        """
        from functools import wraps  # Move import up once Tested In Dynamo

        def wrap(f):
            @wraps(f)
            def wrapped_f(*args, **kwargs):
                with Transaction(transaction_name):
                    return_value = f(*args, **kwargs)
                return return_value
            return wrapped_f
        return wrap



class DynamoTransaction(object):
    def __init__(self, name):
        raise NotImplemented
    #     from rpw import TransactionManager
    #     self.transaction = TransactionManager.Instance
    #
    # def __enter__(self):
    #     self.transaction.EnsureInTransaction(doc)
    #
    # def __exit__(self, exception, exception_value, traceback):
    #     if exception:
    #         pass # self.transaction.RollBack()
    #     else:
    #         try:
    #             self.transaction.TransactionTaskDone()
    #         except:
    #             try:
    #                 self.transaction.ForceCloseTransaction()
    #             except:
    #                 raise RPW_Exception('Failed to complete transaction')
