""" Template Form """  #

from rpw.ui.forms.resources import *
from rpw.ui.forms.template import TemplateForm

class DataGrid(TemplateForm):
    layout = """
            <Window

                    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
                    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
                    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
                    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
                    xmlns:local="clr-namespace:WpfApplication1"
                    mc:Ignorable="d"
                    Title="MainWindow" Height="350" Width="525">
                <Grid>
                    <DataGrid x:Name="dataGrid" VerticalAlignment="Top"
                                                Height="277" Margin="0,10,10,0"
                                                HorizontalAlignment="Right"
                                                Width="497"/>

                </Grid>
            </Window>
        """
    def __init__(self, title):
        super(DataGrid, self).__init__(title, DataGrid.layout)
        # print(self.ui.dataGrid)

        table = DataTable()
        data = ['John', 'Gui']

        column = DataColumn()
        column.DataType = System.Type.GetType("System.Int32")
        column.ColumnName = "id"
        table.Columns.Add(column)
        column = DataColumn()
        column.DataType = System.Type.GetType("System.String")
        column.ColumnName = "item"
        table.Columns.Add(column)

        for n, value in enumerate(data):
            row = table.NewRow()
            row["id"] = n
            row["item"] = value
            table.Rows.Add(row)

        view = DataView(table)
        self.ui.dataGrid.ItemsSource = view

if __name__ == '__main__':
    """ TESTS """

    from rpw.ui.forms import DataGrid; f = DataGrid('Test'); f.show()
    form = TemplateForm('Title', components)
    form.show()

