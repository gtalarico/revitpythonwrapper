=============================
Contribute
=============================

Overview
^^^^^^^^^^^

This projects welcomes contributions in the form of bug reports, suggestions, as well as Pull Requests.
If you have any questions about how to contribute just start an issue on the github repo and we will go from there.

Bug Reports
^^^^^^^^^^^^^^

Please be as specific as you can when creating an issue, and always try to answer the questions:
What are you trying to do?
What was the result?
What did you expect?

Also, try to pinpoint the cause or error by creating a small reproduceable snippet that isolates the issue
in question from other variables.

Suggestions
^^^^^^^^^^^^^^

There is no single correct way of writing these wrappers. Many of the design decisions were based
on maintainability/scalability, code aesthetics, and trying to create intuitive and friendly design patterns.

If you think something can be improved, or have ideas, please send them our way

Pull Requests
^^^^^^^^^^^^^^

Pull Requests are welcome and appreciated. If you are planning on sending PRs, please consider the following:

* Is the code style and patterns cohesive with the existing code base?
* Is the functionality being added belong to a general-purpose wrapper, or is it specific to a single project or used case? In other words, how likely is it to be used by others?

And Lastly, PRs should have the corresponding Tests and Documentation. This can sometimes be more work than writing the wrappers themselves, but they are essential.

Documentation
**************

1. Make sure you are familiar with the existing documentation.

2. Write doc strings on your classes and methods as you go. The docstrings in rpw use the Google Style Python Strings. The style is `documented here <https://google.github.io/styleguide/pyguide.html>`_, and you can find some great `examples here <http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>`_.

3. Duplicate one of the pages, and re-link the `autodoc` and `literal include` directives to point to your new class.

4. From a terminal on the `revitpythonlibrarywrapper.lib` folder, run the `build_docs.bat` file. This should rebuild the documentation and save it on the folder `docs/_build/html`.
The Docs will be build remotely on readthedocs.org once the code is pushed to github.

Unit Tests
**************

Testing python code in revit is a bit unconventional due to the need having to have Revit open.
Rpw uses standard unit tests packaged as a pyRevit extensions.
Take a look at some of the existing tests, and start by duplicate one of the existing tests.
Then add the the parent folder of `rpw.extension` to your pyRevit Paths and reload. You should see a new
tab with all the tests.

.. caution::
   Do not run any of the tests with other revit files open.
   The current tests require the `collector.rvt` for the tests to execute properly.
   This is left over from earlier tests and we intend it to fix it at some point.

Tests should be as self-contained as possible in the sense that they should create and destroy objects and
not be depend son a specific model state. The best approach is to setup your tests using standard API code, and then verify that the class returns the same response as the API by it self. And if any objects are created,
try to clean up and destroy them using the tearDown methods. A simple example of a test for a Collector test might be something like this:

   >>> from rpw import db, DB
   >>> # Tests are generally group into Test Case classes. This part is omitted from this example.
   >>> def test_collector_of_class(self):
   >>>   elements = DB.FilteredElementCollector(doc).OfClass(DB.View).ToElements()
   >>>   rv = db.Collector(of_class='View').elements
   >>>   # Test Return Value:
   >>>   self.assertEqual(len(elements), len(rv))
   >>>   self.assertEqual(elements[0].Id, rv[1].Id)
   >>>   self.assertIsInstance(rv[0], DB.View)

