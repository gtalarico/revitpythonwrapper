""" Python Wrapper For the Revit API """


class DynamoUtils(object):
    # Coerce/Wrap/Unwrap
    # Create object that can act as both?
    pass


class Selection(object):
    """ Revit uidoc.Selection Wrapper """
    # Get Selection
    # Get Selection Element
    # Filter selection with argument
    # Apply Pick
    pass


class BoundingBox(object):
    """ Revit BoundingBox Wrapper """
    # GetCenter
    # FromObject()
    pass


class FamilyInstance(object):
    """ Generic Family Instance Wrapper """
    # Get Type
    # Get Symbol
    # Get Elements
    # @transaction(name)
    def move(self, translation):
        pass


class FamilyType(object):
    """ Generic Family Instance Wrapper """
    # Get Type
    # Get Symbol
    # Get Elements


class UI(object):
  pass


class Doc(object):
  pass
