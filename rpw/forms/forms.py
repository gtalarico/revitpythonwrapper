"""
>>> form = rpw.forms.SelectFromList('Test Window', ['1','2','3'])
>>> form.show()
>>> print(form.selected)
>>> '1'

"""
# TODO: Move to __init__.py to avoid rpw.forms.forms
#       or import class into forms namespaces (failed sphinx build earlier)

import sys
try:
    import clr
    import os
    # IronPython.Wpf is included with RPW: script path is added.
    sys.path.append(os.path.dirname(__file__))
    # Standard Location Added for use in Dynamo, where script cannot reach inside
    # Zip file shipped through package Manager
    sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Platforms\Net40')
    clr.AddReference("PresentationFramework")
    try:
        clr.AddReference('IronPython.Wpf')
        import wpf
    except IOError:
        raise IOError('Could not find IronPython.Wpf. Path: {}'.format(str(sys.path)))
    except ImportError:
        raise ImportError('Could not Import IronPython.Wpf. Path: {}'.format(str(sys.path)))

    from System.Windows import Application, Window
    from System.IO import StringReader
except ImportError:
    from rpw.utils.sphinx_compat import *


class SelectFromList(Window):
    """
    WPF form with ComboBox dropdown.

    Args:
        title (str): Title of form
        options ([str]): List of Options as stings
        description (str): Description of input requested

    Usage:
        >>> form = SelectFromList('Test Window', ['1','2','3'])
        >>> form_ok = form.show()
        >>> if not form_ok:
        >>>     sys.exit() # User Canceld
        >>> selected_item = form.selected

    .. note: XAML is embeded instead loaded from file so that package can be
             kept as .zip for dynamo.
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
                    <Label x:Name="selection_label" Content="Select Item" HorizontalAlignment="Left" Height="30"
                        VerticalAlignment="Top" Width="299"/>
                    <ComboBox x:Name="combo_data" HorizontalAlignment="Left" Margin="0,30,0,0"
                        VerticalAlignment="Top" Width="299"/>
                    <Button x:Name="button_select" Content="Select" HorizontalAlignment="Left" Height="26"
                    Margin="0,63,0,0" VerticalAlignment="Top" Width="299"/>
                </Grid>
            </Window>
            """

    def __init__(self, title, options, description=None):
        # TODO: Validate options type, and handle dictionary input
        # So user can feed a list or a dictionary
        self.selected = None
        self.ui = wpf.LoadComponent(self, StringReader(SelectFromList.LAYOUT))
        # self.ui = wpf.LoadComponent(self, os.path.join(cwd, 'form_select_list.xaml'))
        self.ui.Title = title

        if description is not None:
            self.ui.selection_label.Content = description
        self.ui.button_select.Click += self.select_click

        self.ui.combo_data.Items.Clear()
        self.ui.combo_data.ItemsSource = options
        self.ui.combo_data.SelectedItem = options[0]

    def select_click(self, sender, e):
        self.selected = self.ui.combo_data.SelectedItem
        self.DialogResult = True
        self.Close()

    def show(self):
        return super(SelectFromList, self).ShowDialog()

class TextInput(Window):
    """
    WPF form with TextInput.

    Args:
        title (str): Title of form
        default ([str]): Default value for text box
        description (str): Description of input requested


    Usage:
        >>> prompt = TextInput('Title', default="3")
        >>> prompt.show()
        >>> print(prompt.selected)
    """

    LAYOUT = """
            <Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
                    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                    xmlns:local="clr-namespace:WpfApplication1"
                    mc:Ignorable="d" Height="140.139" Width="325" ResizeMode="NoResize" Title="" WindowStartupLocation="CenterScreen" Topmost="True" SizeToContent="WidthAndHeight">
                <Grid Margin="10,0,10,10">
                    <Label x:Name="selection_label" Content="Select Item" HorizontalAlignment="Left" Height="30" VerticalAlignment="Top" Width="299"/>

                    <TextBox x:Name="text_box" HorizontalAlignment="Left" Margin="0,30,0,0" VerticalAlignment="Top" Width="299"/>

                    <Button x:Name="button_select" Content="Select" HorizontalAlignment="Left" Height="26" Margin="0,63,0,0" VerticalAlignment="Top" Width="299"/>

                </Grid>
            </Window>
            """

    def __init__(self, title, default=None, description=None):
        self.selected = None
        self.ui = wpf.LoadComponent(self, StringReader(TextInput.LAYOUT))
        # self.ui = wpf.LoadComponent(self, os.path.join(cwd, 'form_text_input.xaml'))
        self.ui.Title = title

        if default is not None:
            self.ui.text_box.Text = default

        if description is not None:
            self.ui.selection_label.Content = description
        self.ui.button_select.Click += self.select_click

    def select_click(self, sender, e):
        self.DialogResult = True
        self.selected = self.ui.text_box.Text
        self.Close()

    def show(self):
        return super(TextInput, self).ShowDialog()


class Alert():
    def __init__(self, title=None, heading=None, message=None):
        raise NotImplemented
        # dialog = TaskDialog(alert_title)
        # dialog.MainInstruction = alert_heading
        # dialog.MainContent = alert_content
        # alert_result = dialog.Show()



if __name__ == '__main__':
    prompt = SelectFromList('Title', ['A','B'], description="Your Options")
    prompt.show()
    print(prompt.selected)
#
    prompt = TextInput('Title', default="3")
    prompt.show()
    print(prompt.selected)
