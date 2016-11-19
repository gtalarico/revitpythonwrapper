from rpw import doc, DB, platform
from rpw.base import BaseObjectWrapper
from rpw.exceptions import RPW_Exception
from rpw.utils.logger import logger


class Transaction(BaseObjectWrapper):
    """
    Simplifies transactions by applying ``Transaction.Start()`` and
    ``Transaction.Commit()`` before and after the context.
    Automatically rolls back if exception is raised.

    >>> with Transaction('Move Wall'):
    >>>     wall.DoSomething()

    >>> with Transaction('Move Wall') as t:
    >>>     wall.DoSomething()
    >>>     assert t == DB.TransactionStatus.Started  # True
    >>> assert t == DB.TransactionStatus.Committed    # True

    Wrapped Element:
        self._revit_object = `Revit.DB.Transaction`

    """
    def __init__(self, name=None):
        if name is None:
            name = 'RPW Transaction'
        self.transaction = DB.Transaction(doc, name)

    def __enter__(self):
        self.transaction.Start()
        return self.transaction

    def __exit__(self, exception, exception_value, traceback):
        if exception:
            self.transaction.RollBack()
            logger.error('Error in Transactio Context: has rolled back.')
            logger.error('{}:{}'.format(exception, exception_value))
            raise exception(exception_value, '')
        else:
            try:
                self.transaction.Commit()
            except Exception as errmsg:
                self.transaction.RollBack()
                logger.error('Error in Transactio Commit: has rolled back.')
                logger.error('Error: {}'.format(errmsg))
                raise

    @staticmethod
    def ensure(name):
        """ Transaction Manager Decorator

        Decorate any function with ``@Transaction.ensure('Transaction Name')``
        and the funciton will run within a Transaction Context.

        Args:
            name (str): Name of the Transaction

        >>> @Transaction.ensure('Do Something')
        >>> def set_some_parameter(wall, value):
        >>>     wall.parameters['Comments'].value = value
        >>>
        >>> set_some_parameter(wall, value)
        """
        # TODO: Test in Dynamo
        from functools import wraps

        def wrap(f):
            @wraps(f)
            def wrapped_f(*args, **kwargs):
                with Transaction(name):
                    return_value = f(*args, **kwargs)
                return return_value
            return wrapped_f
        return wrap


class TransactionGroup(BaseObjectWrapper):
    """
    Similar to Transaction, but for ``DB.Transaction Group``

    >>> with TransacationGroup('Do Major Task'):
    >>>     with Transaction('Do Task'):
    >>>         # Do Stuff

    >>> with TransacationGroup('Do Major Task', assimilate=False):
    >>>     with Transaction('Do Task'):
    >>>         # Do Stuff


    """
    def __init__(self, name=None, assimilate=True):
        """
            Args:
                name (str): Name of the Transaction
                assimilate (bool): If assimilates is ``True``, transaction history is `squashed`.
        """
        if name is None:
            name = 'RPW Transaction Group'
        self.transaction_group = DB.TransactionGroup(doc, name)
        self.assimilate = assimilate

    def __enter__(self):
        self.transaction_group.Start()
        return self.transaction_group

    def __exit__(self, exception, exception_value, traceback):
        if exception:
            self.transaction_group.RollBack()
            logger.error('Error in TransactionGroup Context: has rolled back.')
            logger.error('{}:{}'.format(exception, exception_value))
        else:
            try:
                if self.assimilate:
                    self.transaction_group.Assimilate()
                else:
                    self.transaction_group.Commit()
            except Exception as errmsg:
                self.transaction_group.RollBack()
                logger.error('Error in TransactionGroup Commit: has rolled back.')
                logger.error('Error: {}'.format(errmsg))


class DynamoTransaction(object):

    # TODO: Use Dynamo Transaction when platform='dynamo'

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
