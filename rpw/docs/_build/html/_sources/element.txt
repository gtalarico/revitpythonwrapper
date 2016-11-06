.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Element
==============================================

DB Namespace is the Largest namespace and contains over 10,000 members.

.. automodule:: rpw.element
    :members: Element
    :special-members: __init__, __getattr__
    :show-inheritance:


ParameterSet
************

.. autoclass:: rpw.parameter._ParameterSet
    :members:
    :special-members: __getattr__, __getitem__
    :show-inheritance:


Parameter
*********

.. autoclass:: rpw.parameter.Parameter
    :members:
    :special-members: __init__, __getattr__
    :show-inheritance:



Behind the Scenes
*****************

.. literalinclude:: ../element.py
