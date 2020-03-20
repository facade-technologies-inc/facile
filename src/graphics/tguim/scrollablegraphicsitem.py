"""
..
    /------------------------------------------------------------------------------\
    |                 -- FACADE TECHNOLOGIES INC.  CONFIDENTIAL --                 |
    |------------------------------------------------------------------------------|
    |                                                                              |
    |    Copyright [2019] Facade Technologies Inc.                                 |
    |    All Rights Reserved.                                                      |
    |                                                                              |
    | NOTICE:  All information contained herein is, and remains the property of    |
    | Facade Technologies Inc. and its suppliers if any.  The intellectual and     |
    | and technical concepts contained herein are proprietary to Facade            |
    | Technologies Inc. and its suppliers and may be covered by U.S. and Foreign   |
    | Patents, patents in process, and are protected by trade secret or copyright  |
    | law.  Dissemination of this information or reproduction of this material is  |
    | strictly forbidden unless prior written permission is obtained from Facade   |
    | Technologies Inc.                                                            |
    |                                                                              |
    \------------------------------------------------------------------------------/

This module contains the ScrollableGraphicsItem class.
"""

from PySide2.QtWidgets import QGraphicsItem

class ScrollableGraphicsItem(QGraphicsItem):
    """
    This class behaves in a similar way to usual components in the TGUIM, except that it is invisible and is scrollable.
    """
    
    LEFT_OFFSET = 25  # Horizontal distance between self and the window it is associated with
    
    def __init__(self, window: 'ComponentGraphics'):
        """
        Initializes a ScrollableGraphicsItem, tying it to the top-level window it will be next to
        
        :param window: top-level window self will be next to
        :type window: ComponentGraphics
        :param parent: parent component
        :
        """
        
        root = None  # TODO: Find how to get root
        QGraphicsItem.__init__(self, root)
        self._associatedComponent = window
        
        

