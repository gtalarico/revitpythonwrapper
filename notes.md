# Release Notes

### 1.5.0
* Added wrapped kwarg to Reference.get_element()

### 1.4.2
* Converted all Pick class methods to Class Methods
* Picker and References now work with Linked Elements

### 1.4.1
* Addded Rhino3dmIO binary and examples
* Renamed parameters `to_json` to `to_dict`

### 1.4.0
* Added Element.type property
* Added in_assembly() to Element
* Added ParameterSet.get_value() for fail safe dictionary-style access
* Started ParameterSet and Parameter: to_json()
* Fixed RpwParameterNotFound exception message
* Added API Notes on Family/Symbol/Instance
* Added bool() evaluation to Parameter

### 1.3.1
* Improved Category Lookup for instance and wall wrappers
* Fixed Element() doc initialization
* Added XYZ.rotate()
* Added db.Element.from_list() factory
* Added db.Parameter.value_string


### 1.3.0
* Removed Terminate button from Console
* Curve: New Line Class
* Curve: New Line Curve
* Curve: New Line Ellipse
* Curve: New Line Circle
* Curve: New Line Arc
* Curve: New Line Transform, Transform.rotate_vector
* Curve : Started Test Suite
* XYZ: Improved Instantiation methods
* XYZ: Added __mul__, __add__, __sub__
* XYZ: Full test suite
* XYZ: Fixed XYZ __eq__ method

### 1.2.2
* Fixes For pyRevit Zero State Doc

### 1.2.1
* New Wall.change_type method
* New Console Tab autocompletion (works for dotted members)
* Added Terminate button to Console
* Pep8 Fixes (Line Max=100)
* But Fixes
* Moved FamilyInstance and related from element.py to family.py
* Improved Element.__new__ by adding db.__all__

### 1.2.0
* New View Wrappers
* New OverrideGraphicSettings Wrapper by Element and Category
* Complete View Tests
* New Pattern Wrappers (ElementPattern and FillPattern)
* Add to_category_id coerce
* Added fuzzy_get docs
* Bug: Quick Form Title
* Bug: Builtins Repr print bug

### 1.1.2
* New default option for ComboBox, CheckBox, and TextBox
* Added docs for FlexForm Controls Init
* Added docs for on_click
* Added XYZ comparison method
* New Tests for all Collections classes
* New Tests for FlexForm

### 1.1.1
* New Reference Wrappers
* Separated Pick() class
* Docs

### 1.1.0
* Bug Fixes
* New View Wrappers
* Renamed Classes
  * Instance > FamilyInstance
  * Symbol > FamilySymbol
  * WallInstance > Wall
  * WallSymbol > WallType
  * WallFamily > WallKind

### 1.0.1
* Bug Fixes
* Dynamo Compatibility Fixed

### 1.0.0
* Major Refactoring
* New Folder Structure
* New Collector
* New Element Constructor
* Collections
* New Revit Class Wrapper
* New FlexForms
* Console

### 0.0.9
* Foundation
* Wrapper Data Model
* Elements, Base, Collector, Selection, Transaction, Forms, Builtins
* Documentation
* New View Wrappers
* Fixed Quick Form Title
* Fixed Quick Form Title


### 1.1.2
* New default option for ComboBox, CheckBox, and TextBox
* Added docs for FlexForm Controls Init
* Added docs for on_click
* Added XYZ comparison method
* New Tests for all Collections classes
* New Tests for FlexForm

### 1.1.1
* New Reference Wrappers
* Separated Pick() class
* Docs

### 1.1.0
* Bug Fixes
* New View Wrappers
* Renamed Classes
  * Instance > FamilyInstance
  * Symbol > FamilySymbol
  * WallInstance > Wall
  * WallSymbol > WallType
  * WallFamily > WallKind

### 1.0.1
* Bug Fixes
* Dynamo Compatibility Fixed

### 1.0.0
* Major Refactoring
* New Folder Structure
* New Collector
* New Element Constructor
* Collections
* New Revit Class Wrapper
* New FlexForms
* Console

### 0.0.9
* Foundation
* Wrapper Data Model
* Elements, Base, Collector, Selection, Transaction, Forms, Builtins
* Documentation
