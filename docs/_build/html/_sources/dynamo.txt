.. revitpythonwrapper documentation master file, created by
   sphinx-quickstart on Mon Oct 31 13:57:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Using With Dynamo
==================

The Revit Python Wrapper can easily be used within dynamo.
Eventually I hope to deploy it as a Package for convenient install,
in the meantime, here is a quick way to get started:

    1. Install RevitPythonWrapper Package
    2. Find the Package Directory, and open the Getting Started File
    3. revitpythonwrapper is ready to use.

        >>> from rpw import doc, uidoc
        >>> from rpw.collector import Collector

To Do:
    * Adjust Test Runner to run out-of-the-box
    * Improve Getting Started
