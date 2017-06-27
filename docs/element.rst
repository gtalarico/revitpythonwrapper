.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


==============================================
Element Wrappers
==============================================

Element
************

.. automodule:: rpw.db.element
    :undoc-members:

.. autoclass:: rpw.db.Element
    :members:
    :private-members:
    :special-members: __init__, __getattr__, __new__
    :show-inheritance:

Instance
************

.. autoclass:: rpw.db.FamilyInstance
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Symbol
************

.. autoclass:: rpw.db.FamilySymbol
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Family
************

.. autoclass:: rpw.db.Family
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Category
************

.. autoclass:: rpw.db.Category
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

    Unfortunately, this would not be the case with Wall Elements.
    A Wall Instance is actually a ``DB.Wall``; the `Family Type` of a wall
    is not a ``DB.FamilySymbol`` type, but a ``DB.WallType``;
    and instead of ``.Family``, walls use ``.Kind``.

    These wrappers create a more consistent navigation by allowing
    to retrieve the "symbol" and "family" of a wall using:
    `wall.symbol`, and `wall.family`

    >>> wall = rpw.db.WallInstance(SomeWallInstance)
    >>> wall.symbol
    <rpw: WallSymbol % DB.WallType | type:Wall 1>
    >>> wall.family
    <rpw: WallFamily % DB.WallKind | type:Basic 1>

.. autoclass:: rpw.db.WallInstance
    :show-inheritance:
    :special-members: __init__

.. autoclass:: rpw.db.WallSymbol
    :show-inheritance:
    :special-members: __init__

.. autoclass:: rpw.db.WallFamily
    :show-inheritance:
    :special-members: __init__

.. autoclass:: rpw.db.WallCategory
    :show-inheritance:
    :special-members: __init__

----------------------------------------------

Spatial Elements
****************

Room Wrapper

.. autoclass:: rpw.db.Room
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Area Wrapper

.. autoclass:: rpw.db.Area
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

Area Scheme Wrapper

.. autoclass:: rpw.db.AreaScheme
    :members:
    :private-members:
    :special-members: __init__
    :show-inheritance:

----------------------------------------------

Implementation
**************

.. literalinclude:: ../rpw/db/element.py
    :start-after: """  #
.. literalinclude:: ../rpw/db/wall.py
    :start-after: """  #
.. literalinclude:: ../rpw/db/spatial_element.py
    :start-after: """  #

.. disqus
