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

    print('Local vars: ' + str(stack_locals))
    print('Global vars: ' + str(stack_globals))
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
    LAYOUT = """
    <Window
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    xmlns:local="clr-namespace:WpfApplication1"
    mc:Ignorable="d"
    Title="MainWindow" Height="350" Width="525">
    <Grid>
    <TextBox x:Name="text_box"
    KeyDown="OnKeyDownHandler"
    KeyUp="OnKeyUpHandler"
    Height="319"
    AcceptsReturn="True"
    TextWrapping="Wrap"
    Text="TextBox"
    VerticalAlignment="Top"
    VerticalScrollBarVisibility="Auto"
    HorizontalAlignment="Left"
    Width="517"/>
    </Grid>
    </Window>
    """

    NEWLINE = '>>> '

    def __init__(self, stack_globals, stack_locals):

        self.stack_locals = stack_locals
        self.stack_globals = stack_globals

        self.ui = wpf.LoadComponent(self, StringReader(Console.LAYOUT))
        # self.ui.Title = title
        self.ui.text_box.Text = Console.NEWLINE
        self.ui.text_box.Focus()
        self.ui.text_box.CaretIndex = self.ui.text_box.Text.Length

        # if description is not None:
            # self.ui.selection_label.Content = description
        # self.ui.button_select.Click += self.select_click

    def OnKeyUpHandler(self, sender, args):
        line_count = sender.LineCount
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

if __name__ == '__main__':
    # console = Console()
    # console.show()
    def some():
        xxxxxxxxxxxxxxxxxxxx = 'asdadasdasdqweqweqw'
        y = 3
        debug()

    some()
