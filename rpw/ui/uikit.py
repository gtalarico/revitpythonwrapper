# This is only so forms.py to be executed on console for easier testing and dev
# `ipy.exe forms.py` and ipy -X:FullFrames console.py
from itertools import count

from rpw.utils.dotnet import Enum
from rpw.ui.forms import *
# logger.verbose(True)

from System.Windows import Controls
from System.Windows import HorizontalAlignment, VerticalAlignment, Thickness


class CustomForm(Window):

    LAYOUT = """
            <Window
                xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
                xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                xmlns:local="clr-namespace:WpfApplication1" mc:Ignorable="d"
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
        layout = CustomForm.LAYOUT.format(components=self.LAYOUT)

        self.ui = wpf.LoadComponent(self, StringReader(layout))
        self.ui.Title = title
        self.values = {}

        for component in components:
            self.MainGrid.Children.Add(component)
            if hasattr(component, 'on_click'):
                component.Click += getattr(self, component.on_click)

    def show(self):
        return super(CustomForm, self).ShowDialog()

    def get_values(self, sender, e):
        component_values = {}
        for component in self.MainGrid.Children:
            try:
                component_values[component.Name] = component.value
            except AttributeError:
                pass
        self.values = component_values
        self.close()

    def close(self):
        self.DialogResult = True
        self.Close()


class RpwControlMixin():
    _index = count(0)

    def set_attrs(self, **kwargs):
        """ Parses kwargs, sets default values where appropriate. """
        self.index = next(self._index)  # Counts Instatiation to control Height

        # Default Values
        control_type = self.__class__.__name__
        self.Name = kwargs.get('Name', '{}_{}'.format(control_type, self.index))
        self.Width = 300
        self.Height = 25

        h_align = Enum.Parse(HorizontalAlignment, kwargs.get('h_align', 'Left'))
        self.HorizontalAlignment = h_align
        v_align = Enum.Parse(VerticalAlignment, kwargs.get('v_align', 'Top'))
        self.VerticalAlignment = v_align

        # Default Margin Settings
        V_SPACING = 5
        margin_left = kwargs.get('left', 0)
        margin_right = kwargs.get('right', 0)
        margin_bottom = kwargs.get('bottom', 0)
        margin_top = kwargs.get('top', self.index * self.Height +
                                       self.index * V_SPACING)



        self.Margin = Thickness(margin_left, margin_top,
                                margin_right, margin_bottom)

        # Inject Any other Custom Values into Component
        self.__dict__.update(kwargs)


class Label(Controls.Label, RpwControlMixin):

    def __init__(self, label_text, **kwargs):
        self.Content = label_text
        self.set_attrs(**kwargs)


class TextBox(Controls.TextBox, RpwControlMixin):

    def __init__(self, **kwargs):
        self.set_attrs(**kwargs)

    @property
    def value(self):
        return self.Text


class Button(Controls.Button, RpwControlMixin):

    def __init__(self, button_text, **kwargs):
        self.Content = button_text
        self.on_click = kwargs.get('Click', 'get_values')
        self.set_attrs(**kwargs)


class CheckBox(Controls.CheckBox, RpwControlMixin):

    def __init__(self, checkbox_text, **kwargs):
        self.Content = checkbox_text
        self.Padding = Thickness(0, 1, 0, 0)
        self.Height = 30
        self.set_attrs(**kwargs)

    @property
    def value(self):
        return self.IsChecked


class ComboBox(Controls.ComboBox, RpwControlMixin):

    def __init__(self, options, **kwargs):
        self.set_attrs(**kwargs)

        self.options = options
        if hasattr(options, 'keys'):
            options = options.keys()
        if kwargs.get('sort', True):
            options.sort()

        self.Items.Clear()
        self.ItemsSource = options
        self.SelectedItem = options[0]
        # self.Focus()

    @property
    def value(self):
        selected = self.SelectedItem
        if isinstance(self.options, dict):
            selected = self.options[selected]
        return selected

if __name__ == '__main__':
    components = [
                  Label('Option 1'),
                  TextBox(),
                  Label('Option 2'),
                  ComboBox({'A': 1, 'B':2, 'C':3}),
                  ComboBox(['Z', 'X', 'Y']),
                  CheckBox('Select Me'),
                  CheckBox('Select Me'),
                  Label('Option 2'),
                  CheckBox('Select Me'),
                  Button('Press'),
                 ]

    form = CustomForm('UI Kit', components)
    form.show()
    print(form)
    print(form.values)
