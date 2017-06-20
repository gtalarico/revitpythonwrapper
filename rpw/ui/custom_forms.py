# This is only so forms.py to be executed on console for easier testing and dev
# `ipy.exe forms.py` and ipy -X:FullFrames console.py
from itertools import count

try:
    from forms import *
except ImportError:
    from rpw.ui.forms import *
# logger.verbose(True)

V_SPACING = 5


class CustomForm(Window):
    """
    WPF Custom Form.

    """

    LAYOUT = """
            <Window
                xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
                xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                xmlns:local="clr-namespace:WpfApplication1"
                mc:Ignorable="d" Height="140.139" Width="325" ResizeMode="NoResize"
                Title="" WindowStartupLocation="CenterScreen" Topmost="True" SizeToContent="WidthAndHeight">
                <Grid Margin="10,0,10,10">
                    {components}
                </Grid>
            </Window>
            """

    def __init__(self, title, components):
        components_string = ''.join([str(e) for e in components])
        layout = CustomForm.LAYOUT.format(components=components_string.strip())

        self.ui = wpf.LoadComponent(self, StringReader(layout))
        self.ui.Title = title

        # if description is not None:
        #     self.ui.selection_label.Content = description
        # self.ui.button_select.Click += self.select_click



    def select_click(self, sender, e):
        selected = self.ui.combo_data.SelectedItem
    #     if isinstance(self.options, dict):
    #         selected = self.options[selected]
    #
    #     self.selected = selected
    #     self.DialogResult = True
    #     self.Close()

    def show(self):
        return super(CustomForm, self).ShowDialog()


class ComponentAttribute():
    template = '{}="{}" '

    def __init__(self, attr_name, value):
        self.attr_name = attr_name
        self.value = value

    @property
    def uppercamel_name(self):
        """ Converts snake_case to SnakeCase """
        first, rest = self.attr_name.split('_')[0], self.attr_name.split('_')[1:]
        return first.title() + ''.join(word.capitalize() for word in rest)

    def __str__(self):
        """ Takes name and value, returns Name="value" """
        return self.template.format(self.uppercamel_name, self.value)


class Component():
    _index = count(0)
    template = """<{component} x:{attributes}/>"""

    allowed_attributes = ['name', 'width', 'height', 'margin',
                          'content',
                          'horizontal_alignment', 'vertical_alignment',
                          ]

    def __init__(self, **kwargs):
        # DEFAULT VALUES
        self.index = next(self._index)
        self.name = '{}_{}'.format(self.__class__.__name__.lower(), self.index)
        self.width = 300
        self.height = 30
        self.margin = '0,{},0,0'.format(self.index * self.height + V_SPACING * self.index)
        self.horizontal_alignment = "Left"
        self.vertical_alignment = "Top"
        # CUSTOM VALUES
        self.__dict__.update(kwargs)

    def sorted_attributes(self):
        return sorted(vars(self), key=lambda x: x.name == 'Name')

    def __str__(self):
        """ <Label x:  Index="0"  Name="label_0"  Width="30"  Height="30"
             HorizontalAlignment="Left"  VerticalAlignment="Top" />"""
        attributes = ''
        for attr_name, value in vars(self).iteritems():
            if attr_name not in self.allowed_attributes:
                continue
            component = ComponentAttribute(attr_name, value)
            attributes += str(component)
        formatted_component = self.template.format(
                                            component=self.__class__.__name__,
                                            attributes=attributes)
        print('Components: {}'.format(formatted_component))
        return formatted_component

class Label(Component):

    def __init__(self, content, **kwargs):
        Component.__init__(self, **kwargs)
        self.content = content


class TextBox(Component):

    def __init__(self, **kwargs):
        Component.__init__(self, **kwargs)


class Button(Component):

    def __init__(self, content, **kwargs):
        Component.__init__(self, **kwargs)
        self.content = content

class ComboBox(Component):

    def __init__(self, options, **kwargs):
        Component.__init__(self, **kwargs)
        self.options = options


if __name__ == '__main__':
    pass
    components = [
                  Label('Briaaan'),
                  TextBox(),
                  ComboBox({'A': 1}),
                  Button('Button!', width=50, horizontal_alignment="Right"),
                 ]

    form = CustomForm('Title', components)
    form.show()
