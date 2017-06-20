# This is only so forms.py to be executed on console for easier testing and dev
# `ipy.exe forms.py` and ipy -X:FullFrames console.py
from itertools import count

from rpw.ui.forms import *
# logger.verbose(True)

from System.Windows import Controls
print('Custom Forms Started')
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
                mc:Ignorable="d"
                ResizeMode="NoResize"
                WindowStartupLocation="CenterScreen"
                Topmost="True"
                SizeToContent="WidthAndHeight">
                <Grid Name="MainGrid" Margin="10,10,10,10">
                </Grid>
            </Window>
            """
            # {components}
            # Height="140.139" Width="325"

    def __init__(self, title, components):
        # components_string = ''.join([str(e) for e in components])
        # layout = CustomForm.LAYOUT.format(components=components_string.strip())
        layout = CustomForm.LAYOUT.format(components=self.LAYOUT)

        self.ui = wpf.LoadComponent(self, StringReader(layout))
        self.ui.Title = title

        # l = Controls.Label()
        # l.Content = 'GUUUU'

        # for component in components:
        self.MainGrid.Children.Add(components[0])

    def show(self):
        return super(CustomForm, self).ShowDialog()

    def close(self, sender, e):
        component_values = {}
        for component in self.MainGrid.Children:
            component_values[component.Name] = component
        self.value = component_values
        self.Close()
        # if description is not None:
        #     self.ui.selection_label.Content = description
        # self.ui.button_select.Click += self.select_click

    # def button_click(self, sender, e):
    #     self.Close()
        # selected = self.ui.combo_data.SelectedItem
    #     if isinstance(self.options, dict):
    #         selected = self.options[selected]
    #
    #     self.selected = selected
    #     self.DialogResult = True



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

    def __init__(self, **kwargs):
        # DEFAULT VALUES
        self.index = next(self._index)
        self.name = kwargs.get('name', self.__class__.__name__ + str(self.index))
        self.width = 300
        self.height = 25
        self.horizontal_alignment = "Left"
        self.vertical_alignment = "Top"

        # Default Margin Settings
        V_SPACING = 5
        margin_left = kwargs.get('left', 0)
        margin_right = kwargs.get('right', 0)
        margin_bottom = kwargs.get('bottom', 0)
        margin_top = kwargs.get('top', self.index * self.height +
                                       self.index * V_SPACING)

        margin = '{left},{top},{right},{bot}'.format(left=margin_left,
                                                     top=margin_top,
                                                     right=margin_right,
                                                     bot=margin_bottom)
        self.margin = margin
        # Inject Custom Values
        self.__dict__.update(kwargs)

    def sorted_attributes(self):
        return sorted(vars(self), key=lambda x: x.name == 'Name')

    def __str__(self):
        """ <Label x:Name="label_0"  Width="30"  Height="30"
             HorizontalAlignment="Left"  VerticalAlignment="Top" />"""
        attributes = ''
        for attr_name, value in vars(self).iteritems():
            if attr_name not in self.allowed_attributes:
                continue
            component = ComponentAttribute(attr_name, value)
            attributes += str(component)
        component_str = self.template.format(component=self.__class__.__name__,
                                             attributes=attributes)
        print(component_str)
        return component_str


class Label(Controls.Label, Component):

    def __init__(self, content, **kwargs):
        self.content = content
        Component.__init__(self, **kwargs)
        self.Content = content

class TextBox(Component, Controls.TextBox):

    def __init__(self, **kwargs):
        Component.__init__(self, **kwargs)
        self.Text = 'Shiiiit'

    @property
    def value(self):
        return self.Text

class Button(Component):

    def __init__(self, content, **kwargs):
        self.content = content
        Component.__init__(self, **kwargs)

    @property
    def value(self):
        return self.Content


class ComboBox(Component):

    def __init__(self, options, **kwargs):
        Component.__init__(self, name, **kwargs)
        self.options = options


if __name__ == '__main__':
    components = [
                  Label('Option 1'),
                #   TextBox(name='textbox1'),
                #   Label('Option 2'),
                #   TextBox(name='textbox2'),
                #   Button('button1', click='close'),
                #   ComboBox({'A': 1}),
                 ]

    form = CustomForm('Title', components)
    form.show()
    print(form)
    print(form.value)
