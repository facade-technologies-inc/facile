**********
Algorithms
**********

This section describes the critical algorithms of Facile. The four primary algorithms used are:

- Token Comparison Algorithm
- Observer Algorithm
- Explorer Algorithm
- Component Placement Algorithm

These algorithms are discussed in detail in the following sections.

--------------------------
Token Comparison Algorithm
--------------------------

.. todo:: Fill out this part

------------------
Observer Algorithm
------------------

The Observer is the part of Facile that looks at the target application and reports all visible
parts of it, along with any new views or windows that are opened. In order to achieve this
functionality, the observer is driven by the following behavior:

- The observer must first connect to the target application using its Process ID.
- While the application is open, the following occurs:

    - Handles to all visible windows are stored as (window, *None*) tuples (or couples) in a list
      of components to
      analyze, as the list will later be filled with (component, parentSuperToken) tuples as well.
    - Then, as long as there is at least one element in that list:

        - The last element of the list, which is a tuple, is removed and stored in order to be
          analyzed. The first part of the tuple is the handle to a component, for which a Token
          is immediately created, and the second is a reference to the component's parent's
          SuperToken.
        - The algorithm then checks whether a SuperToken already exists for the newly created
          token. To do this, the token comparison algorithm is used to determine if the new token
          and any of its parents' children's SuperTokens have an exact, close, or no match.
        - If there is an exact match, the algorithm takes no action and continues, since the new
          token already exists in a SuperToken.
        - If there is no match, a new SuperToken is created with the new token, and a signal is
          emitted to the Target GUI Model for it to be updated as well.
        - If there is a close match, the token is added to the resembling SuperToken's token
          list, and the algorithm then continues.
        - Handles to the current component's children are then added as (child,
          currentComponentSuperToken) to the list of components to be analyzed.

------------------
Explorer Algorithm
------------------

The Explorer is the part of Facile that interacts with the target application on its own, in an
attempt to display as many parts of the target application as possible. In order to achieve this
functionality, the explorer is driven by the following behavior:

- The explorer must first connect to the target application using its Process ID.
- While the application is open, the following occurs:

    - Handles to all visible windows are stored in a list of components to be interacted with.
    - Then, as long as there is at least one element in that list:

        - The last element of the list is removed and stored (as the current component) in order
          to be interacted with.
        - The current component's children are first added to the list.
        - If the current component is a textfield, the explorer pauses and asks the user to enter
          any necessary information (useful for login/credential cases), after which the user
          confirms the text and allows the explorer to continue.
        - If the current component is clickable, such as a button or menu item, then the explorer
          clicks on it, as long as it is not a "Cancel" button.

-----------------------------
Component Placement Algorithm
-----------------------------

Component Placement in Facile's target GUI view is crucial in order to get a visually recognizable result. Because
Facile wants every component to be selectable, margins must be made around every component, and any collisions between
sibling components must be resolved. In order to do this, Facile uses the following methods:

- If a component has no parent, it is not displayed, because it represents a scene: the
  environment in which the application is running.
- If a component's parent has no parent, it means the component is a top level window. Once
  detected, these components are set to be movable, that way they can move around the scene.
  Additionally, they do not need any margins since no visible component surrounds them, but a
  titlebar is added in order to display information about the component and to allow for better
  selectability.
- Otherwise, components are shrunk by a specific amount in order to have margins around them, and
  a titlebar is added once again. Once this is done, collision resolution takes place:

    - When two components collide, they are overlapping, and this overlap must be mitigated in
      order to obtain a better and more realistic-looking final result. In order to do  this, there
      are four cases considered.

        .. note:: We define a component's placement by its top-left corner

        1. If component 2 is between 45 and 0 degrees from component 1, then component 2 is
           pushed to the right until there is no longer an overlap with component 1.
        #. If component 2 is between 0 and -90 degrees from component 1, then component 2 is
           pushed radially away from component 1 until there is no longer an overlap with
           component 1.
        #. If component 2 is between -90 and -135 degrees from component 1, then component 2 is
           pushed  down until there is no longer an overlap with component 1.
        #. Otherwise, component 2 'wins' and the same rules are applied, but with component 1
           relative to component 2.






































