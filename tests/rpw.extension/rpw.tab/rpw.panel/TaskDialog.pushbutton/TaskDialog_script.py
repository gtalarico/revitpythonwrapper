""" Revit Python Wrapper Tests - Forms

Passes:
2017

"""

import sys
import unittest
import os

test_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(test_dir)
sys.path.append(root_dir)

import rpw
from rpw import revit, DB, UI
doc, uidoc = rpw.revit.doc, rpw.revit.uidoc

from rpw.ui.forms.taskdialog import TaskDialog, CommandLink, Alert
from rpw.exceptions import RpwParameterNotFound, RpwWrongStorageType
from rpw.utils.logger import logger

######################
# Task Dialog
######################


class TaskDialogTests(unittest.TestCase):

    def test_basic(self):
        commands = [CommandLink('Select This Option', return_value='XXX',
                                subtext='Subtext 1'),
                    CommandLink('Option 2 - Should see subtext',
                                subtext='Subtext 2')
                    ]

        dialog = TaskDialog('Test 1 - Full',
                            title='My Title - Footer is ON. No Close Btn',
                            content='X Close IS SHOWING',
                            footer='Foot Text',
                            verification_text='Check This',
                            show_close=True,
                            commands=commands)
        result = dialog.show()
        self.assertEqual(result, 'XXX')
        self.assertEqual(dialog.Title, 'My Title - Footer is ON. No Close Btn')
        self.assertEqual(dialog.MainInstruction, 'Test 1 - Full')
        self.assertEqual(dialog.MainContent, 'X Close IS SHOWING')
        self.assertEqual(dialog.FooterText, 'Foot Text')
        self.assertEqual(dialog.verification_checked, True)

    def test_func_return_value(self):
            commands = [CommandLink('Select This Option',
                            return_value=lambda: 'ZZZ',
                            subtext='Subtext 1'),
                        CommandLink('Option 2', subtext='Subtext 2')
                        ]
            dialog = TaskDialog('Test 2 - Simple',
                                verification_text='Leave this off',
                                commands=commands,
                                content='X Close Should NOT be Showing',
                                show_close=False)
            result = dialog.show()
            self.assertEqual(result(), 'ZZZ')
            self.assertEqual(dialog.verification_checked, False)

    def test_func_defaultvalue_button(self):
            commands = [CommandLink('Press This Button')]
            dialog = TaskDialog('Test 3',
                                content='Press Button Below',
                                commands=commands,
                                buttons=['Cancel'])
            result = dialog.show()
            self.assertEqual(result, 'Press This Button')
            self.assertEqual(dialog.verification_checked, None)

    def test_func_all_buttons_retry(self):
            dialog = TaskDialog('Test 4',
                                content='Press Retry',
                                buttons=['Ok', 'Yes', 'No',
                                         'Cancel', 'Retry', 'Close'])
            result = dialog.show()
            self.assertEqual(result, 'Retry')

    def test_func_all_buttons_close(self):
            dialog = TaskDialog('Test 5',
                                content='Press Close',
                                buttons=['Ok', 'Yes', 'No',
                                         'Cancel', 'Retry', 'Close'])
            result = dialog.show()
            self.assertEqual(result, 'Close')

    def test_func_all_buttons_cancel(self):
            dialog = TaskDialog('Test 6',
                                content='Press Cancel',
                                buttons=['Ok', 'Yes', 'No',
                                         'Cancel', 'Retry', 'Close'])
            result = dialog.show()
            self.assertEqual(result, None)

    def test_close(self):
            dialog = TaskDialog('Test 7 - Exit',
                                content="Close Using X",
                                buttons=[],
                                show_close=True)
            with self.assertRaises(SystemExit):
                result = dialog.show(exit=True)

    def test_close_cancel(self):
            dialog = TaskDialog('Test 8 - Exit',
                                content="Close Using Cancel",
                                buttons=['Cancel'],
                                show_close=False)
            with self.assertRaises(SystemExit):
                result = dialog.show(exit=True)


    # def test_close_for_docs(self):
    #         commands= [CommandLink('Open Dialog', return_value='Open'),
    #                    CommandLink('Command', return_value=lambda: True)]

    #         dialog = TaskDialog('This TaskDialog has Buttons ',
    #                             title_prefix=False,
    #                             content="Further Instructions",
    #                             commands=commands,
    #                             buttons=['Cancel', 'OK', 'RETRY'],
    #                             footer='It has a footer',
    #                             # verification_text='And Verification Text',
    #                             # expanded_content='And Expanded Content',
    #                             show_close=True)
    #         dialog.show()

class AlertTests(unittest.TestCase):

    def test_alert(self):
        alert = Alert('my message - press close',
                      title='My Title',
                      header='My Header',
                      exit=False)
        self.assertIsInstance(alert, Alert)
        self.assertIsInstance(alert.result, UI.TaskDialogResult)


    def test_alert_exit_on_close(self):
        with self.assertRaises(SystemExit):
            Alert('my message - press close - will exit',
                   title='My Title',
                   header='My Header',
                   exit=True)




def run():
    # logger.verbose(False)
    unittest.main(verbosity=3, buffer=True)

if __name__ == '__main__':
    run()
