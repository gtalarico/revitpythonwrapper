import os
import inspect
import tempfile
from collections import defaultdict

from rpw.utils.logger import logger
from forms import *

clr.AddReference("System.Drawing")          # System.Windows.Input
from System.Drawing import FontFamily
from System.Windows.Input import Key

class Console(Window):
    """ REPL Console for Inspecting Stack

    >>> from rpw.forms import Console
    >>> Console()

    Args:
        stack_level (int, optional): Stack Level. Default is 1.
        stack_info (bool): Print Stack Call info. Default is False.

    """
    LAYOUT = """
                <Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                        Title="DeployWindow" Height="400" Width="800" SnapsToDevicePixels="True"
                        UseLayoutRounding="True" WindowState="Normal" WindowStartupLocation="CenterScreen">
            	<Window.Resources>
            		<Style TargetType="{x:Type MenuItem}">
            			<Setter Property="FontFamily" Value="Consolas"/>
            			<Setter Property="FontSize" Value="12.0"/>
            		</Style>
            	</Window.Resources>
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
                         Name="tbox" Margin="6,6,6,6" VerticalAlignment="Stretch"
                         AcceptsReturn="True" VerticalScrollBarVisibility="Auto"
                         TextWrapping="Wrap"
                         FontFamily="Consolas" FontSize="12.0"
                         />
                </Grid>
                </Window>
    """
    # <Button Grid.Column="1" Content="Deploy" Height="30" Width="100" HorizontalAlignment="Left" Margin="10,10,10,10" Name="deployButton" Cursor="Hand" />

    CARET = '>>> '

    def __init__(self, stack_level=1, stack_info=False):

        # History Helper
        tempdir = tempfile.gettempdir()
        filename = 'rpw-history'
        self.history_file = os.path.join(tempdir, filename)

        # Stack Info
        # stack = inspect.currentframe().f_back
        stack_frame = inspect.stack()[stack_level][0] # Finds Calling Stack

        self.stack_locals = stack_frame.f_locals
        self.stack_globals = stack_frame.f_globals
        stack_code = stack_frame.f_code
        logger.debug('Local vars: ' + str(self.stack_locals))
        logger.debug('Global vars: ' + str(self.stack_globals))

        stack_filename = os.path.basename(stack_code.co_filename)
        stack_lineno = stack_code.co_firstlineno
        stack_caller = stack_code.co_name

        # Form Setup
        self.ui = wpf.LoadComponent(self, StringReader(Console.LAYOUT))
        self.ui.Title = 'RevitPythonWrapper Console'
        self.PreviewKeyDown += self.KeyPressPreview

        # Form Init
        self.ui.tbox.Focus()
        if stack_info:
            self.write_line('Caller: {} [line:{}] | File: {}'.format(stack_caller, stack_lineno, stack_filename))

        self.ui.tbox.CaretIndex = len(self.tbox.Text)

        # Vars
        self.history_index = 0
        self.ac_options = defaultdict(int)

        self.ShowDialog()

    def get_line(self, index):
        line = self.tbox.GetLineText(index).replace('\r\n','')
        if line.startswith(Console.CARET):
            line = line[len(Console.CARET):]
        logger.debug('Get Line: {}'.format(line))
        return line

    def get_last_line(self):
        try:
            last_line = self.get_lines()[-1]
        except IndexError:
            last_line = self.get_line(0)

        return last_line

    def get_lines(self):
        last_line_index = self.tbox.LineCount - 1
        lines = []
        for index in range(0, last_line_index):
            line = self.get_line(index)
            lines.append(line)
        logger.debug('Lines: {}'.format(lines))
        return lines

    def OnKeyUpHandler(self, sender, args):
        """ Need to use this to be able to override ENTER """
        if self.tbox.LineCount == 1:
            return
        if args.Key == Key.Enter:
            last_line = self.get_last_line()
            if last_line == '':
                self.write_line(None)
                return
            output = self.evaluate(last_line)
            self.append_history(last_line)
            self.history_index = 0
            self.write_line(output)

    def evaluate(self, line):

        try:
            output = eval(line, self.stack_globals, self.stack_locals)
        except SyntaxError as errmsg:
            exec(line, self.stack_globals, self.stack_locals)
            return
        except Exception as errmsg:
            output = errmsg
        return str(output)

    def OnKeyDownHandler(self, sender, args):
        pass

    def KeyPressPreview(self, sender, e):
        e.Handled = False
        if e.Key == Key.Up:
            self.history_up()
            e.Handled = True
        if e.Key == Key.Down:
            self.history_down()
            e.Handled = True
        if e.Key == Key.Left or e.Key == Key.Back:
            if self.ui.tbox.CaretIndex == self.tbox.Text.rfind(Console.CARET) + len(Console.CARET):
                e.Handled = True
        if e.Key == Key.Home:
            self.tbox.CaretIndex = self.tbox.Text.rfind(Console.CARET) + len(Console.CARET)
            e.Handled = True
        if e.Key == Key.Tab:
            self.autocomplete()
            e.Handled = True

    def autocomplete(self):
        # TODO: Add recursive dir() attribute suggestions
        last_line = self.get_last_line()
        cursor_line_index = self.tbox.CaretIndex - self.tbox.Text.rfind(Console.CARET) - len(Console.CARET)
        text = last_line[0:cursor_line_index]
        possibilities = set(self.stack_locals.keys() + self.stack_globals.keys()) # + self.get_all_history()
        suggestions = [p for p in possibilities if p.lower().startswith(text.lower())]
        logger.debug('Text: {}'.format(text))
        logger.debug('Sug: {}'.format(suggestions))

        if not suggestions:
            return None
        # Create Dictionary to Track iteration over suggestion
        index = self.ac_options[text]
        try:
            suggestion = suggestions[index]
        except IndexError:
            self.ac_options[text] = 0
            suggestion = suggestions[0]
        self.ac_options[text] += 1

        if suggestion is not None:
            caret_index = self.tbox.CaretIndex
            self.write_text(suggestion)
            self.tbox.CaretIndex = caret_index

    def write_line(self, line=None):
        if line:
            self.tbox.AppendText(line)
            self.tbox.AppendText(NewLine)
        self.tbox.AppendText(Console.CARET)

    def write_text(self, line):
        last_new_line = self.tbox.Text.rfind(Console.CARET)
        self.tbox.Text = self.tbox.Text[0:last_new_line]
        self.tbox.AppendText(Console.CARET)
        self.tbox.AppendText(line)
        self.ui.tbox.CaretIndex = len(self.ui.tbox.Text)

    def get_all_history(self):
        """ Retrieves all lines from history file """
        with open(self.history_file) as fp:
            lines = [l for l in fp.read().split('\n') if l != '']
            return lines

    def history_up(self):
        self.history_index += 1
        line = self.history_iter()
        if line is not None:
            self.write_text(line)

    def history_down(self):
        self.history_index -= 1
        line = self.history_iter()
        if line is not None:
            self.write_text(line)

    def append_history(self, line):
        logger.debug('Adding Line to History:' + repr(line))
        with open(self.history_file, 'a') as fp:
            fp.write(line + '\n')

    def history_iter(self):
        lines = self.get_all_history()
        logger.debug('Lines: {}'.format(lines))
        try:
            line = lines[::-1][self.history_index -1]
        except IndexError:
            if len(lines) == 0:
                return None
            if len(lines) < 0:
                self.history_index += len(lines)
            if len(lines) > 0:
                self.history_index -= len(lines)
            line = lines[0]
        return line


if __name__ == '__main__':
    def test():
        Console()
    test()
