import clr
import os

# Verify these are needed.
clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference("System.Windows.Forms")

#  Windows Forms Elements
from System.Drawing import Point, Icon, Color
from System.Windows import Forms
from System.Windows.Forms import Application, Form
from System.Windows.Forms import DialogResult, GroupBox, FormBorderStyle
from System.Windows.Forms import ComboBox, Button, DialogResult


class SelectFromList(Form):

    """
    form = SelectFromList(floor_types.keys())
    form.ShowDialog()

    if form.DialogResult == DialogResult.OK:
        chosen_type_name = form.selected

    """

    def __init__(self, options):

        #  Window Settings
        self.Text = 'Select View Type'
        self.MinimizeBox = False
        self.MaximizeBox = False
        self.BackgroundColor = Color.White
        self.FormBorderStyle = FormBorderStyle.FixedSingle
        self.ShowIcon = False

        combobox = ComboBox()
        combobox.Width = 200
        combobox.Height = 20
        combobox.DataSource = options
        self.combobox = combobox

        button = Button()
        button.Text = 'Select'
        button.Location = Point(0,20)
        button.Width = combobox.Width
        button.Height = 20
        button.Click += self.button_click

        self.Width = combobox.Width + 16
        self.Height = 80

        self.Controls.Add(combobox)
        self.Controls.Add(button)

    def button_click(self, sender, event):
        self.selected = self.combobox.SelectedValue
        self.DialogResult = DialogResult.OK
        self.Close()
