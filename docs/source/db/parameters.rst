.. automodule:: rpw.db.parameter

ParameterSet
************

.. Note::
    These are used internally by all Classes that inherit from ``rpw.db.element``,
    but can be used on their own.


.. autoclass:: rpw.db.ParameterSet
    :members:
    :special-members: __init__, __getitem__, __setitem__, __len__
    :show-inheritance:


Parameter
*********

.. autoclass:: rpw.db.Parameter
    :members:
    :special-members: __init__, __getattr__, __setitem__
    :show-inheritance:

----------------------------------------------

Implementation
**************

.. literalinclude:: ../../../rpw/db/parameter.py
