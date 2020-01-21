************
Introduction
************

The purpose of this document is to describe in detail the architecture and design of the Facile
software system. This document goes over Facile's state machine, data structures, algorithms, and
detailed source code documentation. As you're reading this document, keep in mind that it is
meant to be viewed in a more interactive manner as an HTML document. The PDF is only created for
the purpose of this course.

*************
State Machine
*************

Facile's state machine is growing as we develop Facile. Currently, it only shows the side of
Facile that deals with building the model of the target GUI, but eventually it will show building
the model of the API and compiling the API. The state machine is shown in :num:`Fig. #statemachine`.

.. _StateMachine:

.. figure:: ../images/StateMachine.png
    :alt: Facile's state machine.

    Facile's state machine.