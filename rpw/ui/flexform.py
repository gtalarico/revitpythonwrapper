""" FlexForm """

from itertools import count

from rpw.utils.dotnet import Enum
from rpw.ui.forms import *

from System.Windows import Controls, Window
from System.Windows import HorizontalAlignment, VerticalAlignment, Thickness


class FlexForm(Window):
    """
    Flex Form Usage

    >>> components = [Label('Label'),
                      ComboBox(Name='combobox1'{'Option 1': 10.0, 'Option 2', 20.0}),
                      TextBox(Name='textbox1'),
                      CheckBox(Name='checkbox1'),
                      Separator(),
                      Button('Select')]

    >>> form = FlexForm('Title', components)
    >>> form.show()
    >>> # User selects `Option 1`, types 'Wood' in TextBox, and select Checkbox
    >>> form.values
    {'combobox1': 10.0, 'textbox1': 'Wood', 'checkbox': True}

    """
    layout = """
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

    def __init__(self, title, components, **kwargs):
        """
        Args:
            title (``str``): Form Title
            components (``list``): List of Form Components.
            top_offset (``float``): Optional top offset.
            options (``kwargs``): WPF Parameters Options

        """

        self.ui = wpf.LoadComponent(self, StringReader(self.layout))
        self.ui.Title = title
        self.values = {}

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        for n, component in enumerate(components):
            # print(component.Margin)
            self.MainGrid.Children.Add(component)
            if hasattr(component, 'on_click'):
                component.Click += FlexForm.get_values

            V_SPACE = 5
            if n > 0:
                prev_comp = components[n-1]
                top = prev_comp.Margin.Top + prev_comp.Height + V_SPACE + getattr(component, 'top_offset', 0)
                component.Margin = Thickness(0, top, 0, 0)

    def show(self):
        """
        Initializes Form. Returns ``True`` or ``False`` if form was exited.
        """
        return self.ShowDialog()

    @staticmethod
    def get_values(sender, e):
        """ Default Get Values. Collect values from controls and close """
        component_values = {}
        window = Window.GetWindow(sender)
        for component in window.MainGrid.Children:
            try:
                component_values[component.Name] = component.value
            except AttributeError:
                pass
        window.values = component_values
        window.close()

    def close(self):
        """ Exits Form. Returns ``True`` to ``show()`` method """
        self.DialogResult = True
        self.Close()


class RpwControlMixin():
    """ Control Mixin """
    _index = count(0)

    def __init__(self, **kwargs):
        self.set_attrs(**kwargs)

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

        # Inject Any other Custom Values into Component
        # Updating __dict__ fails due to how .NET inheritance/properties works
        for key, value in kwargs.iteritems():
            setattr(self, key, value)


class Label(RpwControlMixin, Controls.Label):
    """
    Windows.Controls.Label Wrapper

    >>> Label('Label Text')
    """
    def __init__(self, label_text, **kwargs):
        """
        Args:
            label_text (``str``): Label Text
            wpf_params (kwargs): Additional WPF attributes
        """
        self.Content = label_text
        top_offset = 5
        self.set_attrs(**kwargs)


class TextBox(RpwControlMixin, Controls.TextBox):
    """
    Windows.Controls.TextBox Wrapper

    >>> TextBox()
    """
    def __init__(self, **kwargs):
        """
        Args:
            wpf_params (kwargs): Additional WPF attributes
        """
        self.set_attrs(**kwargs)

    @property
    def value(self):
        return self.Text


class Button(RpwControlMixin, Controls.Button):
    """
    Windows.Controls.Button Wrapper

    >>> Button('Select')
    """
    def __init__(self, button_text, **kwargs):
        """
        Args:
            button_text (``str``): Button Text
            wpf_params (kwargs): Additional WPF attributes
        """
        self.Content = button_text
        self.on_click = kwargs.get('Click', FlexForm.get_values)
        self.set_attrs(**kwargs)


class CheckBox(RpwControlMixin, Controls.CheckBox):
    """
    Windows.Controls.Checkbox Wrapper

    >>> CheckBox('Label')
    """
    def __init__(self, checkbox_text, **kwargs):
        """
        Args:
            button_text (``str``): Button Text
            wpf_params (kwargs): Additional WPF attributes
        """
        self.Content = checkbox_text
        self.set_attrs(top_offset=5, **kwargs)

    @property
    def value(self):
        return self.IsChecked


class ComboBox(RpwControlMixin, Controls.ComboBox):
    """
    Windows.Controls.ComboBox Wrapper

    >>> ComboBox({'Option 1': Element, 'Option 2', 'Elemnet'})
    """
    def __init__(self, options, **kwargs):
        """
        Args:
            options (``list``, ``dict``): If ``dict``, selected value is returned
            wpf_params (kwargs): Additional WPF attributes
        """
        self.set_attrs(**kwargs)

        self.options = options
        if hasattr(options, 'keys'):
            options = options.keys()
        if kwargs.get('sort', True):
            options.sort()

        self.Items.Clear()
        self.ItemsSource = options
        self.SelectedItem = options[0]

    @property
    def value(self):
        selected = self.SelectedItem
        if isinstance(self.options, dict):
            selected = self.options[selected]
        return selected

class Separator(RpwControlMixin, Controls.Separator):
    """ WPF Separator """

if __name__ == '__main__':
    components = [
                  Label('Enter Family Name'),
                  TextBox(Name='family_name', Text='XXX-XXX'),
                  Label('Select Tyspe'),
                  ComboBox({'24x36': 1, '36x48': 2, '48x64': 3}),
                  Separator(),
                  ComboBox(['Z', 'X', 'Y']),
                  CheckBox('Select Me'),
                  Label('Option 2'),
                  CheckBox('Select Me'),
                  CheckBox('Select Me', IsChecked=True),
                  Label('Option 2'),
                  Label('Option 2'),
                  Button('Press'),
                  Label('Option 2'),
                  Button('Press'),
                  ]

    form = FlexForm('Title', components).show()
