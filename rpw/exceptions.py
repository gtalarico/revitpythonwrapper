from rpw.logger import logger


class RPWException(Exception):
    """ Revit Python Wrapper Base Exception """

class RPW_WrongStorageType(TypeError):
    """ Wrong Storage Type """
    def __init__(self, storage_type, value):
        logger.error('Wrong Storage Type: [{}]:[{}:{}]'.format(storage_type,
                                                               type(value),
                                                               value
                                                               ))
