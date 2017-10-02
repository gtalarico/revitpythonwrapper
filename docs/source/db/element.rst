.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


==============================================
Element
==============================================

Element Wrapper
***************

.. automodule:: rpw.db.element
    :undoc-members:

.. autoclass:: rpw.db.Element
    :members:
    :private-members:
    :special-members: __init__, __getattr__, __new__
    :show-inheritance:

Parameters
***************

.. toctree::
   :maxdepth: 2

   parameters


Element-based Wrappers
**********************

.. toctree::
   :maxdepth: 2

   assembly
   family
   pattern
   spatial_element
   view
   wall


Implementation
**************

.. literalinclude:: ../../../rpw/db/element.py
    :start-after: """  #

.. disqus
