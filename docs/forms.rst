.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


==================
Forms
==================

Forms are provided to facilitate user input.

.. image:: _static/forms/select-from-list.png

.. autoclass:: rpw.forms.SelectFromList
    :members:
    :special-members: __init__

.. image:: _static/forms/text-input.png

.. autoclass:: rpw.forms.TextInput
    :members:
    :special-members: __init__

----------------------------------------------

Implementation
**************

.. literalinclude:: ../rpw/forms/forms.py
    :start-after: sphinx_compat
