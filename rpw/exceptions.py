from rpw.logger import logger


class RPW_Exception(Exception):
    """ Revit Python Wrapper Base Exception """


class RPW_TypeError(RPW_Exception, TypeError):
    """ Revit Python Wrapper Base Exception """
    def __init__(self, type_expected, type_received):
        logger.error('expected [{}], got [{}]'.format(type_expected,
                                                      type_received))

class RPW_ParameterNotFound(RPW_Exception, KeyError):
    """ Revit Python Wrapper Base Exception """
    def __init__(self, element, param_name):
        logger.error('Parameter Not Found: [{}]:[{}]'.format(element,
                                                             param_name))

class RPW_WrongStorageType(RPW_Exception, TypeError):
    """ Wrong Storage Type """
    def __init__(self, storage_type, value):
        logger.error('Wrong Storage Type: [{}]:[{}:{}]'.format(storage_type,
                                                               type(value),
                                                               value
                                                               ))
