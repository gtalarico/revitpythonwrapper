.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Using With Dynamo
==================

The Revit Python Wrapper can easily be used within dynamo.
Eventually I hope to deploy it as a Package for convenient install,
in the meantime, here is a quick way to get started:

    1. Clone the revitpythonwrapper `repo <https://github.com/gtalarico/revitpythonwrapper>`_.
    2. Insert the following line at the top of your python script:

        >>> import sys
        >>> sys.path.append('c:\Documents\path\to\repo\revitpythonwrapper')

    3. revitpythonwrapper is ready to use.

        >>> from rpw import doc, uidoc
        >>> from rpw.collector import Collector

.. note:: A Dynamo Package it's on it's way.
