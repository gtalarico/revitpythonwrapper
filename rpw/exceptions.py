from rpw.logger import logger


class RPW_Exception(Exception):
    """ Revit Python Wrapper Base Exception """


class RPW_ParameterNotFound(KeyError):
    """ Revit Python Wrapper Base Exception """
    def __init__(self, element, param_name):
        logger.error('Parameter Not Found: [{}]:[{}]'.format(element,
                                                            param_name))


class RPW_WrongStorageType(TypeError):
    """ Wrong Storage Type """
    def __init__(self, storage_type, value):
        logger.error('Wrong Storage Type: [{}]:[{}:{}]'.format(storage_type,
                                                               type(value),
                                                               value
                                                               ))
