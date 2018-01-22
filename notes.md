# Release Notes

### 1.7.4
* Fixed os_forms.select_file(multiple=True) - Issue #35
* Fixed Autodesk.Revit.Exceptions import when running rpw from ipy console (ig. run_tests.bat)


### 1.7.3
* Added Get by Index to Selection (issues #32)
* Converted ElementSet internal storage to list instead of set to allow ordered sequence
* Fixed Revit Exceptions Import Docs
* Fixed Transaction Status Doc

### 1.7.2
* Fixed: Collector.get_element_ids() Typo
* Fix: XYZ can now take regular DB.XYZ
* Fix: ElementSet.__getitem__
* Fix: Rebuilt internals of ElementSet to be a set() instead of dict
* Feature: Deprecated methods to collections
* Feature: .unwrap to to_element (unwraps if wrapped)
* Fixed: Element.from_list

### 1.7.1
* Fix: Autodesk.Revit.Exceptions Circular Import (Dynamo)
* Fix: + Docs Fixes
* Feature: Added Category Mixin to Element()

### 1.7.0
* Feature: Added Collector Exclusion Filter
* Feature: Added Collector UnionWith
* Feature: Added Collector IntersectWith
* Feature: Add Autodesk.Revit.Exceptions module to rpw.revit namespace for easier access
* Feature: Added get_assembly() method to element
* Docs: Reorganized Entire Doc Structure to nest and group by module.
* Fixed: re-enabled TaskDialog Tests
* Fixed: Lot's of Doc Fixes
* Improvement: Optimized db.Element() class discovery for explicit constructor
* Improvement: Handle Pick exception
* Improvement: Remove inspect.getmro check for element wrapping - was :wqnot needed
* Improvement: Added Raise for double wrapping element
* Cleanup: Renamed `Categoy._builtin_enum` to `Category.builtin`. (Depracated Warning)
* Cleanup: New Category Mixin with
* Cleanup: Moved Category into its own file
* Cleanup: Delete Family.Name and FamilySymbol.Name Replaced by Element.name
* Cleanup: Moved in_assembly and get_assembly to FamilyInstance
* Feature/Cleanup: Add get_attribute(wrapped) + deprecate warning to several attributes:
  including: FamilyInstance, FamilySymbol, Family, and Category.
  Attributes like FamilyInstance.symbol should now be accessed using FamilyInstance.get_symbol()
  These are being added in preparation to 2.0.0


### 1.6.0
* Added TaskDialog, Tests, Docs
* Revised Alert
* Added Element.name getter and setter (PR#30)
* Fixed: Console Traceback Printing. Now shows full exception
* Fixed: BaseObject repr

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
