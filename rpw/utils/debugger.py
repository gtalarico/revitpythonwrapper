import sys
import inspect

# from rpw.utils.logger import logger

def debug():
    # stack_tuple = inspect.stack()[1]
    stack_tuple = inspect.stack()[2]

    stack_filename = stack_tuple[1]
    stack_line = stack_tuple[2]
    stack_name = stack_tuple[3]

    stack = stack_tuple[0]
    stack_locals = stack.f_locals
    stack_globals = stack.f_globals

    # print('Local vars: ' + str(stack_locals))
    # print('Global vars: ' + str(stack_globals))
    console = Console(stack_globals, stack_locals)
    console.ShowDialog()

try:
    import clr
    import os
    # Standard Location Added for use in Dynamo, where script cannot reach inside
    sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Platforms\Net40')
    clr.AddReference("PresentationFramework")
    clr.AddReference("WindowsBase") #System.Windows.Input
    clr.AddReference('IronPython')
    # clr.AddReference('IronPython.Modules')
    clr.AddReference('IronPython.Wpf')
    from IronPython.Modules import Wpf as wpf
    from System.Windows import Application, Window
    from System.IO import StringReader
    from System.Environment import Exit, NewLine
    from System.Windows.Input import Key
    # from rpw.revit import UI
except ImportError as errmsg:
    print('Import Error')
    print(errmsg)
    # logger.error('Import Error: {}'.format(errmsg))
    # from rpw.utils.sphinx_compat import *

class Console(Window):
    # https://www.roelvanlisdonk.nl/2010/12/09/setting-100-width-and-100-height-for-a-textbox-in-wpf/
    LAYOUT = """
    <Window
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    Title="DeployWindow" Height="400" Width="800" SnapsToDevicePixels="True" UseLayoutRounding="True" WindowState="Normal" WindowStartupLocation="CenterScreen"
    >
    <Grid>
    <Grid.ColumnDefinitions>
    <ColumnDefinition Width="*"></ColumnDefinition>
    </Grid.ColumnDefinitions>
    <Grid.RowDefinitions>
    <RowDefinition Height="0"></RowDefinition>
    <RowDefinition Height="*"></RowDefinition>
    </Grid.RowDefinitions>
    <TextBox Grid.Column="1" Grid.Row="1"  HorizontalAlignment="Stretch" KeyDown="OnKeyDownHandler" KeyUp="OnKeyUpHandler"
    Name="text_box" Margin="6,6,6,6" VerticalAlignment="Stretch" AcceptsReturn="True" VerticalScrollBarVisibility="Auto" />
    </Grid>
    </Window>
    """
    # <Button Grid.Column="1" Content="Deploy" Height="30" Width="100" HorizontalAlignment="Left" Margin="10,10,10,10" Name="deployButton" Cursor="Hand" />

    NEWLINE = '>>> '

    def __init__(self, stack_globals, stack_locals):

        self.stack_locals = stack_locals
        self.stack_globals = stack_globals

        self.ui = wpf.LoadComponent(self, StringReader(Console.LAYOUT))
        self.ui.Title = 'RevitPythonWrapper Stack Debugger'

        self.ui.text_box.Text = Console.NEWLINE
        self.ui.text_box.Focus()
        self.ui.text_box.CaretIndex = self.ui.text_box.Text.Length

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
            sender.AppendText(Console.NEWLINE)

    def evaluate(self, line):
        # print('Stack: ' + str(self.stack_vars))
        output = eval(line, self.stack_globals, self.stack_locals)
        return output

    def OnKeyDownHandler(self, sender, args):
        pass

# if __name__ == '__main__':
#     # console = Console()
#     # console.show()
#     def some():
#         xxxxxxxxxxxxxxxxxxxx = 'asdadasdasdqweqweqw'
#         y = 3
#         debug()
#
#     some()
