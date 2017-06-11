import clr
clr.AddReference('System')
from System.Diagnostics import Process

from rpw.utils.logger import logger
from rpw.base import BaseObject


class Revit(BaseObject):
    """Revit Application Wrapper """

    class HOSTS():
        RPS = 'RPS'
        DYNAMO = 'Dynamo'

    def __init__(self):
        try:
            self.uiapp = __revit__
            self.host = Revit.HOSTS.RPS
        except NameError:
            try:
                self.uiapp = self.find_dynamo_uiapp()
            except Exception as errmsg:
                logger.error(errmsg)
                raise Exception('A Revit Application handle could not be found')
        clr.AddReference('RevitAPI')
        clr.AddReference('RevitAPIUI')


    def find_dynamo_uiapp(self):
        clr.AddReference("RevitServices")
        import RevitServices
        from RevitServices.Persistence import DocumentManager

        self.host = Revit.HOSTS.DYNAMO
        import sys
        sys.path.append(r'C:\Program Files (x86)\IronPython 2.7\Lib')
        return DocumentManager.Instance.CurrentUIApplication

    @property
    def doc(self):
        return self.uiapp.ActiveUIDocument.Document

    @property
    def uidoc(self):
        return self.uiapp.ActiveUIDocument

    @property
    def active_view(self):
        return self.uidoc.ActiveView

    @active_view.setter
    def active_view(self, view_reference):
        self.uidoc.ActiveView = view_reference

    @property
    def app(self):
        return self.uiapp.Application

    @property
    def docs(self):
        return self.app.Application.Documents

    @property
    def username(self):
        return self.uiapp.Application.Username

    @property
    def version(self):
        return RevitVersion(self.uiapp)

    @property
    def process(self):
        return Process.GetCurrentProcess()

    @property
    def process_id(self):
        return Process.GetCurrentProcess().Id

    @property
    def process_name(self):
        return Process.GetCurrentProcess().ProcessName

    def __repr__(self):
        return '<{version} [{process}:{pid}] >'.format(version=self.version,
                                                       process=self.process_name,
                                                       pid=self.process_id)

    # @property
    # def proc_screen(self):
    #     clr.AddReferenceByPartialName('System.Windows.Forms')
    #     # noinspection PyUnresolvedReferences
    #     from System.Windows.Forms import Screen
    #     return Screen.FromHandle(Process.GetCurrentProcess().MainWindowHandle)
    #
    # def is_newer_than(self, version):
    #     return int(self.version) > int(version)
    #
    # def is_older_than(self, version):
    #     return int(self.version) < int(version)

class RevitVersion():
    def __init__(self, uiapp):
        self.uiapp = uiapp

    @property
    def year(self):
        return self.uiapp.Application.VersionNumber

    @property
    def name(self):
        return self.uiapp.Application.VersionName

    @property
    def build(self):
        return self.uiapp.Application.VersionBuild

    def __lt__(self):
        """ Handle Version Comparison Logic"""
        raise NotImplemented

    def __repr__(self):
        return '<Version: {year}: {build}>'.format(year=self.name,
                                                   build=self.build)
    def __str__(self):
        return '{name}:{build}'.format(name=self.name, build=self.build)

revit = Revit()
from Autodesk.Revit import DB, UI
