.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


==================
Transaction
==================

Wrappers to make Revit Transactions work with Python Context Manager.

.. automodule:: rpw.db.transaction
    :undoc-members:

.. autoclass:: rpw.db.Transaction
    :members:
    :special-members: __init__, __getattr__, __enter__, __exit__
    :private-members:
    :show-inheritance:

----------------------------------------------

Implementation
**************

.. literalinclude:: ../../../rpw/db/transaction.py

.. disqus
