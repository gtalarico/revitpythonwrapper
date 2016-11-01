class Base(object):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return '<X:{}>'.format(self._name)

    @classmethod
    def __repr__(cls):
        return '<BASE>'


class TestClass(Base):

    def __new__(self, name):
        if name is None:
            return None
        return self

    def __init__(self, name):
        self.__name = name

    def name(self):
        pass
        return self._name
        # return self.__name


t = TestClass('Gui')
print(t)
# Access Hidden Variable
# print(t._TestClass__name)
# print(t.name())
# t.name()
