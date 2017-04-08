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
    :undoc-members:

.. autoclass:: rpw.Element
    :members:
    :private-members:
    :special-members: __init__, __getattr__
    :show-inheritance:

Instance
************

.. autoclass:: rpw.Instance
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Symbol
************

.. autoclass:: rpw.Symbol
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Family
************

.. autoclass:: rpw.Family
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Category
************

.. autoclass:: rpw.Category
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

----------------------------------------------

Walls
************

Wall Element Tree Wrappers

.. Note::
    These classes inherit from the classes listed above, but make some adjustments
    to compensate for disimilarties in in Wall Families.

    When retrieving the FamilySymbol from an instance, and the  Family from a Symbol,
    one might uses ``instance.Symbol`` and ``symbol.Family``.

    Unfortunatelly, this would not be the case with Wall Elements.
    A Wall Instance is actually a ``DB.Wall``; the `Family Type` of a wall
    is not a ``DB.FamilySymbol`` type, but a ``DB.WallType``;
    and instead of ``.Family``, walls use ``.Kind``.

    These wrappers create a more consistent navigation by allowing
    to retrieve the "symbol" and "family" of a wall using:
    `wall.symbol`, and `wall.family`

    >>> wall = rpw.WallInstance(SomeWallInstance)
    >>> wall.symbol
    < RPW_WallType: Wall 1>
    >>> wall.family
    < RPW_WallKind: Basic Wall>

.. autoclass:: rpw.WallInstance
    :show-inheritance:
    :special-members: __init__

.. autoclass:: rpw.WallSymbol
    :show-inheritance:
    :special-members: __init__

.. autoclass:: rpw.WallFamily
    :show-inheritance:
    :special-members: __init__

.. autoclass:: rpw.WallCategory
    :show-inheritance:
    :special-members: __init__

----------------------------------------------

Room
************

Room Wrapper

.. autoclass:: rpw.Room
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

----------------------------------------------

Parameter and Parameter Set
***************************

ParameterSet
^^^^^^^^^^^^

.. Note::
    These are used internally by all Classes that inherit from ``rpw.Element``,
    but can be used on their own.


.. autoclass:: rpw.ParameterSet
    :members:
    :special-members: __init__, __getitem__, __setitem__, __len__
    :show-inheritance:


Parameter
^^^^^^^^^

.. autoclass:: rpw.parameter.Parameter
    :members:
    :special-members: __init__, __getattr__, __setitem__
    :show-inheritance:

----------------------------------------------

Implementation
**************

.. literalinclude:: ../rpw/element.py
.. literalinclude:: ../rpw/parameter.py
