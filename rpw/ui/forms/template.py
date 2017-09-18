""" Template Form """  #

from rpw.ui.forms.resources import *


class TemplateForm(Window):
    """
    Flex Form Usage

    >>> class YourForm(TemplateForm):
    >>>     layout = '<window> ... </window>'
    >>>     def __init__(self, *args, **kwargs):
    >>>     super(DataGrid, self).__init__(title, DataGrid.layout)

    """
    def __init__(self, xaml):
        """
        Args:
            components (``list``): List of Form Components.

        """
        self.ui = wpf.LoadComponent(self, StringReader(self.layout))

    def show(self):
        """
        Initializes Form. Returns ``True`` or ``False`` if form was exited.
        """
        return self.ShowDialog()

    def close(self):
        """ Exits Form. Returns ``True`` to ``show()`` method """
        self.DialogResult = True
        self.Close()


if __name__ == '__main__':
    """ TESTS """

    from rpw.ui.forms import DataGrid; f = DataGrid('Test'); f.show()

    form = TemplateForm('Title', components)
    form.show()

    print(form.values)
