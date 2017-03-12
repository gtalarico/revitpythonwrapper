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

Wall Element Tree Wrappers

.. Note::
    These classes inherit from the classes listed above, but make some adjustments
    to compensate for disimilarties in in Wall Families.

    To go from an FamilyInstance (placed instance) to a FamilySymbol (Family Type on User Interface)
    to a Family, one would might use ``instance.Symbol`` and ``symbol.Family``.

    Unfortunatelly, this would not be the case with Wall Elements.
    A Wall Instance is actually a ``DB.Wall``; the `Family Type` of a wall
    is not a ``DB.FamilySymbol`` type, but a ``DB.WallType``;
    and instead of ``.Family``, walls use ``.Kind``.

    These subclasses are used to
    `tweak` the primary classes so navigation across the element tree is more
    consistent.

    .. ::
        >>> wall = rpw.WallInstance(SomeWallInstance)
        >>> wall.symbol
        < RPW_WallType: Wall 1>
        >>> wall.family
        < RPW_WallKind: Basic Wall>

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

Room
************

Room Wrapper

.. autoclass:: rpw.element.Room
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

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
