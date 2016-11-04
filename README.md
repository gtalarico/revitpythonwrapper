Revit Python Wrapper!

The Idea is similar to what I did to the Ui components on that fork of pyrevit that I sent, and abstract it even more to make more reusable by other programs and scripts.

You have done that as well on some of your scripts.

The idea is to create a  python api interface (wrapper) to simplify interaction with the api, make it easier, more fun, and more pythonic.

Goals:
- Normalize revit version (handle calls base on revit version, similar to how python Six module does for python 2 and 3
- normalize pyrevit and dynamo document manager, so code can be reused (doc and ui doc are handled automatically)
- create a python friendly interface for common tasks, for example :

element.parameter['Height'] = 10
(finds parameter, opens transaction, coerce data type if needed, sets parameter, and commit)
element.parameters.builtins['WALL_LOCATION_LINE']

I have a nice prototype working. I put it on github when I get chance.
I get the feeling this will plug really nice with that idea of pyrevit standard library, but I also want to maintain it as separate project so dynamo users can import it an use it as well (bigger audiece=more maintainers, hopefully)  :)

I'm also using this as a chance to learn Sphinx, so the python wrapper api would have a fully documented interface.

It's a big project, but it will be fun. I'm learning a lot.
