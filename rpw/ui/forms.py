"""
Forms are provided to facilitate user input.

"""

import sys
from rpw.utils.logger import logger

try:
    import clr
    import os
    # Standard Location Added for use in Dynamo, where script cannot reach inside
    sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Platforms\Net40')
    clr.AddReference("PresentationFramework")   # ?
    clr.AddReference("WindowsBase")             # System.Windows.Input
    try:
        clr.AddReference('IronPython')
        # clr.AddReference('IronPython.Modules')
        clr.AddReference('IronPython.Wpf')
        from IronPython.Modules import Wpf as wpf
    except IOError as errmsg:
        logger.error(errmsg)
        raise IOError('Could not find IronPython.Wpf. Path: {}'.format(str(sys.path)))
    except ImportError as errmsg:
        logger.error(errmsg)
        raise ImportError('Could not Import IronPython.Wpf. Path: {}'.format(str(sys.path)))

    from System.Windows import Application, Window
    from System.IO import StringReader
    from System.Environment import Exit, NewLine
    from System.Windows.Input import Key
    from rpw.revit import UI
except ImportError as errmsg:
    logger.error('Import Error: {}'.format(errmsg))
    from rpw.utils.sphinx_compat import *


class SelectFromListForm(Window):
    """
    WPF form with ComboBox dropdown.

    Args:
        title (str): Title of form
        options (dict,list[str]): Dictionary (string keys) or List[strings]
        description (str): Optional Description of input requested  [default: None]
        sort (bool): Optional sort flag - sorts keys [default: True]
        exit_on_close (bool): Form will call sys.exit() if Closed on X. [default: True]

    Usage:
        >>> form = SelectFromList('Test Window', ['1','2','3'])
        >>> # Dropdown shows '1', '2' ,'3'. User clicks Select '1'
        >>> form
        True
        >>> form.selected
        '1'
        >>> # Dictionary
        >>> form = SelectFromList('Test Window', {'Text':str, 'Number':int})
        >>> # User clicks Text
        >>> form
        True
        >>> form.selected
        str

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

    def __init__(self, title, options, description=None, sort=True):
        self.selected = None
        self.ui = wpf.LoadComponent(self, StringReader(SelectFromListForm.LAYOUT))
        # self.ui = wpf.LoadComponent(self, os.path.join(cwd, 'form_select_list.xaml'))
        self.ui.Title = title

        if description is not None:
            self.ui.selection_label.Content = description
        self.ui.button_select.Click += self.select_click

        self.options = options

        if isinstance(options, dict):
            options = options.keys()
        if sort:
            options = sorted(options)

        self.ui.combo_data.Items.Clear()
        self.ui.combo_data.ItemsSource = options
        self.ui.combo_data.SelectedItem = options[0]
        self.ui.combo_data.Focus()

    def select_click(self, sender, e):
        selected = self.ui.combo_data.SelectedItem
        if isinstance(self.options, dict):
            selected = self.options[selected]

        self.selected = selected
        self.DialogResult = True
        self.Close()

    def show(self):
        return super(SelectFromListForm, self).ShowDialog()

class TextInputForm(Window):
    """
    WPF form with TextInput.

    Args:
        title (str): Title of form
        default (str): Optional default value for text box [default: None]
        description (str): Optional Description of input requested  [default: None]
        exit_on_close (bool): Form will call sys.exit() if Closed on X. [default: True]


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
                    <Label x:Name="selection_label" Content="Enter Text" HorizontalAlignment="Left" Height="30" VerticalAlignment="Top" Width="299"/>

                    <TextBox x:Name="text_box" HorizontalAlignment="Left" Margin="0,30,0,0" VerticalAlignment="Top" Width="299"/>

                    <Button x:Name="button_select" Content="Select" HorizontalAlignment="Left" Height="26" Margin="0,63,0,0" VerticalAlignment="Top" Width="299"/>

                </Grid>
            </Window>
            """

    def __init__(self, title, default=None, description=None):
        self.selected = None
        self.ui = wpf.LoadComponent(self, StringReader(TextInputForm.LAYOUT))
        # self.ui = wpf.LoadComponent(self, os.path.join(cwd, 'form_text_input.xaml'))
        self.ui.Title = title

        self.ui.text_box.Focus()
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
        return super(TextInputForm, self).ShowDialog()


class Alert():
    def __init__(self, message, title='Alert', heading='', exit=False):
        """
        Creates Standard Revit Alert.

        Args:
            message (str): TaskDialog Message
            title (str, optional): TaskDialog Title
            heading (str, optional): TaskDialog Message Heading
            exit (bool, optional): Exit Script after Dialog. Useful for handled Errors.

        Usage:
            >>> Alert('Your Message', title="Title", heading="Some Heading")
            >>> Alert('You need to select Something', exit=True)
        """
        dialog = UI.TaskDialog(title)
        dialog.MainInstruction = heading
        dialog.MainContent = message
        self.result = dialog.Show()

        if exit:
            sys.exit(1)


class Console(Window):
    """ Perfect for Debugging / Inspecting """
    # https://www.roelvanlisdonk.nl/2010/12/09/setting-100-width-and-100-height-for-a-textbox-in-wpf/
    # Check RPS for Autocomplete/History ?
    # https://github.com/architecture-building-systems/revitpythonshell/blob/master/IronTextBox/IronTextBox.cs
    LAYOUT = """
    <Window
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    Title="DeployWindow" Height="400" Width="800" SnapsToDevicePixels="True"
    UseLayoutRounding="True" WindowState="Normal" WindowStartupLocation="CenterScreen"
    >
    <Grid>
    <Grid.ColumnDefinitions>
    <ColumnDefinition Width="*"></ColumnDefinition>
    </Grid.ColumnDefinitions>
    <Grid.RowDefinitions>
    <RowDefinition Height="0"></RowDefinition>
    <RowDefinition Height="*"></RowDefinition>
    </Grid.RowDefinitions>
    <TextBox Grid.Column="1" Grid.Row="1"  HorizontalAlignment="Stretch"
    KeyDown="OnKeyDownHandler" KeyUp="OnKeyUpHandler"
    Name="text_box" Margin="6,6,6,6" VerticalAlignment="Stretch" AcceptsReturn="True" VerticalScrollBarVisibility="Auto" />
    </Grid>
    </Window>
    """
    # <Button Grid.Column="1" Content="Deploy" Height="30" Width="100" HorizontalAlignment="Left" Margin="10,10,10,10" Name="deployButton" Cursor="Hand" />

    CARET = '>>> '

    # def __init__(self, stack_globals, stack_locals):
    def __init__(self):

        import inspect
        stack_tuple = inspect.stack()[2]

        stack_filename = stack_tuple[1]
        stack_line = stack_tuple[2]
        stack_name = stack_tuple[3]

        stack = stack_tuple[0]
        stack_locals = stack.f_locals
        stack_globals = stack.f_globals

        # print('Local vars: ' + str(stack_locals))
        # print('Global vars: ' + str(stack_globals))
        # console_form = Console(stack_globals, stack_locals)
        # console_form.ShowDialog()

        self.stack_locals = stack_locals
        self.stack_globals = stack_globals

        self.ui = wpf.LoadComponent(self, StringReader(Console.LAYOUT))
        self.ui.Title = 'RevitPythonWrapper Stack Debugger'

        self.ui.text_box.Text = Console.CARET
        self.ui.text_box.Focus()
        self.ui.text_box.CaretIndex = self.ui.text_box.Text.Length

        self.PreviewKeyDown += self.KeyDownEvent

        self.ShowDialog()
        # if description is not None:
            # self.ui.selection_label.Content = description
        # self.ui.button_select.Click += self.select_click

    def OnKeyUpHandler(self, sender, args):
        line_count = sender.LineCount
        if line_count == 1:
            return
        if args.Key == Key.Enter:
            last_line = line_count - 1
            # line = sender.GetLineText(line_count - 2)[3:-1] - ipy console
            line = sender.GetLineText(line_count - 2)[3:-1]
            try:
                output = self.evaluate(line)
            except Exception as errmsg:
                output = str(errmsg)

            output = '{}'.format(str(output))
            sender.AppendText(output)
            sender.AppendText(NewLine)
            sender.AppendText(Console.CARET)

    def evaluate(self, line):
        # print('Stack: ' + str(self.stack_vars))
        output = eval(line, self.stack_globals, self.stack_locals)
        return output

    def OnKeyDownHandler(self, sender, args):
        pass

    def KeyDownEvent(self, sender, e):
        e.Handled = False
        if e.Key == Key.Up:
            e.Handled = True



class FormWrapper(object):
    """ Wraps WPF Window """

    def __init__(self, *args, **kwargs):
        form_class = getattr(self.__class__, 'form_class', None)
        self.__class__.__doc__ = form_class.__doc__
        if not form_class:
            raise Exception('FormWrapper is for inheritance only')

        self.exit_on_close = kwargs.pop('exit_on_close', True)
        self.form = form_class(*args, **kwargs)

    def show(self):
        results = self.form.show()
        if not results and self.exit_on_close:
            logger.debug('Form was closed. Script will exit.')
            sys.exit(1)
        elif results:
            return True
        else:
            return False

    def __getattr__(self, attr):
        return getattr(self.form, attr)


class SelectFromList(FormWrapper):
    form_class = SelectFromListForm
    __doc__ = SelectFromListForm.__doc__


class TextInput(FormWrapper):
    form_class = TextInputForm
    __doc__ = TextInputForm.__doc__


if __name__ == '__main__':
    prompt = SelectFromList('Title', ['A','B'], description="Your Options", exit_on_close=True)
    prompt.show()
    print(prompt.selected)

    prompt = SelectFromList('Title', {'A':5, 'B':10}, description="Your Options", exit_on_close=True)
    prompt.show()
    print(prompt.selected)

    prompt = TextInput('Title', default="3", exit_on_close=True)
    prompt.show()
    print(prompt.selected)
    print('forms.py ran')

#
