""" Standard IO Dialogs

"""
# TODO: Merge with Forms ?

import clr

clr.AddReferenceByPartialName('System.Windows.Forms')
from System.Windows import Forms

def select_folder():
    """ Selects a Folder Path using the standard OS Dialog

    >>> folderpath = select_folder()
    'C:\\folder\\path'

    """

    form = Forms.FolderBrowserDialog()
    if form.ShowDialog() == Forms.DialogResult.OK:
        return form.SelectedPath


def select_file(file_ext='*', multi_file=False):
    """ Selects a File Path using the standard OS Dialog

    >>> filepath = select_file('rvt')
    'C:\\folder\\file.rvt'

    """
    form = Forms.OpenFileDialog()
    form.Filter = '|*.{}'.format(file_ext)
    form.RestoreDirectory = True
    form.Multiselect = multi_file
    if form.ShowDialog() == Forms.DialogResult.OK:
        return form.FileName


if __name__ == '__main__':
    select_folder()
    select_file()
