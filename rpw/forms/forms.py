# TODO: Clean up + handle imports

import sys
sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')

import os
# Remove these depenencies?
cwd = os.path.dirname(__file__)
sys.path.append(cwd)

import clr
# clr.AddReference('PresentationCore')
clr.AddReference("PresentationFramework")
clr.AddReference('IronPython.Wpf')

try:
    from System.Windows import Application, Window
    import wpf
except ImportError:
    from ..sphinx_compat import *


class SelectFromList(Window):
    """
    Simple WPF form with ComboBox dropdown.

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
    """
    def __init__(self, title, options, description=None):
        self.selected = None
        self.ui = wpf.LoadComponent(self, os.path.join(cwd, 'form_select_list.xaml'))
        self.ui.Title = title

        if description is not None:
            self.ui.selection_label.Content = description
        self.ui.button_select.Click += self.select_click

        self.ui.combo_data.Items.Clear()
        self.ui.combo_data.ItemsSource = options
        self.ui.combo_data.SelectedItem = options[0]

    def combo_SelectionChanged(self, sender, e):
        self.selected = self.ui.combo_data.SelectedItem

    def select_click(self, sender, e):
        self.DialogResult = True
        self.Close()

    def show(self):
        return super(SelectFromList, self).ShowDialog()
