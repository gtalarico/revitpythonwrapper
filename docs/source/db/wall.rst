.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=================
Walls
=================

Wall Wrappers
*************

.. Note::
    These classes inherit from the classes listed above, but make some adjustments
    to compensate for dissimilarities in in Wall Families.

    When retrieving the FamilySymbol from an instance, and the  Family from a Symbol,
    one might uses ``instance.Symbol`` and ``symbol.Family``.

    Unfortunately, this would not be the case with Wall Elements.
    A Wall Instance is actually a ``DB.Wall``; the `Family Type` of a wall
    is not a ``DB.FamilySymbol`` type, but a ``DB.WallType``;
    and instead of ``.Family``, walls use ``.Kind``.

    These wrappers create a more consistent navigation by allowing
    to retrieve the "symbol" and "family" of a wall using:
    `wall.symbol`, and `wall.family`

    >>> wall = rpw.db.Wall(SomeWallInstance)
    >>> wall.symbol
    <rpw: WallType % DB.WallType | type:Wall 1>
    >>> wall.family
    <rpw: WallKind % DB.WallKind | type:Basic 1>

.. autoclass:: rpw.db.Wall
    :members:
    :show-inheritance:
    :special-members: __init__
    :inherited-members:
    :exclude-members: from_id, from_int, from_list

.. autoclass:: rpw.db.WallType
    :members:
    :show-inheritance:
    :special-members: __init__
    :inherited-members:
    :exclude-members: from_id, from_int, from_list

.. autoclass:: rpw.db.WallKind
    :members:
    :show-inheritance:
    :special-members: __init__
    :inherited-members:
    :exclude-members: from_id, from_int, from_list

.. autoclass:: rpw.db.WallCategory
    :members:
    :show-inheritance:
    :special-members: __init__
    :inherited-members:
    :exclude-members: from_id, from_int, from_list


----------------------------------------------

Implementation
**************

.. literalinclude:: ../../../rpw/db/wall.py
    :start-after: """  #

.. disqus
