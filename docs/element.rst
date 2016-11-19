.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


==============================================
Element Wrappers
==============================================

Element
************

.. automodule:: rpw.element

.. autoclass:: rpw.element.Element
    :members:
    :private-members:
    :special-members: __init__, __getattr__
    :show-inheritance:

Instance
************

.. autoclass:: rpw.element.Instance
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Symbol
************

.. autoclass:: rpw.element.Symbol
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Family
************

.. autoclass:: rpw.element.Family
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Category
************

.. autoclass:: rpw.element.Category
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

----------------------------------------------

Walls
************

These classes are the same as above, but adjusted for Wall System Families.
They exist to handle the primary Element Tree classes when needed:
 (ie. Wall Types vs FamilySymbol, Family vs WallKind)

.. autoclass:: rpw.element.WallInstance
    :show-inheritance:
    :special-members: __init__

.. autoclass:: rpw.element.WallSymbol
    :show-inheritance:
    :special-members: __init__

.. autoclass:: rpw.element.WallFamily
    :show-inheritance:
    :special-members: __init__

.. autoclass:: rpw.element.WallCategory
    :show-inheritance:
    :special-members: __init__

----------------------------------------------

ParameterSet
************

.. autoclass:: rpw.parameter.ParameterSet
    :members:
    :special-members: __init__, __getitem__, __setitem__, __len__
    :show-inheritance:


Parameter
*********

.. autoclass:: rpw.parameter.Parameter
    :members:
    :special-members: __init__, __getattr__, __setitem__
    :show-inheritance:

----------------------------------------------

Implementation
**************

.. literalinclude:: ../rpw/element.py
.. literalinclude:: ../rpw/parameter.py
