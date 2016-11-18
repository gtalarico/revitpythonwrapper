from rpw.utils.logger import logger

class RPW_Exception(Exception):
    """ Revit Python Wrapper Base Exception """


class RPW_TypeError(TypeError):
    """ Revit Python Wrapper Base Exception """
    def __init__(self, type_expected, type_received=None):
        type_received = type_received or 'not reported'
        msg = 'expected [{}], got [{}]'.format(type_expected, type_received)
        super(RPW_TypeError, self).__init__(msg)


class RPW_ParameterNotFound(RPW_Exception, KeyError):
    """ Revit Python Wrapper Base Exception """
    def __init__(self, element, param_name):
        msg = 'parameter not found [element:{}]:[param_name:{}]'.format(element, param_name)
        super(RPW_ParameterNotFound, self).__init__(msg)


class RPW_WrongStorageType(RPW_Exception, TypeError):
    """ Wrong Storage Type """
    def __init__(self, storage_type, value):
        msg = 'Wrong Storage Type: [{}]:[{}:{}]'.format(storage_type,
                                                        type(value), value)
        super(RPW_WrongStorageType, self).__init__(msg)
