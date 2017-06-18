from collections import defaultdict
from forms import *


class Console(Window):
    """ REPL Console for Inspecting Stack

    >>> from rpw.forms import Console
    >>> Console()

    """
    LAYOUT = """
                <Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                        Title="DeployWindow" Height="400" Width="800" SnapsToDevicePixels="True"
                        UseLayoutRounding="True" WindowState="Normal" WindowStartupLocation="CenterScreen">
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
                         AcceptsReturn="True" VerticalScrollBarVisibility="Auto" />
                </Grid>
                </Window>
    """
    # <Button Grid.Column="1" Content="Deploy" Height="30" Width="100" HorizontalAlignment="Left" Margin="10,10,10,10" Name="deployButton" Cursor="Hand" />

    CARET = '>>> '

    def __init__(self):

        import inspect
        import os
        import tempfile
        import pickle

        tempdir = tempfile.gettempdir()
        filename = 'rpw-history'
        self.history_file = os.path.join(tempdir, filename)

        stack_tuple = inspect.stack()[2] # Finds Calling Stack

        # TODO: Print Stack Info on Init
        stack_filename = stack_tuple[1]
        stack_line = stack_tuple[2]
        stack_name = stack_tuple[3]

        stack = stack_tuple[0]
        stack_locals = stack.f_locals
        stack_globals = stack.f_globals

        # print('Local vars: ' + str(stack_locals))
        # print('Global vars: ' + str(stack_globals))

        self.stack_locals = stack_locals
        self.stack_globals = stack_globals

        self.ui = wpf.LoadComponent(self, StringReader(Console.LAYOUT))
        self.ui.Title = 'RevitPythonWrapper Console'

        self.ui.tbox.Text = Console.CARET
        self.ui.tbox.Focus()
        self.ui.tbox.CaretIndex = len(Console.CARET)

        # self.tbox.FontFamily = FontFamily("Consolas")

        self.PreviewKeyDown += self.KeyPressPreview
        self.history_index = 0
        self.ac_options = defaultdict(int)
        self.ac_index = 0

        self.ShowDialog()

    def get_line(self, index):
        line = self.tbox.GetLineText(index).replace('\r\n','')
        if line.startswith(Console.CARET):
            line = line[len(Console.CARET):]
        # print('Get Line: {}'.format(line))
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
        # print('Lines: {}'.format(lines))
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
        # print('Stack: ' + str(self.stack_vars))
        try:
            output = eval(line, self.stack_globals, self.stack_locals)
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
        print('Text: {}'.format(text))
        possibilities = set(self.stack_locals.keys() + self.stack_globals.keys()) # + self.get_all_history()
        suggestions = [p for p in possibilities if p.lower().startswith(text.lower())]
        print('Sug: {}'.format(suggestions))

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
        print('Adding Line to History:' + repr(line))
        with open(self.history_file, 'a') as fp:
            fp.write(line + '\n')

    def history_iter(self):
        lines = self.get_all_history()
            # print('Lines: {}'.format(lines))
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
