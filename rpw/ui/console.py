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
                         Name="text_box" Margin="6,6,6,6" VerticalAlignment="Stretch"
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

        stack_tuple = inspect.stack()[2]

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
        self.ui.Title = 'RevitPythonWrapper Stack Debugger'

        self.ui.text_box.Text = Console.CARET
        self.ui.text_box.Focus()
        self.ui.text_box.CaretIndex = len(Console.CARET)

        self.PreviewKeyDown += self.KeyPressPreview

        self.history_index = 0

        self.ShowDialog()

    def OnKeyUpHandler(self, sender, args):
        if args.Key == Key.Enter:
            line_count = sender.LineCount
            last_line = line_count - 1
            line = sender.GetLineText(last_line - 1)[4:-1]
            # print('Line:{}'.format(repr(line)))
            if line == '\r':
                self.write_line(None)
                return

            output = self.evaluate(line)
            self.append_history(line)
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
            if self.ui.text_box.CaretIndex == self.text_box.Text.rfind(Console.CARET) + len(Console.CARET):
                e.Handled = True
        if e.Key == Key.Tab:
            # TODO: Tab Completion
            raise NotImplemented

    def write_line(self, line=None):
        if line:
            self.text_box.AppendText(line)
            self.text_box.AppendText(NewLine)
        self.text_box.AppendText(Console.CARET)

    def history_set(self, line):
        last_new_line = self.text_box.Text.rfind(Console.CARET)
        self.text_box.Text = self.text_box.Text[0:last_new_line]
        self.text_box.AppendText(Console.CARET)
        self.text_box.AppendText(line)
        self.ui.text_box.CaretIndex = len(self.ui.text_box.Text)

    def history_up(self):
        self.history_index += 1
        line = self.read_history()
        if line is not None:
            self.history_set(line)

    def history_down(self):
        self.history_index -= 1
        line = self.read_history()
        if line is not None:
            self.history_set(line)

    def append_history(self, line):
        with open(self.history_file, 'a') as fp:
            fp.write(line)

    def read_history(self):
        with open(self.history_file) as fp:
            lines = fp.read().split()
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
