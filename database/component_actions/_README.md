# This is a guide explaining the contents of action files.

Action files contain information about an action that can be 
performed via a Facile API.

Each action file has the following attributes:

- **name**: The name of the action such as "click". This does
  not have to be the same as the file name, but should be similar.
  
- **description**: A *brief* comment about what the action does
  and how the action is performed as well as any side effects.
  
- **targets**: A list of friendly class names that this action can
  be performed on (see [Friendly Class Names](#friendly-class-names)).
  - If the list is empty, the action specification will not be bound to
  any component type.
  - If the list contains *all*, the action can be performed
  on any component type.
  
- **inputs**: A list of inputs to the action. The inputs will follow
  the [port format](#port-format).
  
- **outputs**: A list of outputs to the action. The outputs will
  follow the [port format](#port-format)
  
- **code**: The code that will be run to perform the action. See 
  the [code format](#code-format) for more information.
  

## Friendly Class Names

The following names can be used as valid targets for the action.
Depending on the backend used for the project (either **win32** 
or **uia**), different actions may be available. Because of this,
action specifications should list all viable targets from all
of the 3 lists below.

UIA types:
- Button
- ComboBox
- Edit
- HeaderItem
- Header
- ListItem
- ListView
- MenuItem
- Menu
- Slider
- Static
- TabControl
- Toolbar
- Tooltip
- TreeItem
- TreeView

Win32 types:
- Button
- ComboBox
- Edit
- ListBox
- PopupMenu
- Static

Common types:
- _toolbar_button
- _treeview_element
- _listview_item
- Animation
- Calendar
- ComboBox
- DateTimePicker
- Header
- Hotkey
- IPAddress
- ListView
- Pager
- Progress
- ReBar
- StatusBar
- TabControl
- ToolTip
- ToolTips (not fully implemented)
- Toolbar
- Trackbar
- TreeView
- UpDown

NOTE: Other types may exist that are not listed. If you would
like to control a component from the target GUI model, but don't
know what type it is, click on it and look in the property editor.


## Port Format

Inputs and outputs to the action will be specified as ports. 
Each port has:
- **name**: A valid python variable name.
- **datatype**: a valid python type (str, int, float, etc.).

Input ports also have the following:
- **optional**: a boolean value specifying whether the input 
  is optional or not.
- **default**: Only needed if the the input is optional.

## Code Format

The code provided for the action needs to be valid python code.
This code will be inserted into a method after some environment-initialization 
code is run. The code can use any of the following environment variables:

- **self.app**: is the pywinauto application instance attached to the
  currently running application
- **comp**: is the pywinauto wrapper object for the component that is to be
  interacted with.

The code may also use any inputs specified for this action. To use inputs,
simply access the input name as a python variable.

**IMPORTANT:** the code MUST define all of the outputs and return them as a
tuple in the order specified in the *outputs* field of the action specification.
This may not be enforced, but usage of an action that does not obey this rule
will almost certainly bare unintended consequences.




