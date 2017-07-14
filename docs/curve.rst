.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


==================
Curve
==================

.. automodule:: rpw.db.curve

.. autoclass:: rpw.db.Curve
    :members:
    :special-members: __init__
    :private-members:
    :show-inheritance:

.. autoclass:: rpw.db.Line
    :members:
    :special-members: __init__
    :private-members:
    :show-inheritance:

    .. automethod:: create_detail

.. autoclass:: rpw.db.Ellipse
    :members:
    :special-members: __init__, create_detail
    :private-members:
    :show-inheritance:

    .. automethod:: create_detail

.. autoclass:: rpw.db.Circle
    :members:
    :special-members: __init__, create_detail
    :private-members:
    :show-inheritance:

    .. automethod:: create_detail

----------------------------------------------

Implementation
**************

.. literalinclude:: ../rpw/db/curve.py

.. disqus
